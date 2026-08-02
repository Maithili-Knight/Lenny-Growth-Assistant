# 🎨 UI/UX Design Document (`design.md`) — Lenny Growth Assistant

This document outlines the UI/UX design architecture, design system tokens, interaction patterns, and user experience rationale behind the **Lenny Growth Assistant**.

---

## 👁️ 1. Design Philosophy: Impeccable Design & Modern Aesthetics

The interface is designed to provide a **WOW experience** at first glance. Rather than looking like a generic prototype, the UI mirrors the refined, dark-mode elegance of industry standards like ChatGPT and Claude while introducing custom micro-interactions tailored for growth engineers and content creators.

### Core Principles
1. **Focus on Content**: Interface elements recede into the background, letting the conversation, transcript context, and generated artifacts take visual priority.
2. **Zero Context Loss**: The split-screen panel system allows users to view chat responses on the left while simultaneously reviewing, executing, or reading code/essay artifacts on the right.
3. **Immediate Tactile Feedback**: Micro-animations, subtle hover states, glowing focus rings, and real-time streaming text reassure users that the AI agent is actively processing their inputs.

---

## 🎨 2. Design System & Visual Tokens

### Color Palette (Curated Dark Mode)
| Token | Hex / Value | Usage |
| :--- | :--- | :--- |
| **Canvas Background** | `#212121` | Main chat window background |
| **Sidebar Dark** | `#171717` | Left session list & drawer background |
| **Panel Split** | `#1e1e1f` | Claude Artifact Viewer background |
| **Surface Elevate** | `#2f2f2f` | Input capsule & active tab background |
| **Hover Highlight** | `#2a2a2a` | Sidebar item hover state |
| **Primary Text** | `#ececf1` | Headings, user text, and primary labels |
| **Muted Text** | `#8e8ea0` | Subtitles, timestamps, and section headers |
| **Emerald Accent** | `#10a37f` | Assistant avatar, active toggle, and focus ring |
| **Violet Accent** | `#5436da` | User avatar background |
| **Purple Highlight** | `#a855f7` | Artifact badge text & border glow |

### Typography System
* **Primary Font Family**: `'Outfit', sans-serif` (Google Font)
* **Code / Monospace Font**: `'Fira Code', 'Courier New', monospace`
* **Hierarchy**:
  - `h1` (App Header): `1.05rem`, Weight `600`
  - `h2` (Welcome Heading): `1.85rem`, Weight `600`, Letter Spacing `-0.5px`
  - `Body Text` (Messages): `0.95rem`, Line Height `1.7`
  - `Subtext / Badges`: `0.7rem` – `0.75rem`, Weight `600` uppercase

---

## 📐 3. Layout Architecture & Mental Models

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                       MAIN LAYOUT                                       │
├──────────────┬─────────────────────────────────────────────┬────────────────────────────┤
│   SIDEBAR    │                  CHAT PANE                  │       ARTIFACT PANE        │
│   (260px)    │            (50% split / 100% full)          │        (50% split)         │
│              │                                             │                            │
│  + New Chat  │  ┌───────────────────────────────────────┐  │  ┌──────────────────────┐  │
│              │  │ App Header + Model Switcher Pill      │  │  │ Header: Preview/Code │  │
│  CHATS       │  └───────────────────────────────────────┘  │  └──────────────────────┘  │
│  • Session 1 │  ┌───────────────────────────────────────┐  │  ┌──────────────────────┐  │
│  • Session 2 │  │ System Prompt Bar                     │  │  │ Rendered HTML iframe │  │
│  • Session 3 │  └───────────────────────────────────────┘  │  │ or Markdown Essay    │  │
│              │  ┌───────────────────────────────────────┐  │  └──────────────────────┘  │
│  [Stream 🔘] │  │ Messages Thread / Welcome Screen      │  │                            │
│              │  └───────────────────────────────────────┘  │                            │
│              │  ┌───────────────────────────────────────┐  │                            │
│              │  │ Floating Input Capsule                │  │                            │
│              │  └───────────────────────────────────────┘  │                            │
└──────────────┴─────────────────────────────────────────────┴────────────────────────────┘
```

### 1. Left Session Sidebar
- **New Chat Button**: Fixed at top with clear icon.
- **Scrollable History**: Sessions ordered chronologically with truncate overflow ellipsis.
- **Footer Controls**: Streaming response toggle cleanly grouped at the bottom.

### 2. Centered Welcome Screen (Empty State)
- When starting a fresh session (`messages.length === 0`), the complex chat window clears out, rendering a clean, centered title: **"Where should we begin?"**
- The input bar sits directly beneath the title, creating an inviting, clutter-free entry point identical to ChatGPT.

### 3. Dual-Pane Artifact Viewer (Splitscreen)
- When a user requests an essay, HTML component, or summary, the chat pane smoothly compresses from `100%` to `50%` width.
- The right-side **Artifact Viewer** slides in using a `cubic-bezier(0.4, 0, 0.2, 1)` transition.
- **Tab Navigation**: Users can toggle between:
  - **Preview Tab**: Live sandboxed `iframe` rendering for HTML/CSS or formatted Markdown essay preview.
  - **Code Tab**: Monospace raw source viewer.

---

## ⚡ 4. Key Micro-Interactions & UX Polish

### 1. Double-Click Inline Session Rename
- **User Action**: Double-click any session item in the left sidebar.
- **Transition**: The text label instantly transforms into a sleek dark input box (`.rename-input`) with an emerald focus border.
- **Completion**: Pressing `Enter` or clicking away (`onBlur`) saves the title to PostgreSQL via `PATCH /sessions/{id}` and updates the state without reloading the page.

### 2. Dynamic Model Switcher Pill
- Positioned in the header next to the title.
- Pill selector dropdown (`⚡ Local (Ollama)` vs `☁️ Cloud (Claude 3.5)`).
- Hover state increases border brightness, reassuring the user of interactivity.

### 3. Real-Time Auto-Titling
- When a user sends their first query in a session, the LLM auto-generates a 3–5 word title (e.g. *"Product-Led Growth Loops"*).
- The sidebar updates automatically upon response completion.

### 4. Interactive Artifact Badges
- In the message thread, whenever an assistant response creates a saved document, a purple badge appears (`[📄 View Essay Artifact]`).
- Clicking the badge opens or switches the side panel directly to that artifact.

---

## ♿ 5. Accessibility & Responsiveness

- **High Contrast Ratios**: Text colors (`#ececf1` on `#212121` and `#ffffff` on `#10a37f`) exceed standard WCAG AAA contrast guidelines.
- **Keyboard Navigation**: Form inputs respond to `Enter` and standard tab navigation.
- **Sandboxed Security**: Interactive HTML components render inside `<iframe sandbox="allow-scripts" />` to protect against cross-site script execution while preserving dynamic CSS layout math.
