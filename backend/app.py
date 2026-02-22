from fastapi import FastAPI
from pydantic import BaseModel
from gemini_backend import generate_response

app = FastAPI()


class QuestionRequest(BaseModel):
    field: str
    difficulty: int
    interview_type: str


class AnswerRequest(BaseModel):
    field: str
    difficulty: int
    question: str
    answer: str

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/generate-question")
def generate_question(req: QuestionRequest):

    prompt = f"""
You are conducting a {req.interview_type} interview.

Field: {req.field}

Difficulty: {req.difficulty}/10

Ask interview question.
"""

    question = generate_response(prompt)

    return {"question": question}


@app.post("/evaluate-answer")
def evaluate_answer(req: AnswerRequest):

    prompt = f"""
Field: {req.field}

Difficulty: {req.difficulty}

Question:
{req.question}

Answer:
{req.answer}

Evaluate answer.

Give score, strengths, weaknesses.
"""

    feedback = generate_response(prompt)

    return {"feedback": feedback}