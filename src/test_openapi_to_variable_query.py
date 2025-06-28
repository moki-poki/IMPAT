import sys
from openalex_api.openalex_interface import search_openalex, articles_to_variable_prompt
from openai_api.openai_api import get_prompt_result, CONTEXT_STORE

# Hardcoded list of known variables (IPCC Special Report scenarios and related variables)
KNOWN_VARIABLES = [
    "SSP1-1.9", "SSP1-2.6", "SSP2-4.5", "SSP3-7.0", "SSP5-8.5",
    "RCP2.6", "RCP4.5", "RCP6.0", "RCP8.5",
    "CO2 concentration", "global temperature", "sea level rise",
    "precipitation", "extreme weather", "mitigation", "adaptation",
    "emissions", "land use", "renewable energy", "fossil fuels"
]

# Formalized known relationship structure for context (as triples, IPCC scenarios)
KNOWN_RELATIONSHIP_STRUCTURE = """
Known variable relationships (subject, relation, object):
- ("SSP1-1.9", "is_a", "low emissions scenario")
- ("SSP1-2.6", "is_a", "sustainable development scenario")
- ("SSP2-4.5", "is_a", "intermediate scenario")
- ("SSP3-7.0", "is_a", "regional rivalry scenario")
- ("SSP5-8.5", "is_a", "high emissions scenario")
- ("RCP2.6", "corresponds_to", "SSP1-2.6")
- ("RCP4.5", "corresponds_to", "SSP2-4.5")
- ("RCP6.0", "corresponds_to", "SSP4-6.0")
- ("RCP8.5", "corresponds_to", "SSP5-8.5")
- ("CO2 concentration", "drives", "global temperature")
- ("global temperature", "influences", "sea level rise")
- ("global temperature", "affects", "precipitation")
- ("global temperature", "increases", "extreme weather")
- ("mitigation", "reduces", "emissions")
- ("adaptation", "responds_to", "climate impacts")
- ("emissions", "result_from", "fossil fuels")
- ("renewable energy", "reduces", "emissions")
- ("land use", "affects", "CO2 concentration")
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_openapi_to_variable_query.py <search terms>")
        sys.exit(1)
    # Set the context for all queries
    CONTEXT_STORE.value = (
        "You are an expert in climate science and data extraction.\n"
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
