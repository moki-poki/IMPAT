import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from openai import OpenAI

load_dotenv()  # Load environment variables from .env

app = FastAPI()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_prompt_result(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o",
        instructions="You are a coding assistant that talks like a pirate.",
        input=prompt,
    )
    return response.output_text

@app.get("/prompt")
async def get_prompt(prompt: str = Query(..., description="Prompt to send to OpenAI")):
    result = get_prompt_result(prompt)
    return JSONResponse(content={"result": result})