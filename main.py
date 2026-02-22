import streamlit as st
from gemini_backend import generate_response


# -------------------
# Session state setup
# -------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "question" not in st.session_state:
    st.session_state.question = ""

if "round" not in st.session_state:
    st.session_state.round = 1

if "history" not in st.session_state:
    st.session_state.history = []


# -------------------
# UI
# -------------------

st.title("🤖 AI Interview Platform")


# -------------------
# Start Interview
# -------------------

if st.button("Start Interview"):

    st.session_state.started = True

    st.session_state.round = 1

    prompt = "You are a technical interviewer. Ask one DSA interview question."

    st.session_state.question = generate_response(prompt)


# -------------------
# Interview loop
# -------------------

if st.session_state.started:

    st.write(f"## Round {st.session_state.round}")

    st.write("### Question:")

    st.write(st.session_state.question)


    # User reply box
    answer = st.text_area("Type your answer here:")


    if st.button("Submit Answer"):


        # Save history
        st.session_state.history.append({

            "question": st.session_state.question,

            "answer": answer

        })


        # Evaluate answer
        eval_prompt = f"""

You are an interviewer.

Question:
{st.session_state.question}

Candidate Answer:
{answer}

Evaluate the answer.

Give:

Score out of 10

Strengths

Weakness

"""

        feedback = generate_response(eval_prompt)


        st.write("## Feedback")

        st.write(feedback)


        # Next question
        next_prompt = f"""

Based on previous answer:

{answer}

Ask next interview question.

"""

        st.session_state.question = generate_response(next_prompt)
 

        st.session_state.round += 1