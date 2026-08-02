"""
Chat CRUD — Orchestrates the full chat pipeline.

Flow:
    1. Load conversation history
    2. Save user message to database
    3. Retrieve RAG context from ChromaDB
    4. Detect active skill (QA vs Ship30for30)
    5. Build system prompt via skills module
    6. Generate LLM response
    7. Save assistant message
    8. Auto-title the session (first message only)
    9. Generate artifact (if applicable)
    10. Return response
"""

import logging

from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest
from app.services.retriever import retrieve_context
from app.services.llm_service import generate_llm_response, generate_artifact_unified
from app.services.skills import detect_skill, build_system_prompt

from app.crud.artifact import create_artifact
from app.schemas.artifact import ArtifactCreate
from app.services.ollama_service import generate_response_stream

from app.crud.message import (
    create_message,
    get_session_messages,
)
from app.schemas.message import MessageCreate
from app.crud.session import update_session_title

logger = logging.getLogger(__name__)


def chat(
    db: Session,
    request: ChatRequest,
):
    """
    Process a chat request through the full pipeline:
    history → RAG → skill detection → LLM → save → auto-title → artifacts.
    """

    # ── Step 1: Load conversation history ──
    history_messages = get_session_messages(
        db=db,
        session_id=request.session_id,
        limit=10,
    )

    conversation_history = ""
    for message in history_messages:
        conversation_history += (
            f"{message.role.title()}: "
            f"{message.content}\n"
        )

    logger.info(f"Session {request.session_id} — loaded {len(history_messages)} history messages")

    # ── Step 2: Resolve user query ──
    query = request.message if request.message else request.prompt

    # ── Step 3: Save user message to database ──
    create_message(
        db=db,
        session_id=request.session_id,
        message=MessageCreate(
            role="user",
            content=query,
        ),
    )

    # ── Step 4: Retrieve RAG context from ChromaDB ──
    chunks = retrieve_context(
        query=query,
        n_results=5,
    )
    context = "\n\n".join(chunks)

    # ── Step 5: Detect active skill ──
    active_skill = detect_skill(query)
    logger.info(f"Active skill for session {request.session_id}: {active_skill}")

    # ── Step 6: Build system prompt via skills module ──
    custom_instructions = request.system_prompt if request.system_prompt else ""

    system_prompt = build_system_prompt(
        skill=active_skill,
        conversation_history=conversation_history,
        context=context,
        custom_instructions=custom_instructions,
    )

    # ── Step 7: Generate LLM response ──
    provider = request.llm_provider
    if provider and request.session_id:
        from app.models.session import ChatSession
        session_obj = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
        if session_obj:
            session_obj.llm_provider = provider
            db.commit()

    answer = generate_llm_response(
        message=query,
        system_prompt=system_prompt,
        provider=provider,
    )

    # ── Step 8: Save assistant message ──
    create_message(
        db=db,
        session_id=request.session_id,
        message=MessageCreate(
            role="assistant",
            content=answer,
        ),
    )

    # ── Step 9: Auto-title generation (first message only) ──
    session_title = None
    if len(history_messages) == 0:
        try:
            title_prompt = (
                f'Generate a concise 3-5 word title for a conversation that starts with this message: "{query}". '
                f'Return ONLY the title text, no quotes, no punctuation, no explanation.'
            )
            generated_title = generate_llm_response(
                message=title_prompt,
                system_prompt="You are a helpful assistant that generates short chat titles.",
                provider=provider,
            )
            generated_title = generated_title.strip().strip('"').strip("'")
            if len(generated_title) > 60:
                generated_title = generated_title[:57] + "..."
            if generated_title:
                update_session_title(db, request.session_id, generated_title)
                session_title = generated_title
                logger.info(f"Auto-titled session {request.session_id}: {generated_title}")
        except Exception as e:
            logger.warning(f"Failed to auto-generate session title: {e}")

    # ── Step 10: Artifact generation (keyword-triggered) ──
    artifact_id = None

    artifact_keywords = [
        "summarize", "summary", "meeting notes", "action items",
        "todo", "to-do", "report", "blog", "notes",
        "essay", "ship30for30", "ship30", "article",
        "html", "css", "code",
    ]

    if query and any(keyword in query.lower() for keyword in artifact_keywords):
        query_lower = query.lower()
        if "html" in query_lower or "css" in query_lower or "code" in query_lower:
            art_type = "html"
        elif "essay" in query_lower or "ship30for30" in query_lower or "article" in query_lower:
            art_type = "essay"
        else:
            art_type = "summary"

        try:
            artifact = generate_artifact_unified(
                artifact_type=art_type,
                prompt=query,
                provider=provider,
            )

            saved_artifact = create_artifact(
                db=db,
                artifact=ArtifactCreate(
                    session_id=request.session_id,
                    type=artifact["type"],
                    title=artifact["title"],
                    content=artifact["content"],
                ),
            )

            artifact_id = saved_artifact.id
            logger.info(f"Created artifact {artifact_id} (type={art_type}) for session {request.session_id}")
        except Exception as e:
            logger.error(f"Artifact generation failed: {e}")

    return {
        "response": answer,
        "artifact_id": artifact_id,
        "session_title": session_title,
    }


def chat_stream(
    db: Session,
    request: ChatRequest,
):
    """
    Stream a chat response token-by-token via Ollama / Claude.
    Saves the user query and the final generated response to the database.
    """
    # ── Step 1: Load conversation history ──
    history_messages = get_session_messages(
        db=db,
        session_id=request.session_id,
        limit=10,
    )

    conversation_history = ""
    for message in history_messages:
        conversation_history += (
            f"{message.role.title()}: "
            f"{message.content}\n"
        )

    # ── Step 2: Resolve user query ──
    query = request.message if request.message else request.prompt

    # ── Step 3: Save user message to database ──
    create_message(
        db=db,
        session_id=request.session_id,
        message=MessageCreate(
            role="user",
            content=query,
        ),
    )

    # ── Step 4: Retrieve RAG context from ChromaDB ──
    chunks = retrieve_context(
        query=query,
        n_results=5,
    )
    context = "\n\n".join(chunks)

    # ── Step 5: Detect active skill ──
    active_skill = detect_skill(query)

    # ── Step 6: Build system prompt via skills module ──
    custom_instructions = request.system_prompt if request.system_prompt else ""
    system_prompt = build_system_prompt(
        skill=active_skill,
        conversation_history=conversation_history,
        context=context,
        custom_instructions=custom_instructions,
    )

    # ── Step 7: Stream LLM response & save at end ──
    provider = request.llm_provider
    if provider and request.session_id:
        from app.models.session import ChatSession
        session_obj = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
        if session_obj:
            session_obj.llm_provider = provider
            db.commit()

    from app.services.llm_service import generate_llm_response_stream

    def generator():
        full_response = ""
        for chunk in generate_llm_response_stream(
            message=query,
            system_prompt=system_prompt,
            provider=provider,
        ):
            full_response += chunk
            yield chunk

        # Save assistant message once stream completes
        if full_response.strip():
            create_message(
                db=db,
                session_id=request.session_id,
                message=MessageCreate(
                    role="assistant",
                    content=full_response,
                ),
            )

            # Auto-title generation (first message only)
            if len(history_messages) == 0:
                try:
                    title_prompt = (
                        f'Generate a concise 3-5 word title for a conversation that starts with this message: "{query}". '
                        f'Return ONLY the title text, no quotes, no punctuation, no explanation.'
                    )
                    generated_title = generate_llm_response(
                        message=title_prompt,
                        system_prompt="You are a helpful assistant that generates short chat titles.",
                        provider=provider,
                    )
                    generated_title = generated_title.strip().strip('"').strip("'")
                    if len(generated_title) > 60:
                        generated_title = generated_title[:57] + "..."
                    if generated_title:
                        update_session_title(db, request.session_id, generated_title)
                except Exception as e:
                    logger.warning(f"Failed to auto-generate session title in stream: {e}")

    return generator()