import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Body
from fastapi.responses import JSONResponse
from openai import OpenAI

load_dotenv()  # Load environment variables from .env

app = FastAPI()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Use a context store that persists across requests
class ContextStore:
    value = ""

CONTEXT_STORE = ContextStore()

def get_prompt_result(prompt: str) -> str:
    context = CONTEXT_STORE.value
    full_prompt = f"{context}\n{prompt}" if context else prompt
    response = client.responses.create(
        model="gpt-4o",
        instructions="You are a coding assistant that talks like a pirate.",
        input=full_prompt,
    )
    return response.output_text

@app.get("/prompt")
async def get_prompt(prompt: str = Query(..., description="Prompt to send to OpenAI")):
    result = get_prompt_result(prompt)
    return JSONResponse(content={"result": result})

@app.post("/set_context")
async def set_context(context: str = Body(..., embed=True)):
    CONTEXT_STORE.value = context
    return {"message": "Context updated."}

@app.get("/get_context")
async def get_context():
    return {"context": CONTEXT_STORE.value}