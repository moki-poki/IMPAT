from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openalex_api.openalex_interface import search_openalex, articles_to_variable_prompt
from openai_api.openai_api import get_prompt_result
import itertools
import re
import random

app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

def build_openalex_keyword_prompt(data):
    """
    Build a prompt for OpenAI to extract a list of OpenAlex search keywords from the form data.
    """
    prompt = (
        "Given the following user submission form data, return a JSON array of up to 10 relevant search keywords "
        "that would be most effective for querying the OpenAlex scientific literature database. "
        "Order the keywords by importance, with the most important first. "
        "Each keyword must be a single word (no spaces or phrases). "
        "Focus on extracting terms that best represent the research context, location, planning horizon, and relevant sectors. "
        "Return only the JSON array as your response.\n\n"
        f"Location: {data.get('location', '')}\n"
        f"Planning Horizon: {data.get('planning_horizon', '')}\n"
        f"Available Investment: {data.get('available_investment', '')} EUR\n"
        f"Relevant Sectors: {', '.join(data.get('relevant_sectors', []))}\n"
    )
    return prompt

def build_markdown(data, articles, prompts, responses, keywords):
    from openalex_api.openalex_interface import inverted_index_to_abstract
    md = ["# Submission\n"]
    md.append(f"**Location:** {data.get('location', '')}\n")
    md.append(f"**Planning Horizon:** {data.get('planning_horizon', '')}\n")
    md.append(f"**Available Investment:** {data.get('available_investment', '')} EUR\n")
    md.append("**Relevant Sectors:**\n" + ''.join(f"- {s}\n" for s in data.get('relevant_sectors', [])))
    md.append("\n## Literature Search Keywords\n")
    md.append(", ".join(keywords))
    md.append("\n## OpenAlex Results\n")
    for i, article in enumerate(articles):
        md.append(f"### Article {i+1}\n")
        md.append(f"**Title:** {article.title}\n")
        md.append(f"**Authors:** {', '.join(article.authors)}\n")
        readable_abstract = inverted_index_to_abstract(article.abstract_inversion)
        md.append(f"**Abstract:** {readable_abstract}\n")
        md.append(f"**Database Query:**\n\n{responses[i]}\n")
    return '\n'.join(md)

def random_keyword_impact(keywords):
    """
    Randomly split 100 among the keywords, returning a list of dicts with 'keyword' and 'impact'.
    """
    if not keywords:
        return []
    n = len(keywords)
    # Generate n-1 random cut points between 0 and 100
    cuts = sorted([0] + [random.randint(0, 100) for _ in range(n - 1)] + [100])
    impacts = [cuts[i+1] - cuts[i] for i in range(n)]
    # Shuffle to avoid always giving the first keyword the largest chunk
    random.shuffle(impacts)
    return [{"keyword": k, "impact": v} for k, v in zip(keywords, impacts)]

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # Expecting JSON
    print("\n===== USER INPUT =====")
    print(data)
    # Build prompt and get keywords from OpenAI
    keyword_prompt = build_openalex_keyword_prompt(data)
    print("\n===== KEYWORD PROMPT TO LLM =====")
    print(keyword_prompt)
    import json as _json
    try:
        keyword_response = get_prompt_result(keyword_prompt)
        print("\n===== LLM KEYWORD RESPONSE =====")
        print(keyword_response)
        # Remove code block markers if present
        if keyword_response.strip().startswith('```'):
            keyword_response = keyword_response.strip().strip('`').strip('json').strip()
        # Parse as JSON
        keywords = _json.loads(keyword_response)
        # Only keep single words, deduplicate, and clean
        flat_keywords = []
        for kw in keywords:
            if isinstance(kw, str):
                word = kw.strip()
                if word and ' ' not in word:
                    flat_keywords.append(word)
        # Remove duplicates while preserving order
        seen = set()
        keywords = []
        for word in flat_keywords:
            if word not in seen:
                seen.add(word)
                keywords.append(word)
        # Limit to max 5 keywords for OpenAlex search
        keywords = keywords[:5]
        if not isinstance(keywords, list):
            raise ValueError("LLM did not return a list of keywords")
    except Exception as e:
        print(f"Keyword extraction failed: {e}")
        keywords = []
    print("\n===== SEARCH KEYWORDS =====")
    print(keywords)
    articles = search_openalex(keywords, per_page=3)  # Limit for demo
    print("\n===== OPENALEX ARTICLES =====")
    for i, article in enumerate(articles):
        print(f"Article {i+1}: {article.title}")
    prompts = list(map(articles_to_variable_prompt, articles))
    print("\n===== PROMPTS TO LLM =====")
    for i, prompt in enumerate(prompts):
        print(f"Prompt {i+1}:\n{prompt}\n")
    responses = list(map(get_prompt_result, prompts))
    print("\n===== LLM RESPONSES =====")
    for i, resp in enumerate(responses):
        print(f"Response {i+1}:\n{resp}\n")
    markdown_content = build_markdown(data, articles, prompts, responses, keywords)
    output_filename = "output.md"
    output_path = Path(app.static_folder) / output_filename
    output_path.write_text(markdown_content)
    file_url = f"/{output_filename}"

    # Convert MD to PDF using docutils/md_to_pdf.py
    try:
        from docutils.md_to_pdf import md_to_pdf
        pdf_path = md_to_pdf(output_path)
        pdf_url = f"/{pdf_path.name}"
    except Exception as e:
        print(f"PDF conversion failed: {e}")
        pdf_url = None

    # Add keyword impact structure
    keyword_impact = random_keyword_impact(keywords)

    return jsonify({
        "status": "ok",
        "message": "Markdown file saved!",
        "file_url": file_url,
        "pdf_url": pdf_url,
        "keyword_impact": keyword_impact
    })

if __name__ == '__main__':
    app.run(debug=True)
