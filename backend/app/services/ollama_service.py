import ollama
from ollama import Client
from app.core.config import settings

# Initialize Ollama client with host setting
client = Client(host=settings.ollama_base_url)


def generate_response(prompt: str) -> str:
    response = client.chat(
        model=settings.ollama_model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]


def generate_rag_response(
    question: str,
    context: str,
):
    prompt = f"""
You are Lenny Growth Assistant.

Answer ONLY using the context below.

If the answer is not present in the context,
say:

"I couldn't find that information in the knowledge base."

-------------------------
Context

{context}

-------------------------

Question:

{question}

Answer:
"""

    return generate_response(prompt)