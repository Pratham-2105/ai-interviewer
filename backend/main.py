from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from gemini_backend import generate_response
import uuid
import json
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# In-memory session storage
# -----------------------------
sessions: Dict[str, dict] = {}

# -----------------------------
# Models
# -----------------------------
class StartInterviewRequest(BaseModel):
    field: str
    interview_type: str
    difficulty: int
    total_rounds: int
    resume: str = ""
    job_description: str = ""

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

# -----------------------------
# Helper Functions
# -----------------------------

def build_question_prompt(session):
    return f"""
You are conducting a {session['interview_type']} interview.

Field: {session['field']}
Difficulty Level: {session['difficulty']}/10

Resume:
{session['resume']}

Job Description:
{session['job_description']}

Ask a challenging interview question appropriate to the difficulty level.
"""

def build_evaluation_prompt(session, question, answer):
    return f"""
You are evaluating a candidate's interview response.

Field: {session['field']}
Interview Type: {session['interview_type']}
Difficulty: {session['difficulty']}/10

Question:
{question}

Candidate Answer:
{answer}

Return your evaluation STRICTLY in this JSON format:

{{
  "score": integer (1-10),
  "communication_score": integer (1-10),
  "technical_score": integer (1-10),
  "confidence_score": integer (1-10),
  "strengths": "string",
  "weaknesses": "string"
}}

Rules:
- Return ONLY valid JSON.
- Do not include markdown/code fences.
- Do not include any text before or after JSON.
"""

def build_final_prompt(session):
    return f"""
You conducted a full interview.

Field: {session['field']}

Interview History:
{session['history']}

Average Score: {session['average_score']}

Generate final structured report:

Overall Summary
Strengths
Weaknesses
Hiring Recommendation
"""

def calculate_average_score(score_history):
    if not score_history:
        return 0
    return round(sum(score_history) / len(score_history), 2)

def parse_feedback(raw_feedback: str):
    text = (raw_feedback or "").strip()

    # Direct JSON parse first.
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return normalize_feedback(parsed)
    except Exception:
        pass

    # Handle markdown fenced blocks and mixed output by extracting the first JSON object.
    fenced = re.search(r"```(?:json)?\s*({[\s\S]*?})\s*```", text, re.IGNORECASE)
    if fenced:
        try:
            parsed = json.loads(fenced.group(1))
            if isinstance(parsed, dict):
                return normalize_feedback(parsed)
        except Exception:
            pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            parsed = json.loads(text[start:end + 1])
            if isinstance(parsed, dict):
                return normalize_feedback(parsed)
        except Exception:
            pass

    return None

def clamp_score(value):
    try:
        n = int(value)
    except Exception:
        return 0
    return max(1, min(10, n))

def normalize_feedback(payload: dict):
    required_text_fields = ["strengths", "weaknesses"]
    for key in required_text_fields:
        if key not in payload:
            payload[key] = ""

    communication_score = clamp_score(payload.get("communication_score", 0))
    technical_score = clamp_score(payload.get("technical_score", 0))
    confidence_score = clamp_score(payload.get("confidence_score", 0))
    score = clamp_score(payload.get("score", 0))

    if score == 0:
        sub_scores = [v for v in [communication_score, technical_score, confidence_score] if v > 0]
        if sub_scores:
            score = round(sum(sub_scores) / len(sub_scores))

    normalized = {
        "score": score,
        "communication_score": communication_score,
        "technical_score": technical_score,
        "confidence_score": confidence_score,
        "strengths": str(payload.get("strengths", "")),
        "weaknesses": str(payload.get("weaknesses", "")),
    }

    # If all scores are missing/invalid, treat this as a parse failure.
    score_values = [
        normalized["score"],
        normalized["communication_score"],
        normalized["technical_score"],
        normalized["confidence_score"],
    ]
    if all(v == 0 for v in score_values):
        return None
    return normalized

# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"message": "AI Interview Backend Running"}

# -----------------------------
# Start Interview
# -----------------------------
@app.post("/start-interview")
def start_interview(data: StartInterviewRequest):

    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "field": data.field,
        "interview_type": data.interview_type,
        "difficulty": data.difficulty,
        "total_rounds": data.total_rounds,
        "current_round": 1,
        "resume": data.resume,
        "job_description": data.job_description,
        "history": [],
        "score_history": [],
        "average_score": 0
    }

    question_prompt = build_question_prompt(sessions[session_id])
    question = generate_response(question_prompt)

    sessions[session_id]["current_question"] = question

    return {
        "session_id": session_id,
        "question": question
    }

# -----------------------------
# Submit Answer
# -----------------------------
@app.post("/submit-answer")
def submit_answer(data: AnswerRequest):

    session = sessions.get(data.session_id)

    if not session:
        return {"error": "Invalid session ID"}

    question = session["current_question"]

    eval_prompt = build_evaluation_prompt(session, question, data.answer)
    raw_feedback = generate_response(eval_prompt)
    feedback_json = parse_feedback(raw_feedback)
    if feedback_json is None:
        return {
            "error": "Failed to parse AI response",
            "raw_response": raw_feedback
        }

    # Store history
    session["history"].append({
        "question": question,
        "answer": data.answer,
        "evaluation": feedback_json
    })

    # Store score
    session["score_history"].append(feedback_json["score"])
    session["average_score"] = calculate_average_score(session["score_history"])

    # Adaptive difficulty logic
    score = feedback_json["score"]

    if score >= 8:
        session["difficulty"] = min(10, session["difficulty"] + 2)
    elif score <= 4:
        session["difficulty"] = max(1, session["difficulty"] - 1)
    else:
        session["difficulty"] = min(10, session["difficulty"] + 1)

    session["current_round"] += 1

    # Interview Complete
    if session["current_round"] > session["total_rounds"]:

        final_prompt = build_final_prompt(session)
        final_report = generate_response(final_prompt)

        return {
            "feedback": feedback_json,
            "interview_complete": True,
            "final_report": final_report,
            "average_score": session["average_score"]
        }

    # Generate next question
    next_question_prompt = build_question_prompt(session)
    next_question = generate_response(next_question_prompt)

    session["current_question"] = next_question

    return {
        "feedback": feedback_json,
        "interview_complete": False,
        "next_question": next_question,
        "current_round": session["current_round"],
        "average_score": session["average_score"]
    }

# -----------------------------
# Analytics Endpoint
# -----------------------------
@app.get("/session-summary/{session_id}")
def session_summary(session_id: str):

    session = sessions.get(session_id)

    if not session:
        return {"error": "Invalid session ID"}

    return {
        "total_rounds": session["total_rounds"],
        "completed_rounds": len(session["score_history"]),
        "average_score": session["average_score"],
        "score_history": session["score_history"],
        "difficulty_current": session["difficulty"]
    }
