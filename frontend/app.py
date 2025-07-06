import streamlit as st
import sys
import os

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from db import (
    create_user, get_user_by_name, log_question,
    log_feedback, log_performance, get_recent_performance
)
from content_generator import generate_math_question
from adaptive_logic import adjust_difficulty

st.set_page_config(page_title="Reflective AI Math Tutor", page_icon="🧠")
st.title("🧠 Reflective AI Math Tutor")

# --- Step 1: User Info Form ---
with st.form("user_form"):
    name = st.text_input("Enter your name:")
    grade = st.selectbox("Grade Level", ["Grade 3", "Grade 4", "Grade 5"])
    topic = st.text_input("Topic (e.g., multiplication):", value="multiplication")
    submitted = st.form_submit_button("Start Session")

if submitted and name:
    # Check or create user
    user = get_user_by_name(name)
    if user:
        st.success(f"👋 Welcome back, {user['name']}!")
        user_id = user["_id"]
    else:
        user_id = create_user(name, grade)
        st.success("✅ New user created!")

    # --- Step 2: Adjust Difficulty & Generate Question ---
    recent_logs = get_recent_performance(user_id, limit=5)
    difficulty = adjust_difficulty(recent_logs)
    st.info(f"📊 Based on your performance, difficulty is: **{difficulty}**")

    question = generate_math_question(grade, topic)
    st.subheader("📘 Your Math Question")
    st.write(question)

    # --- Step 3: Answer Form ---
    with st.form("answer_form"):
        answer = st.text_input("Your Answer:")
        correct = st.radio("Was your answer correct?", ["Yes", "No"])
        reflection = st.text_area("Why did you choose that answer?")
        emoji = st.selectbox("How do you feel?", ["😊", "😕", "😠", "😐"])
        confidence = st.selectbox("Confidence level", ["high", "medium", "low"])
        submit_answer = st.form_submit_button("Submit Answer")

    if submit_answer:
        correct_bool = correct == "Yes"
        question_id = log_question(user_id, question, answer, correct_bool)
        log_feedback(question_id, reflection, emoji, confidence)
        log_performance(user_id, topic, correct_bool, emoji)
        st.success("📝 Your answer and feedback have been recorded.")

        # --- Step 4: Show Performance ---
        st.subheader("📊 Your Recent Performance")
        logs = get_recent_performance(user_id, limit=5)
        for log in logs:
            st.write(f"- 🕒 {log['timestamp']} | ✅ Correct: {log['correct']} | 😐 Emotion: {log['emotion']}")
