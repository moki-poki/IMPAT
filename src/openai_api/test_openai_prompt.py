import sys
from get_prompt_result import get_prompt_result

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_openai_prompt.py <your prompt>")
        sys.exit(1)
    prompt = " ".join(sys.argv[1:])
    result = get_prompt_result(prompt)
    print(result)

if __name__ == "__main__":
    main()
