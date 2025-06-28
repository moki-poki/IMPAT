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

# Example usage:
# terms = ["climate", "impact", "lentil"]
# print(search_openalex(terms))
