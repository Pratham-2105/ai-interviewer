import streamlit as st
from backend.gemini_backend import generate_response


# ------------------------
# SESSION STATE
# ------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "question" not in st.session_state:
    st.session_state.question = ""

if "round" not in st.session_state:
    st.session_state.round = 1

if "history" not in st.session_state:
    st.session_state.history = []

if "difficulty" not in st.session_state:
    st.session_state.difficulty = 1


# ------------------------
# UI HEADER
# ------------------------

st.title("🌍 Universal AI Interview Platform")


# ------------------------
# USER INPUT OPTIONS
# ------------------------

field = st.selectbox(

    "Select Interview Field",

    [

        "Software Engineering",

        "Data Science",

        "Machine Learning",

        "Product Management",

        "Marketing",

        "Finance",

        "Consulting",

        "Human Resources",

        "Sales",

        "Custom"

    ]

)


if field == "Custom":

    field = st.text_input("Enter Custom Field")


total_rounds = st.slider(

    "Number of Rounds",

    1,

    10,

    3

)


base_difficulty = st.slider(

    "Starting Difficulty",

    1,

    10,

    3

)


# ------------------------
# START BUTTON
# ------------------------

if st.button("Start Interview"):

    st.session_state.started = True

    st.session_state.round = 1

    st.session_state.history = []

    st.session_state.difficulty = base_difficulty


    prompt = f"""

You are a professional interviewer.

Field: {field}

Difficulty Level: {st.session_state.difficulty}/10

Ask interview question.

"""

    st.session_state.question = generate_response(prompt)

# ------------------------
# SESSION STATE ADDITIONS
# ------------------------

if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False

if "interview_complete" not in st.session_state:
    st.session_state.interview_complete = False


# ------------------------
# INTERVIEW LOOP
# ------------------------

if st.session_state.started and not st.session_state.interview_complete:

    st.write(f"## Round {st.session_state.round} / {total_rounds}")

    st.write(f"Difficulty: {st.session_state.difficulty}/10")

    st.write("### Question:")
    st.write(st.session_state.question)


    # Only show answer box if feedback not shown yet
    if not st.session_state.show_feedback:

        answer = st.text_area("Your Answer", key=f"answer_{st.session_state.round}")


        if st.button("Submit Answer"):

            st.session_state.current_answer = answer

            eval_prompt = f"""
Field: {field}
Difficulty: {st.session_state.difficulty}

Question:
{st.session_state.question}

Answer:
{answer}

Evaluate answer.
Give score, strengths, weaknesses.
"""

            st.session_state.feedback = generate_response(eval_prompt)

            st.session_state.show_feedback = True

            st.rerun()


    # Show feedback
    if st.session_state.show_feedback:

        st.write("## Feedback")
        st.write(st.session_state.feedback)


        # Save history
        st.session_state.history.append({

            "question": st.session_state.question,

            "answer": st.session_state.current_answer,

            "difficulty": st.session_state.difficulty

        })


        # NEXT ROUND BUTTON
        if st.button("Next Round"):


            # Increase difficulty gradually
            difficulty_step = max(1, int(10 / total_rounds))

            st.session_state.difficulty = min(
                10,
                st.session_state.difficulty + difficulty_step
            )


            st.session_state.round += 1


            # Check interview finished
            if st.session_state.round > total_rounds:

                st.session_state.interview_complete = True

                st.rerun()


            # Generate harder question
            next_prompt = f"""
You are a professional interviewer.

Field: {field}

Difficulty: {st.session_state.difficulty}/10

Ask a more challenging and deeper question than previous round.

"""

            st.session_state.question = generate_response(next_prompt)


            st.session_state.show_feedback = False

            st.rerun()


# ------------------------
# FINAL REPORT
# ------------------------

if st.session_state.interview_complete:

    st.write("# Interview Complete")


    report_prompt = f"""
Field: {field}

Interview history:

{st.session_state.history}

Generate final interview report.

Include:

Overall score
Strengths
Weaknesses
Final hiring decision
"""

    report = generate_response(report_prompt)

    st.write(report)

    st.session_state.started = False