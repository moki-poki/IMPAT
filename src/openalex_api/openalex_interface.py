from dataclasses import dataclass
from typing import List, Dict, Any
import requests

@dataclass
class Article:
    title: str
    authors: List[str]
    abstract_inversion: Dict[str, Any]

def search_openalex(terms, per_page=10) -> List[Article]:
    """
    Query OpenAlex API with a list of terms.
    Returns a list of Article dataclass instances.
    """
    query = "+".join(terms)
    url = (
        "https://api.openalex.org/works"
        "?page=1"
        f"&filter=title_and_abstract.search:{query}"
        "&sort=relevance_score:desc"
        f"&per_page={per_page}"
        "&select=title,authorships,abstract_inverted_index"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    results = []
    for work in data.get("results", []):
        title = work.get("title", "")
        # Extract author names
        authors = []
        for auth in work.get("authorships", []):
            author_name = auth.get("author", {}).get("display_name")
            if author_name:
                authors.append(author_name)
        abstract_inv = work.get("abstract_inverted_index", {})
        results.append(Article(
            title=title,
            authors=authors,
            abstract_inversion=abstract_inv
        ))
    return results

def articles_to_variable_prompt(article: Article) -> str:
    """
    Create a prompt for a single article that asks the LLM to return a structured query
    using the known variables and their relationships from the context.
    The LLM must return a structured output (e.g., JSON).
    """
    prompt_lines = [
        "Given the following scientific article, use the known variables and their relationships provided in the context.",
        "Return a structured JSON object with the following fields:",
        "- relevant_variables: a list of variable names from the known variables that are relevant to this article",
        "- variable_query: a query string or structure that could be used to retrieve data about these variables and their relationships",
        "",
        f"Title: {article.title}",
        f"Authors: {', '.join(article.authors) if article.authors else 'N/A'}",
    ]
    if article.abstract_inversion:
        prompt_lines.append(f"Abstract: {inverted_index_to_abstract(article.abstract_inversion)}")
    else:
        prompt_lines.append("Abstract: N/A")
    prompt_lines.append(
        "\nReturn only the JSON object as your response."
    )
    return "\n".join(prompt_lines)

def inverted_index_to_abstract(abstract_inversion: dict) -> str:
    """
    Convert OpenAlex abstract_inverted_index to a readable abstract string.
    """
    if not abstract_inversion:
        return ""
    # Create a list where index is the word position
    word_positions = []
    for word, positions in abstract_inversion.items():
        for pos in positions:
            word_positions.append((pos, word))
    # Sort by position and join words
    word_positions.sort()
    abstract_words = [word for pos, word in word_positions]
    return " ".join(abstract_words)

# Example usage:
# terms = ["climate", "impact", "lentil"]
# print(search_openalex(terms))
