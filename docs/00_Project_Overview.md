# Project Overview

**Project Name:** The Lenny Growth Assistant
**Version:** 1.0
**Author:** Maithili Kumar
**Project Type:** Agentic AI Web Application
**Status:** Design Phase

---

# Overview

The **Lenny Growth Assistant** is an Agentic AI-powered conversational workspace that enables users to explore, understand, and transform insights from **Lenny Rachitsky's Podcast** through grounded conversations and intelligent content generation.

The application combines Retrieval-Augmented Generation (RAG), specialized AI agents, persistent conversation memory, and configurable Large Language Models (LLMs) into a modern ChatGPT-like experience. Users can ask transcript-based questions, generate long-form content in the Ship30for30 writing style, and create reusable Markdown or HTML artifacts that are rendered directly inside the application.

The project demonstrates modern AI engineering principles including modular architecture, agent orchestration, provider abstraction, persistent state management, and production-inspired software design.

---

# Vision

Build a production-inspired AI assistant that transforms static podcast transcripts into an interactive knowledge platform capable of answering questions, generating content, and producing reusable artifacts through specialized AI agents.

---

# Objectives

## Product Objectives

* Provide conversational access to Lenny's podcast knowledge.
* Generate grounded, reliable responses from transcript data.
* Offer a seamless ChatGPT-like user experience.
* Enable users to transform conversations into reusable content.

## Engineering Objectives

* Design a modular and maintainable architecture.
* Support multiple LLM providers without code changes.
* Demonstrate agent orchestration instead of a single monolithic chatbot.
* Follow production-oriented software engineering practices.

---

# Core Features

## 1. Conversational AI

* Chat-based interface
* Multiple conversation sessions
* Persistent chat history
* Context-aware responses

---

## 2. Knowledge Assistant (RAG)

* Transcript ingestion
* Semantic search
* Context retrieval
* Grounded answers

---

## 3. Ship30for30 Writing Assistant

Generate structured long-form articles featuring:

* Strong opening hook
* Clear section hierarchy
* Bullet points
* Bold highlights
* Actionable takeaways

---

## 4. Artifact Generation

Generate reusable artifacts such as:

* Markdown documents
* HTML pages
* Documentation
* Technical notes

---

## 5. Artifact Viewer

Render generated content directly inside the application.

Supported formats include:

* Markdown Preview
* HTML Preview

---

## 6. Multiple LLM Providers

The application supports both local and cloud-based language models.

* Ollama (Local)
* Anthropic Claude (Cloud)

The provider can be switched through configuration without modifying application logic.

---

# High-Level System Architecture

                         +----------------------+
                         |        User          |
                         +----------+-----------+
                                    |
                                    v
                  +------------------------------------+
                  |      React Frontend (UI Layer)     |
                  |------------------------------------|
                  | Chat | History | Artifacts | Config|
                  +----------------+-------------------+
                                   |
                                   v
                  +------------------------------------+
                  |      FastAPI Backend (API Layer)   |
                  +----------------+-------------------+
                                   |
                                   v
                  +------------------------------------+
                  |      Agent Orchestrator            |
                  +--------+------------+--------------+
                           |            |
          +----------------+            +----------------+
          |                                     |
          v                                     v
+-----------------------+          +-------------------------+
| Transcript QA Agent   |          | Content Generation Agent|
+-----------+-----------+          +------------+------------+
            |                                     |
            |                                     |
            v                                     v
     +--------------+                   +------------------+
     | RAG Retriever|                   | Artifact Agent   |
     +------+-------+                   +---------+--------+
            |                                     |
            +-------------------+-----------------+
                                |
                                v
                  +-------------------------------+
                  |     LLM Provider Layer        |
                  |-------------------------------|
                  | Ollama | Claude | OpenAI      |
                  +---------------+---------------+
                                  |
                                  v
          +-----------------------------------------------+
          | Knowledge & Persistence Layer                 |
          |-----------------------------------------------|
          | FAISS | Transcript Dataset | PostgreSQL       |
          +-----------------------------------------------+

# Technology Stack

| Layer              | Technology                    |
| ------------------ | ----------------------------- |
| Frontend           | React + Vite + Tailwind CSS   |
| Backend            | FastAPI                       |
| Database           | PostgreSQL (Supabase)         |
| ORM                | SQLAlchemy                    |
| Validation         | Pydantic                      |
| Vector Store       | FAISS                         |
| Embedding Model    | SentenceTransformers          |
| Local LLM          | Ollama                        |
| Cloud LLM          | Anthropic Claude              |
| Artifact Rendering | React Markdown + HTML Preview |
| Version Control    | Git + GitHub                  |

---

# Engineering Principles

The project is designed around the following principles.

## Separation of Concerns

Business logic, APIs, AI orchestration, persistence, and frontend rendering are implemented as independent modules.

---

## Agent-Based Architecture

Rather than using a single prompt for every request, the application routes requests to specialized agents based on user intent.

Examples include:

* Transcript Question Answering Agent
* Content Generation Agent
* Artifact Generation Agent

---

## Configurable LLM Layer

All interactions with language models pass through a common provider interface.

Benefits include:

* Easy model replacement
* Reduced code duplication
* Simplified testing
* Support for both local and cloud providers

---

## Retrieval-Augmented Generation

Responses to transcript-related questions are generated only after retrieving relevant knowledge from the indexed transcript collection, reducing hallucinations and improving factual consistency.

---

## Persistent Conversations

Every conversation is associated with a unique session and stored in PostgreSQL, allowing users to resume previous chats.

---

# Repository Structure

```text
lenny-growth-assistant/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── agents/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── prompts/
│   │   ├── utils/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│
├── docs/
│
├── data/
│
├── scripts/
│
├── agent_transcripts/
│
├── README.md
│
└── docker-compose.yml
```

---

# Development Workflow

The project follows an incremental development lifecycle.

1. Product Discovery
2. Requirements Analysis
3. System Architecture Design
4. Database Design
5. API Design
6. Backend Development
7. AI Integration
8. Frontend Development
9. Testing
10. Documentation
11. Deployment

---

# Documentation Roadmap

| Document                  | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| 00_Project_Overview.md    | High-level project introduction            |
| 01_PRD.md                 | Product requirements and business goals    |
| 02_System_Architecture.md | Overall software architecture              |
| 03_Database_Design.md     | Database schema and relationships          |
| 04_API_Specification.md   | REST API documentation                     |
| 05_Agent_Architecture.md  | Agent routing and orchestration            |
| 06_RAG_Architecture.md    | Knowledge ingestion and retrieval pipeline |
| 07_UI_UX_Design.md        | User experience and interface decisions    |
| 08_Deployment_Guide.md    | Local setup and deployment instructions    |
| 09_Testing_Strategy.md    | Testing methodology and validation         |
| 10_Future_Roadmap.md      | Planned enhancements                       |

---

# Expected Deliverables

* FastAPI Backend
* React Frontend
* PostgreSQL Database
* Retrieval-Augmented Generation Pipeline
* Agent-Based AI Orchestration
* Configurable LLM Provider Layer
* Artifact Generation and Viewer
* Complete Engineering Documentation
* Deployment Guide
* Public GitHub Repository
* Demonstration Video

---

# Guiding Principle

> **Build an AI assistant that is modular, explainable, grounded in trusted knowledge, and engineered like a production system rather than a prototype.**
