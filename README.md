# MeetMind 🧠

> AI-Powered Meeting Notes Generator

## Overview

MeetMind is an AI-powered assistant that transforms meeting recordings into structured summaries, decisions, and actionable tasks, eliminating the need for manual note-taking.

The goal of MeetMind is to help teams save time, improve productivity, and ensure that important discussions, decisions, and responsibilities are never lost after a meeting.

---

## Problem

In many meetings, participants focus on discussions rather than taking notes. As a result:

- Important information may be missed.
- Manual note-taking is time-consuming.
- Action items can be forgotten.
- Decisions become difficult to track later.
- Meeting records are often scattered and unorganized.

---

## Solution

MeetMind automatically processes meeting recordings and converts them into structured knowledge.

The platform will:

- Convert speech into text using Speech-to-Text technology.
- Generate concise meeting summaries.
- Identify key discussion points.
- Extract decisions made during meetings.
- Detect action items and responsible owners.
- Generate follow-up notes for participants.
- Build a searchable knowledge base of past meetings.

---

## Example

### Meeting Conversation

> Rahul will prepare the project report by Friday.
>
> Marketing campaign will start next week.
>
> Budget of ₹50,000 is approved.

### MeetMind Output

#### Summary

- Project report discussion completed.
- Marketing campaign approved.
- Budget approved.

#### Action Items

| Task | Owner | Deadline |
|------|--------|----------|
| Prepare project report | Rahul | Friday |
| Start marketing campaign | Marketing Team | Next Week |

#### Decisions

- Budget of ₹50,000 approved.

---

## Planned Features

### Phase 1 – MVP

- Audio Upload
- Video Upload
- Speech-to-Text Transcription
- AI Meeting Summaries
- Decision Extraction
- Action Item Extraction
- Meeting History
- PDF Export
- DOCX Export

### Phase 2 – Enhanced Collaboration

- Speaker Identification
- Semantic Search
- Meeting Dashboard
- Task Tracking
- Meeting Analytics

### Phase 3 – AI Assistant Features

- AI Meeting Chatbot
- Follow-up Email Generation
- Smart Task Detection
- Multi-Language Support
- Organization Knowledge Base

### Phase 4 – Integrations

- Zoom Integration
- Google Meet Integration
- Microsoft Teams Integration
- Slack Integration
- Jira Integration
- Notion Integration
- Trello Integration

---

## Proposed Architecture

```text
Upload Recording
        │
        ▼
Speech-to-Text Engine
        │
        ▼
Transcript Generation
        │
        ▼
AI Processing Layer
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
Summary Decisions Action Items
        │
        ▼
Database Storage
        │
        ▼
Dashboard & Search
```

## Tech Stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- Shadcn UI

### Backend

- FastAPI (Python)

### Database

- PostgreSQL

### AI & Machine Learning

- OpenAI Whisper
- Large Language Models (LLMs)
- pgvector (Vector Search)

### Deployment

- Vercel (Frontend)
- Railway / Render / AWS (Backend)
- PostgreSQL Database

---

## Development Roadmap

### Sprint 1

- Repository Setup
- Project Structure
- Backend Initialization
- Frontend Initialization
- Database Design

### Sprint 2

- Audio/Video Upload System
- File Storage
- Meeting Management

### Sprint 3

- Whisper Integration
- Transcript Generation
- Transcript Viewer

### Sprint 4

- AI Summary Generation
- Decision Extraction
- Action Item Detection

### Sprint 5

- Dashboard
- Meeting History
- Export Functionality

### Sprint 6

- Semantic Search
- Vector Database Integration

### Sprint 7

- Meeting Chatbot (RAG)

### Sprint 8

- Third-Party Integrations

---

## Project Status

🚧 **UNDER ACTIVE DEVELOPMENT**

MeetMind is currently in the early development stage.

The project is being built incrementally with proper version control, documentation, and milestone-based development.

Features, architecture, and implementation details may change as the project evolves.

---

## Long-Term Vision

MeetMind aims to become more than a transcription tool.

The vision is to create a complete Meeting Intelligence Platform that helps organizations:

- Capture meeting knowledge automatically
- Track decisions across teams
- Manage action items efficiently
- Search historical discussions instantly
- Interact with meeting records through AI

---

## Contributing

Contributions, suggestions, and feedback will be welcome in future releases.

---

### Built with ❤️ as part of the MeetMind Project
