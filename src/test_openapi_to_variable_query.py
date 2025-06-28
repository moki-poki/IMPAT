import sys
from openalex_api.openalex_interface import search_openalex, articles_to_variable_prompt
from openai_api.openai_api import get_prompt_result

# Hardcoded list of known variables
KNOWN_VARIABLES = [
    "climate", "impact", "lentil", "yield", "temperature", "precipitation",
    "soil moisture", "growth rate", "photosynthesis", "harvest", "disease"
]

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_openapi_to_variable_query.py <search terms>")
        sys.exit(1)
    terms = sys.argv[1:]
    articles = search_openalex(terms)
    for idx, article in enumerate(articles, 1):
        prompt = articles_to_variable_prompt(article, KNOWN_VARIABLES)
        print(f"\n--- Prompt for Article {idx} ---\n")
        print(prompt)
        print("\n--- OpenAI Response ---\n")
        result = get_prompt_result(prompt)
        print(result)
        print("\n==============================\n")

if __name__ == "__main__":
    main()
