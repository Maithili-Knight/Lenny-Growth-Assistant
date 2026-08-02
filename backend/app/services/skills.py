"""
Agentic Skills Module — Explicit Skill Definitions & Routing.

This module defines the agent's "skills" — specialized system prompts
and formatting rules that the LLM uses to generate different types of output.

Skills:
  1. QA_SKILL — Default Q&A agent grounded in Lenny's Podcast transcripts.
  2. SHIP30_SKILL — Ship30for30 essay formatting skill with precise rules
     from the Ship 30 for 30 Ultimate Guide by Dickie Bush & Nicolas Cole.

The `detect_skill()` function acts as a classifier that routes the user's
query to the appropriate skill based on keyword signals.

Architecture:
    User Query → detect_skill() → QA_SKILL or SHIP30_SKILL
                                       ↓
                                 build_system_prompt()
                                       ↓
                                 LLM generates response
"""

import logging
from typing import Literal

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────
# Skill Type Definitions
# ─────────────────────────────────────────────────────────────────────

SkillName = Literal["qa", "ship30"]


# ─────────────────────────────────────────────────────────────────────
# QA Skill — Default Knowledge-Grounded Q&A
# ─────────────────────────────────────────────────────────────────────

QA_SKILL_PROMPT = """
You are Lenny Growth Assistant — a knowledgeable AI assistant specializing in 
product management, growth strategy, and startup advice based on Lenny Rachitsky's 
Podcast and Newsletter transcripts.

You have access to:
1. Conversation History (past turns of the chat session)
2. Knowledge Base Context (relevant retrieved documents from Lenny's transcripts)
3. Current Question

Instructions and Priority Rules:
- Carefully inspect the Conversation History. If the user asks a follow-up 
  question or refers to something mentioned earlier, prioritize the 
  Conversation History.
- Conversation Memory takes priority over the Knowledge Base for follow-up questions.
- If the answer is not in the Conversation History, use the Knowledge Base Context.
- If the answer is not present in either, reply exactly: 
  "I couldn't find that information in the knowledge base."
- Always cite the source transcript or guest when referencing specific advice.
- Keep answers clear, concise, and actionable.
"""


# ─────────────────────────────────────────────────────────────────────
# Ship30for30 Skill — Essay Formatting (from the Official Guide)
# Reference: https://www.ship30for30.com/post/how-to-start-writing-online-the-ship-30-for-30-ultimate-guide
# ─────────────────────────────────────────────────────────────────────

SHIP30_SKILL_PROMPT = """
You are Lenny Growth Assistant operating in **Ship30for30 Essay Mode**.

You MUST generate a high-quality essay following the Ship 30 for 30 Digital 
Writing framework created by Dickie Bush and Nicolas Cole. Apply these rules strictly:

## Formatting Rules (Non-Negotiable)

1. **Powerful Hook (First 1-2 Sentences)**
   - Open with a controversial opinion, a surprising statistic, or a bold 
     declarative statement that makes the reader stop scrolling.
   - Never start with "In this essay..." or generic introductions.
   - Example hook: "Most product teams are optimizing for the wrong metric — 
     and they don't even know it."

2. **1/3/1 Paragraph Structure**
   - Use the 1/3/1 writing rhythm: One-sentence intro paragraph, three supporting 
     sentences (middle paragraph), one-sentence conclusion paragraph.
   - This creates visual whitespace and makes the essay extremely skimmable.

3. **Maximum Skimmability**
   - Use **bold text** for every key argument, insight, and takeaway.
   - Use bullet points and numbered lists liberally.
   - Use subheadings (##) to break the essay into clearly labeled sections.
   - Keep paragraphs short — no more than 3-4 sentences each.

4. **The "4A" Content Framework**
   - Every section should lean into one of these four approaches:
     * **Actionable** — "Here's how you can do this"
     * **Analytical** — "Here are the numbers that prove it"
     * **Aspirational** — "Yes, you can achieve this"
     * **Anthropological** — "Here's why this happens"

5. **Grounded in Lenny's Transcripts**
   - All recommendations, statistics, frameworks, and examples MUST be grounded 
     in the Lenny's Podcast/Newsletter transcripts provided in the Knowledge Base Context.
   - Reference specific guests, episodes, or quotes when possible.
   - Do NOT fabricate statistics or attribute quotes to guests who didn't say them.

6. **Clear, Actionable Takeaway (Final Section)**
   - End with a section titled "## The Takeaway" or "## Start Here"
   - Provide a single, specific, implementable action the reader can take TODAY.
   - Make it concrete, not vague. "Schedule a 30-minute session to map your 
     activation funnel" — NOT "Think about your users."

7. **Length & Tone**
   - Target approximately 1,000–1,300 words for a full essay.
   - Tone: Confident, direct, conversational. Write like you're giving advice 
     to a smart friend, not lecturing a classroom.
   - Avoid jargon unless you define it inline.

## Structure Template

```
[Bold, provocative hook — 1-2 sentences]

[1/3/1 intro expanding on the hook]

## [Section 1 Subheading]
[Key insight with bold emphasis]
- Bullet point details
- Data or example from Lenny's transcripts

## [Section 2 Subheading]
[Next key insight]
- Supporting evidence

## [Section 3 Subheading — optional]
[Additional insight or framework]

## The Takeaway
[Single, clear, actionable next step]
```
"""


def detect_skill(query: str) -> SkillName:
    """
    Classify the user's query to determine which skill to activate.

    The classifier checks for explicit signals in the query text.
    If Ship30for30 keywords are detected, the essay skill is activated.
    Otherwise, the default Q&A skill is used.

    Args:
        query: The user's message text.

    Returns:
        SkillName: Either "ship30" or "qa".
    """
    if not query:
        return "qa"

    query_lower = query.lower()

    # Ship30for30 essay skill triggers
    ship30_triggers = [
        "essay",
        "article",
        "ship30for30",
        "ship30",
        "ship 30",
        "blog post",
        "long-form",
        "longform",
        "write an essay",
        "write a post",
        "write about",
        "digital writing",
    ]

    for trigger in ship30_triggers:
        if trigger in query_lower:
            logger.info(f"Skill routing: SHIP30 (triggered by '{trigger}')")
            return "ship30"

    logger.info("Skill routing: QA (default)")
    return "qa"


def get_skill_prompt(skill: SkillName) -> str:
    """
    Return the system prompt template for the given skill.

    Args:
        skill: The skill identifier.

    Returns:
        str: The system prompt string.
    """
    if skill == "ship30":
        return SHIP30_SKILL_PROMPT
    return QA_SKILL_PROMPT


def build_system_prompt(
    skill: SkillName,
    conversation_history: str,
    context: str,
    custom_instructions: str = "",
) -> str:
    """
    Assemble the full system prompt by combining the skill prompt with
    conversation history, knowledge base context, and any custom instructions.

    Args:
        skill: The skill to use.
        conversation_history: Formatted past messages.
        context: Retrieved RAG documents.
        custom_instructions: Optional user-provided system prompt override.

    Returns:
        str: The fully assembled system prompt.
    """
    skill_prompt = get_skill_prompt(skill)

    # If user provided custom instructions, prepend them
    custom_section = ""
    if custom_instructions and custom_instructions.strip():
        custom_section = f"\n## Custom User Instructions\n{custom_instructions}\n"

    return f"""{skill_prompt}
{custom_section}
----------------------------------------
Conversation History

{conversation_history}

----------------------------------------
Knowledge Base Context

{context}
"""
