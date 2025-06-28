import sys
from openalex_api.openalex_interface import search_openalex, articles_to_variable_prompt
from openai_api.openai_api import get_prompt_result, CONTEXT_STORE

# Hardcoded list of known variables
KNOWN_VARIABLES = [
    "climate", "impact", "lentil", "yield", "temperature", "precipitation",
    "soil moisture", "growth rate", "photosynthesis", "harvest", "disease"
]

# Formalized known relationship structure for context (as triples)
KNOWN_RELATIONSHIP_STRUCTURE = """
Known variable relationships (subject, relation, object):
- ("climate", "affects", "temperature")
- ("climate", "affects", "precipitation")
- ("temperature", "influences", "soil moisture")
- ("precipitation", "influences", "soil moisture")
- ("soil moisture", "impacts", "growth rate")
- ("soil moisture", "impacts", "yield")
- ("growth rate", "linked_to", "photosynthesis")
- ("disease", "reduces", "yield")
- ("disease", "affects", "harvest")
- ("lentil", "is_a", "crop of interest")
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_openapi_to_variable_query.py <search terms>")
        sys.exit(1)
    # Set the context for all queries
    CONTEXT_STORE.value = (
        "You are an expert in agricultural science and data extraction.\n"
        f"Known variables: {', '.join(KNOWN_VARIABLES)}\n"
        f"{KNOWN_RELATIONSHIP_STRUCTURE.strip()}\n"
    )
    terms = sys.argv[1:]
    articles = search_openalex(terms)
    for idx, article in enumerate(articles, 1):
        prompt = articles_to_variable_prompt(article)
        print(f"\n--- Prompt for Article {idx} ---\n")
        print(prompt)
        print("\n--- OpenAI Response ---\n")
        result = get_prompt_result(prompt)
        print(result)
        print("\n==============================\n")

if __name__ == "__main__":
    main()
