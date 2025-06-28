from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openalex_api.openalex_interface import search_openalex, articles_to_variable_prompt
from openai_api.openai_api import get_prompt_result
import itertools
import re

app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

def extract_keywords(data):
    # Use all string fields and relevant_sectors as keywords
    fields = [
        data.get('location', ''),
        data.get('planning_horizon', ''),
    ]
    sectors = data.get('relevant_sectors', [])
    # Only keep alphanumeric words from fields
    words = set()
    for f in fields:
        words.update(re.findall(r'\b\w+\b', f))
    # Clean sector names to remove special characters
    clean_sectors = [re.sub(r'[^\w ]', '', s) for s in sectors]
    keywords = list(words.union(clean_sectors))
    # Remove empty strings and join with + for OpenAlex
    return [k for k in keywords if k]

def build_markdown(data, articles, prompts, responses):
    from openalex_api.openalex_interface import inverted_index_to_abstract
    md = ["# Submission\n"]
    md.append(f"**Location:** {data.get('location', '')}\n")
    md.append(f"**Planning Horizon:** {data.get('planning_horizon', '')}\n")
    md.append(f"**Available Investment:** {data.get('available_investment', '')} EUR\n")
    md.append("**Relevant Sectors:**\n" + ''.join(f"- {s}\n" for s in data.get('relevant_sectors', [])))
    md.append("\n## Literature Search Keywords\n")
    md.append(", ".join(extract_keywords(data)))
    md.append("\n## OpenAlex Results\n")
    for i, article in enumerate(articles):
        md.append(f"### Article {i+1}\n")
        md.append(f"**Title:** {article.title}\n")
        md.append(f"**Authors:** {', '.join(article.authors)}\n")
        readable_abstract = inverted_index_to_abstract(article.abstract_inversion)
        md.append(f"**Abstract:** {readable_abstract}\n")
        md.append(f"**Database Query:**\n\n{responses[i]}\n")
    return '\n'.join(md)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # Expecting JSON
    print("\n===== USER INPUT =====")
    print(data)
    keywords = extract_keywords(data)
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
    markdown_content = build_markdown(data, articles, prompts, responses)
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

    return jsonify({"status": "ok", "message": "Markdown file saved!", "file_url": file_url, "pdf_url": pdf_url})

if __name__ == '__main__':
    app.run(debug=True)
