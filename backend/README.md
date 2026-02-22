Agentic AI Mock Interview Platform – Backend Documentation

1. Project Overview

This backend powers an Agentic AI-based Mock Interview System that:

Conducts multi-round interviews

Adapts difficulty dynamically

Evaluates responses using structured scoring

Tracks session state

Generates final structured interview reports

Exposes REST APIs for frontend integration

The system is session-aware and maintains progressive context across rounds.

2. Architecture Overview
Frontend (React / Voice UI)
        ↓
FastAPI Backend (Python)
        ↓
Gemini 3 Flash Preview (REST API)
Responsibilities

Frontend

Captures user input (text or voice → text)

Calls backend endpoints

Displays questions, feedback, and final report

Backend

Manages interview session state

Builds prompts

Calls Gemini

Parses structured responses

Adjusts difficulty

Tracks scoring analytics

Gemini

Generates questions

Evaluates answers

Produces final summary

3. Backend Tech Stack

Python

FastAPI

Pydantic

Requests

Gemini REST API (gemini-3-flash-preview)

UUID-based session tracking

In-memory session store

4. Project Structure
project/
│
├── backend/
│   ├── main.py
│   ├── gemini_backend.py
│   ├── config.py
│   └── README.md
│
└── frontend/
5. Core Design Decisions
1. REST Instead of SDK

Gemini is accessed using direct REST calls to avoid SDK quota and dependency issues.

2. Session-Based Architecture

Each interview session is tracked using:

sessions: Dict[str, dict]

Key session fields:

{
  field,
  interview_type,
  difficulty,
  total_rounds,
  current_round,
  resume,
  job_description,
  history,
  score_history,
  average_score,
  current_question
}
3. Adaptive Difficulty

Difficulty adjusts based on performance:

Score ≥ 8 → Increase difficulty +2

Score 5–7 → Increase difficulty +1

Score ≤ 4 → Decrease difficulty -1

This creates progressive agentic behavior.

4. Structured Scoring

Gemini is instructed to return strict JSON:

{
  "score": 8,
  "communication_score": 7,
  "technical_score": 8,
  "confidence_score": 9,
  "strengths": "...",
  "weaknesses": "..."
}

Backend parses this into structured analytics.

6. API Endpoints
GET /

Health check.

Response:

{
  "message": "AI Interview Backend Running"
}
POST /start-interview
Request
{
  "field": "Software Engineering",
  "interview_type": "Technical",
  "difficulty": 5,
  "total_rounds": 3,
  "resume": "...",
  "job_description": "..."
}
Response
{
  "session_id": "uuid",
  "question": "First interview question..."
}

Creates a new interview session.

POST /submit-answer
Request
{
  "session_id": "uuid",
  "answer": "Candidate response..."
}
If interview not finished:
{
  "feedback": { structured scoring },
  "interview_complete": false,
  "next_question": "...",
  "current_round": 2,
  "average_score": 7.5
}
If interview finished:
{
  "feedback": { structured scoring },
  "interview_complete": true,
  "final_report": "...",
  "average_score": 7.8
}
GET /session-summary/{session_id}

Returns analytics:

{
  "total_rounds": 3,
  "completed_rounds": 3,
  "average_score": 7.8,
  "score_history": [6, 8, 9],
  "difficulty_current": 9
}
7. Interview Flow

Frontend calls /start-interview

Backend:

Stores session

Generates first question

Frontend displays question

User answers

Frontend calls /submit-answer

Backend:

Evaluates answer

Parses structured scoring

Updates difficulty

Stores history

Generates next question OR final report

Repeat until complete

8. Voice Integration (Planned)

Current design:

Frontend:

Capture microphone

Convert speech → text

Send text to backend

Backend:

Treats input as normal answer text

Future:

Streaming

WebSockets

TTS support

9. Current Limitations

Sessions stored in memory (lost on restart)

No authentication

No database persistence

No streaming responses

No multi-user scaling layer

10. Git Workflow

Current Branch Structure:

main                  ← Stable backend
frontend-dev          ← Frontend work
feature/*             ← Temporary feature branches

Workflow followed:

Create feature branch

Implement changes

Commit with descriptive message

Push branch

Merge into main

Delete feature branch

Backend is now merged into main.

11. What This Demonstrates

API Design

State Management

AI Orchestration

Adaptive Difficulty Modeling

Structured AI Output Parsing

Session Tracking

Progressive Interview Simulation

12. Future Roadmap
Phase 2

Database (Postgres / Redis)

Authentication

Interviewer personality modes

Trend analytics visualization

Phase 3

Real-time conversation mode

Streaming responses

Voice-to-voice interaction

Cloud deployment

Final Status

Backend:

Complete

Stable

Structured

Adaptive

Ready for frontend integration
