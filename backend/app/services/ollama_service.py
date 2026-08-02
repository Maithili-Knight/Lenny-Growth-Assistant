"""
Ollama LLM Service Layer.

Provides local LLM inference via the Ollama API.
Accepts the same (message, system_prompt) interface as the Claude service
for clean provider-switching through llm_service.py.
"""

import json
import logging

import ollama
from ollama import Client, ResponseError

from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize Ollama client with host setting
client = Client(host=settings.ollama_base_url)


def generate_response(
    message: str,
    system_prompt: str = "You are a helpful AI assistant.",
) -> str:
    """
    Generate a response from the local Ollama model.

    Args:
        message: The user's message/query.
        system_prompt: System-level instructions for the model.

    Returns:
        str: The generated response text.

    Raises:
        ConnectionError: If Ollama server is unreachable.
        RuntimeError: If the model fails to generate a response.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    try:
        response = client.chat(
            model=settings.ollama_model,
            messages=messages,
        )
        return response["message"]["content"]

    except ResponseError as e:
        logger.error(f"Ollama API error: {e}")
        raise RuntimeError(f"Ollama model error: {str(e)}")
    except Exception as e:
        error_msg = str(e).lower()
        if "connect" in error_msg or "refused" in error_msg or "timeout" in error_msg:
            logger.error(f"Ollama server connection failed: {e}")
            raise ConnectionError(
                f"Cannot connect to Ollama at {settings.ollama_base_url}. "
                f"Make sure Ollama is running: `ollama serve`"
            )
        logger.error(f"Unexpected Ollama error: {e}")
        raise RuntimeError(f"Unexpected error during Ollama response generation: {str(e)}")


def generate_response_stream(prompt: str):
    """
    Stream a response from the local Ollama model token-by-token.
    """
    try:
        stream = client.chat(
            model=settings.ollama_model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        for chunk in stream:
            yield chunk["message"]["content"]

    except Exception as e:
        logger.error(f"Ollama streaming error: {e}")
        yield f"\n[Error: {str(e)}]"


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
- Carefully inspect the Conversation History.
- If the user asks a follow-up question or refers to something mentioned earlier, prioritize the Conversation History.
- Conversation Memory takes priority over the Knowledge Base for follow-up questions.
- If the answer is not in the Conversation History, use the Knowledge Base Context.
- If the answer is not present in either, reply exactly:
"I couldn't find that information in the knowledge base."

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

    return generate_response(message=prompt)


def generate_artifact(
    artifact_type: str,
    prompt: str,
):
    full_prompt = f"""
You are an AI assistant.

Generate a {artifact_type}.

Return ONLY valid JSON.

Format:

{{
    "title": "...",
    "type": "{artifact_type}",
    "content": "..."
}}

User Request:

{prompt}
"""

    response = generate_response(message=full_prompt)

    return json.loads(response)