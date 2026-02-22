from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from gemini_backend import generate_response
import uuid

app = FastAPI()


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
        "history": []
    }

    question_prompt = f"""
You are conducting a {data.interview_type} interview.

Field: {data.field}

Difficulty Level: {data.difficulty}/10

Resume:
{data.resume}

Job Description:
{data.job_description}

Ask first interview question.
"""

    question = generate_response(question_prompt)

    sessions[session_id]["current_question"] = question

    return {
        "session_id": session_id,
        "question": question
    }


# -----------------------------
# Submit Answer & Get Next
# -----------------------------

@app.post("/submit-answer")
def submit_answer(data: AnswerRequest):

    session = sessions.get(data.session_id)

    if not session:
        return {"error": "Invalid session ID"}

    question = session["current_question"]

    eval_prompt = f"""
Field: {session['field']}
Interview Type: {session['interview_type']}
Difficulty: {session['difficulty']}/10

Question:
{question}

Candidate Answer:
{data.answer}

Evaluate answer.

Give:
Score /10
Strength
Weakness
"""

    feedback = generate_response(eval_prompt)

    session["history"].append({
        "question": question,
        "answer": data.answer,
        "feedback": feedback
    })

    # Increase difficulty slightly
    difficulty_step = max(1, int(10 / session["total_rounds"]))
    session["difficulty"] = min(10, session["difficulty"] + difficulty_step)

    session["current_round"] += 1

    if session["current_round"] > session["total_rounds"]:

        final_prompt = f"""
Field: {session['field']}

Interview History:
{session['history']}

Generate final report:

Overall Score
Strengths
Weaknesses
Hiring Recommendation
"""

        final_report = generate_response(final_prompt)

        return {
            "feedback": feedback,
            "interview_complete": True,
            "final_report": final_report
        }

    # Generate next harder question
    next_question_prompt = f"""
You are conducting a {session['interview_type']} interview.

Field: {session['field']}

Difficulty Level: {session['difficulty']}/10

Ask a more complex and deeper question than previous round.
"""

    next_question = generate_response(next_question_prompt)

    session["current_question"] = next_question

    return {
        "feedback": feedback,
        "interview_complete": False,
        "next_question": next_question,
        "current_round": session["current_round"]
    }