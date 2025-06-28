# IMPAT

IMPAT is a Python-based toolkit for searching scientific articles using the OpenAlex API, extracting relevant information, and leveraging OpenAI's API to analyze and filter variables from article content.

## Features

- Search for scientific articles via OpenAlex.
- Extract article metadata (title, authors, abstract).
- Reconstruct abstracts from OpenAlex's inverted index format.
- Generate prompts to identify relevant variables in articles.
- Query OpenAI's API with custom prompts.
- FastAPI interface for OpenAI prompt results.

## Structure

- `src/openalex_api/`
  - `openalex_interface.py`: Functions and dataclasses for OpenAlex queries and prompt generation.
  - `test_openalex.py`: CLI to search OpenAlex and output results in Markdown.
  - `test_openalex_variable_prompt.py`: CLI to generate variable-filtering prompts for articles.
- `src/openai_api/`
  - `get_prompt_result.py`: FastAPI app and function to query OpenAI with a prompt.
  - `test_openai_prompt.py`: CLI to send a prompt to OpenAI and print the result.
- `src/test_openapi_to_variable_query.py`: End-to-end CLI: search articles, generate prompts, and get OpenAI responses.
- `.env`: Store your OpenAI API key as `OPENAI_API_KEY=...`
- `requirements.txt`: Python dependencies.

## Usage

1. **Install dependencies:**
   ```bash
   pip install -r src/requirements.txt
   ```

2. **Set up your OpenAI API key:**
   - Create a `.env` file in the project root with:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Search for articles:**
   ```bash
   python src/openalex_api/test_openalex.py climate impact lentil
   ```

4. **Generate prompts for variable extraction:**
   ```bash
   python src/openalex_api/test_openalex_variable_prompt.py climate impact lentil
   ```

5. **Send a custom prompt to OpenAI:**
   ```bash
   python src/openai_api/test_openai_prompt.py "Your prompt here"
   ```

6. **End-to-end variable extraction using OpenAI:**
   ```bash
   python src/test_openapi_to_variable_query.py climate impact lentil
   ```

## Notes

- The FastAPI interface can be run with:
  ```bash
  uvicorn openai_api.get_prompt_result:app --reload --app-dir src
  ```
- Make sure your `.env` file is present and contains your OpenAI API key.

---


