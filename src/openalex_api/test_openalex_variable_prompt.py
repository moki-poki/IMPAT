import sys
from openalex_interface import search_openalex, articles_to_variable_prompt

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_openalex_variable_prompt.py <search terms>")
        sys.exit(1)
    terms = sys.argv[1:]
    articles = search_openalex(terms)
    for article in articles:
        prompt = articles_to_variable_prompt(article=article, known_variables=["climate", "impact", "lentil"])
        print(prompt)
        print("--- End of prompt ---")
        print()
        print()
    print("--- End of prompts ---")

if __name__ == "__main__":
    main()
