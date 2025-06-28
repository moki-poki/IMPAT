import sys
from openalex_interface import search_openalex

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_openalex.py <search terms>")
        sys.exit(1)
    terms = sys.argv[1:]
    results = search_openalex(terms)
    md_lines = ["# OpenAlex Search Results\n"]
    for i, res in enumerate(results, 1):
        md_lines.append(f"## Result {i}")
        md_lines.append(f"**Title:** {res['title']}")
        md_lines.append(f"**Authors:** {', '.join(res['authors']) if res['authors'] else 'N/A'}")
        md_lines.append("**Abstract Inversion:**")
        md_lines.append(f"```\n{res['abstract_inversion']}\n```")
        md_lines.append("")
    with open("openalex_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print("Results written to openalex_results.md")

if __name__ == "__main__":
    main()
