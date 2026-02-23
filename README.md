# AI Interviewer

AI-powered mock interview platform with adaptive difficulty, structured scoring, and session analytics.

This project simulates real technical interviews using Google Gemini API and provides detailed feedback across multiple evaluation dimensions.

---

## Overview

AI Interviewer is a full-stack web application built with:

- FastAPI backend
- Vanilla JavaScript frontend
- Google Gemini API for question generation and evaluation
- In-memory session management with adaptive difficulty

The system dynamically adjusts interview difficulty based on performance and generates structured JSON feedback including technical, communication, and confidence scores.

---

## Features

- Multi-round interview sessions
- Adaptive difficulty adjustment
- Structured scoring (technical, communication, confidence)
- Final performance report
- Session analytics endpoint
- Resume and Job Description contextualization
- Clean frontend UI with API-based communication

---

## Tech Stack

Backend:
- FastAPI
- Uvicorn
- Pydantic
- Google Generative AI
- Requests

Frontend:
- HTML
- CSS
- Vanilla JavaScript (Fetch API)

---

## Project Structure

ai_interviewer/
│
├── backend/
│   ├── main.py
│   ├── gemini_backend.py
│   ├── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
└── README.md

---

# 🚀 Running the Project Locally

## 1. Clone Repository

git clone https://github.com/Pratham-2105/ai-interviewer.git  
cd ai-interviewer

---

## 2. Setup Backend

cd backend

Create virtual environment:

python -m venv venv

Activate:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn main:app --reload

Backend will run at:
http://127.0.0.1:8000

Verify by visiting:
http://127.0.0.1:8000

You should see:
{"message": "AI Interview Backend Running"}

---

## 3. Setup Environment Variables

Create a `.env` file inside the backend folder:

GEMINI_API_KEY=your_api_key_here

Ensure gemini_backend.py loads this key using python-dotenv.

---

## 4. Run Frontend

Open a new terminal.

cd frontend

Start local server:

python -m http.server 5500

Open browser:

http://localhost:5500

Set API Base to:

http://127.0.0.1:8000

Start interview.

---

## API Endpoints

POST /start-interview  
POST /submit-answer  
GET /session-summary/{session_id}

---

## Architecture Notes

- Sessions are stored in memory (reset when backend restarts).
- Difficulty dynamically adjusts based on previous round scores.
- Evaluation responses are strictly parsed JSON to ensure structured scoring.
- CORS enabled for local development.

---

## Future Improvements

- Persistent database storage
- Authentication system
- Docker deployment
- Cloud hosting
- Performance analytics dashboard

---

## Author

Pratham Srivastava

---

## License

MIT