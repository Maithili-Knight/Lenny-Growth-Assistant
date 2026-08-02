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
    history: str,
):
    prompt = f"""
You are Lenny Growth Assistant.

You have access to:
1. Conversation History (past turns of the chat session)
2. Knowledge Base Context (relevant retrieved documents)
3. Current Question

Instructions and Priority Rules:
- Carefully inspect the Conversation History. If the user asks a follow-up question, resolves pronouns (such as "it", "they", "this company", "that placement"), or asks about a topic already discussed/mentioned in the Conversation History (e.g., what company/topic they are preparing for), you MUST prioritize the Conversation History to answer.
- Memory takes absolute priority over the Knowledge Base Context when answering follow-up questions.
- If the information is NOT present in the Conversation History, use the Knowledge Base Context.
- If the answer cannot be found in either, reply exactly: "I couldn't find that information in the knowledge base."

----------------------------------------
Conversation History

{history}

----------------------------------------
Knowledge Base Context

{context}

----------------------------------------
Current Question

{question}

Answer:
"""

    return generate_response(prompt)