"""
Unified LLM Service Layer.

Acts as a gateway/provider selection abstraction, keeping the FastAPI routing layer
isolated from concrete LLM provider integrations (Claude / Ollama).

The active provider is controlled by the `LLM_PROVIDER` setting in `.env`:
  - "claude" → Anthropic Claude API (cloud)
  - "ollama" → Local Ollama server (local)
"""

import json
import logging

from app.core.config import settings
from app.services import claude
from app.services import ollama_service as ollama

logger = logging.getLogger(__name__)


def generate_llm_response(
    message: str,
    system_prompt: str = None,
    provider: str = None,
) -> str:
    """
    Selects the configured LLM provider and generates a response.

    Args:
        message: The user query.
        system_prompt: The system prompt. Defaults to a generic assistant if None.
        provider: Optional provider override ("claude" or "ollama").

    Returns:
        str: Response text from the selected LLM provider.

    Raises:
        ValueError: If the message is empty or provider is unsupported.
        ConnectionError: If the LLM provider is unreachable.
        RuntimeError: If the LLM provider returns an error.
    """
    # 1. Validate empty message
    if not message or not message.strip():
        raise ValueError("Message input cannot be empty.")

    # 2. Get system prompt (use default if missing or empty)
    sys_prompt = system_prompt
    if not sys_prompt or not sys_prompt.strip():
        sys_prompt = "You are a helpful AI assistant."

    # 3. Read provider (use override parameter or fallback to env configuration)
    selected_provider = (provider or settings.llm_provider or "claude").lower().strip()

    # 4. Route to the appropriate provider
    if selected_provider == "claude":
        logger.info("Routing chat request to OpenRouter (Claude) provider.")
        try:
            has_key = settings.openrouter_api_key or settings.anthropic_api_key
            if not has_key:
                raise ValueError("No OpenRouter/Anthropic API key is configured.")
            return claude.generate_response(message=message, system_prompt=sys_prompt)
        except Exception as e:
            logger.warning(
                f"Claude API failed ({e}). "
                f"Automatically falling back to local Ollama provider."
            )
            return ollama.generate_response(message=message, system_prompt=sys_prompt)

    elif selected_provider == "ollama":
        logger.info("Routing chat request to local Ollama provider.")
        return ollama.generate_response(message=message, system_prompt=sys_prompt)

    else:
        logger.error(f"Unsupported LLM provider requested: {selected_provider}")
        raise ValueError(
            f"Unsupported LLM provider: '{selected_provider}'. "
            f"Supported values: 'claude', 'ollama'."
        )


def generate_llm_response_stream(
    message: str,
    system_prompt: str = None,
    provider: str = None,
):
    """
    Selects the configured LLM provider and streams the response token-by-token.
    If the active provider (e.g. Claude) fails or returns an error (e.g. HTTP 402),
    it seamlessly falls back and streams from local Ollama.
    """
    if not message or not message.strip():
        raise ValueError("Message input cannot be empty.")

    sys_prompt = system_prompt or "You are a helpful AI assistant."
    selected_provider = (provider or settings.llm_provider or "claude").lower().strip()

    if selected_provider == "claude":
        logger.info("Routing streaming chat request to OpenRouter (Claude) provider.")
        
        def stream_with_fallback():
            has_emitted = False
            fallback_needed = False
            
            try:
                for chunk in claude.generate_response_stream(message=message, system_prompt=sys_prompt):
                    # Detect error keywords in initial chunks
                    if any(err_word in chunk for err_word in ["[Error:", "Stream Error:", "Connection Error:"]):
                        logger.warning(f"Claude stream yielded error: {chunk.strip()}. Switching to Ollama.")
                        fallback_needed = True
                        break
                    
                    has_emitted = True
                    yield chunk
            except Exception as e:
                logger.warning(f"Claude stream crashed: {e}. Switching to Ollama.")
                fallback_needed = True

            if fallback_needed or not has_emitted:
                logger.info("Initiating fallback stream via local Ollama...")
                for chunk in ollama.generate_response_stream(sys_prompt + "\n\nQuery: " + message):
                    yield chunk

        return stream_with_fallback()
    else:
        logger.info("Routing streaming chat request to local Ollama provider.")
        return ollama.generate_response_stream(sys_prompt + "\n\nQuery: " + message)


def generate_artifact_unified(
    artifact_type: str,
    prompt: str,
    provider: str = None,
) -> dict:
    """
    Generates an artifact containing title, type, and content using the active LLM provider.

    For HTML artifacts: asks the LLM for raw valid HTML (no JSON wrapper), 
    then builds the artifact dict manually — so the content field contains 
    pure HTML that can be rendered directly in an <iframe>.

    For other types (essay, summary): asks the LLM for JSON-formatted output.

    Args:
        artifact_type: The type of artifact ("essay", "summary", "html").
        prompt: The user's request text.
        provider: Optional provider override ("claude" or "ollama").

    Returns:
        dict: {"title": str, "type": str, "content": str}
    """
    if artifact_type == "html":
        # ── HTML Artifact: ask directly for raw HTML output ──
        html_prompt = f"""You are an expert front-end developer.

Generate a complete, self-contained, valid HTML document for the following request.

Rules:
- Output ONLY valid HTML. No JSON. No explanation. No markdown code fences.
- Start your response directly with <!DOCTYPE html>
- Include all CSS inline inside a <style> tag in the <head>.
- The design should look modern and polished (dark background preferred).
- Include all content and interactivity inline — no external CDN links.

User Request:
{prompt}
"""
        raw_html = generate_llm_response(html_prompt, provider=provider)

        # Clean up any accidental code fences (```html ... ```)
        cleaned = raw_html.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()

        return {
            "title": "Generated HTML Component",
            "type": "html",
            "content": cleaned,
        }

    else:
        # ── Non-HTML Artifacts (essay, summary): ask for JSON format ──
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
        response_text = generate_llm_response(full_prompt, provider=provider)

        # Strip any extra markdown code fences if LLM returns ```json ... ```
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```"):
            lines = cleaned_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            cleaned_text = "\n".join(lines).strip()

        try:
            return json.loads(cleaned_text)
        except Exception as e:
            logger.error(f"Error parsing artifact JSON: {str(e)}. Raw text: {response_text}")
            return {
                "title": f"Generated {artifact_type.title()}",
                "type": artifact_type,
                "content": response_text,
            }

