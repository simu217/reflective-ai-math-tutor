# app.py
import streamlit as st
from collections import Counter

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))


# Emoji → expression map (shown in the final reflections section)
emoji_map = {
    "😀": "Happy",
    "😃": "Excited",
    "😊": "Happy",
    "😐": "Neutral",
    "😟": "Confused",
    "🤔": "Thoughtful",
    "🤩": "Motivated",
    "😞": "Frustrated",
    "😌": "Relieved",
}

from backend.db import (
    create_user, log_question, log_feedback,
    log_performance, get_recent_performance
)
from backend.content_generator import generate_math_question
from backend.adaptive_logic import adjust_difficulty_with_ai, generate_motivation, analyze_reflections

# ---------------- INITIAL SETUP ----------------
def _init_state():
    defaults = {
        "answered": False,
        "asked_questions": [],
        "difficulty_level": 1,
        "question_count": 0,       # human-counted question index (1..MAX_QUESTIONS)
        "correct_streak": 0,
        "all_reflections": [],     # canonical list for score & summary (1 item per Q)
        "show_next": False,        # gate to generate next Q
        "question_text": "",
        "correct_answer": "",
        "correct_bool": None,
        "question_id": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

st.title("Reflective AI Math Tutor 🤖📚")
st.warning("⚠️ Don’t refresh/reload the page — progress will reset!")

MAX_QUESTIONS = 10 # number of quiz questions are 10

# ---------------- HELPER: show final summary ----------------
def show_and_log_final_summary():
    st.success("🎉 Quiz completed! ")

    # Score computed strictly from reflections (safe: exactly one per Q)
    correct_count = sum(1 for r in st.session_state.all_reflections if r["your_answer"])
    st.write(f"✅ Final Score: {correct_count}/{MAX_QUESTIONS}")

    # Show all reflections
    st.subheader("📝 Reflections")
    for i, r in enumerate(st.session_state.all_reflections, 1):
        expression = emoji_map.get(r["emotion"], "Neutral")
        st.markdown(f"**Q{i}: {r['question']}**")
        st.markdown(f"- Your Answer Correct? {r['your_answer']}")
        st.markdown(f"- Reflection: {r['reflection']}")
        st.markdown(f"- Emotion: {r['emotion']} ({expression}), Confidence: {r['confidence']}%")
        st.write("---")

    # Overall AI summary (strengths, areas, suggestions)
    summary = analyze_reflections(st.session_state.all_reflections,  st.session_state.name)
    st.subheader("🧠 Overall Reflection Summary")
    st.markdown(summary)

    # Decide one overall emotion to store (mode)
    emotions = [r["emotion"] for r in st.session_state.all_reflections]
    overall_emotion = None
    if emotions:
        overall_emotion = Counter(emotions).most_common(1)[0][0]

    # Log final performance (one row)
    final_score = correct_count / MAX_QUESTIONS
    log_performance(
        st.session_state.user_id,
        st.session_state.topic,
        final_score,
        st.session_state.difficulty_level
    )

    st.balloons()
    st.stop()

# ---------------- USER SETUP ----------------
if "user_id" not in st.session_state:
    name = st.text_input("Enter your name:")
    grade = st.selectbox("Select your grade", ["1", "2", "3", "4", "5"])
    topic = st.selectbox("Select a topic", ["Addition", "Subtraction", "Multiplication", "Division"])

    if st.button("Start"):
        if not name.strip() or not topic.strip():
            st.warning("⚠️ Please enter your name and select your topic before starting.")
        else:
            user_id = create_user(name, grade, topic)
            st.session_state.user_id = user_id
            st.session_state.name = name
            st.session_state.grade = grade
            st.session_state.topic = topic
            st.session_state.difficulty_level = 1
            st.session_state.correct_streak = 0
            st.session_state.question_count = 1  # first question index

            # Generate first unique question
            q, a = generate_math_question(
                grade, topic, name, st.session_state.difficulty_level
            )
            st.session_state.question_text = q
            st.session_state.correct_answer = a
            st.session_state.asked_questions.append(q)
            st.session_state.answered = False
            st.rerun()

# ---------------- EARLY EXIT: if all reflections done, show summary ----------------
if len(st.session_state.all_reflections) >= MAX_QUESTIONS:
    show_and_log_final_summary()

# ---------------- QUESTION ----------------
if "user_id" in st.session_state and not st.session_state.answered:
    st.subheader(f"📌 Question {st.session_state.question_count} of {MAX_QUESTIONS}")
    st.write(st.session_state.question_text)

    answer = st.text_input("Your Answer")
    if st.button("Submit Answer"):
        # Evaluate answer
        try:
            student_ans = str(answer).strip().lower()
            correct_ans = str(st.session_state.correct_answer).strip().lower()
            correct_bool = student_ans == correct_ans
        except Exception:
            correct_bool = False

        st.session_state.correct_bool = correct_bool

        # Adjust simple difficulty on correct
        if correct_bool:
            st.session_state.correct_streak += 1
            st.session_state.difficulty_level = min(10, st.session_state.difficulty_level + 1)
        else:
            st.session_state.correct_streak = 0

        # Log the question attempt
        qid = log_question(
            st.session_state.user_id,
            st.session_state.question_text,
            answer,
            correct_bool
        )
        st.session_state.question_id = qid

        # Motivation (send name too)
        motivation_msg = generate_motivation(answer, correct_bool, st.session_state.name)
        st.write("✅ Correct!" if correct_bool else f"❌ Incorrect. Correct answer was: {st.session_state.correct_answer}")
        st.write(motivation_msg)

        st.session_state.answered = True

# ---------------- REFLECTION AFTER EVERY QUESTION ----------------
if st.session_state.get("answered", False):
    # Reflection form (one per question)
    with st.form(f"reflection_form_{st.session_state.question_count}"):
        reflection = st.text_area("What did you learn from this question?")
        emoji = st.selectbox("Your emotion",emoji_map , key=f"emoji_{st.session_state.question_count}")
        confidence = st.slider("Confidence (0-100%)", 0, 100, 50, key=f"confidence_{st.session_state.question_count}")
        submit_reflection = st.form_submit_button("Submit Reflection")

    if submit_reflection:
        # Save reflection to DB
        log_feedback(
            st.session_state.question_id,
            reflection,
            emoji,
            confidence
        )

        # Save reflection in session (CANONICAL record)
        st.session_state.all_reflections.append({
            "question": st.session_state.question_text,
            "answer": st.session_state.correct_answer,
            "your_answer": bool(st.session_state.correct_bool),
            "reflection": reflection,
            "emotion": emoji,
            "confidence": confidence
        })

        # AI difficulty adjuster from reflection
        ai_result = adjust_difficulty_with_ai(
            reflection=reflection,
            last_problem=st.session_state.question_text,
            current_level=st.session_state.difficulty_level
        )
        st.session_state.difficulty_level = ai_result.get("new_difficulty", st.session_state.difficulty_level)

        # If we just finished the last reflection, go straight to summary
        if len(st.session_state.all_reflections) >= MAX_QUESTIONS:
            show_and_log_final_summary()

        # Otherwise, move to next question
        st.session_state.show_next = True
        st.rerun()

# ---------------- NEXT QUESTION ----------------
if st.session_state.get("show_next", False) and len(st.session_state.all_reflections) < MAX_QUESTIONS:
    # Generate new unique question
    for _ in range(8):
        q, a = generate_math_question(
            st.session_state.grade,
            st.session_state.topic,
            st.session_state.name,
            st.session_state.difficulty_level
        )
        if q and q not in st.session_state.asked_questions:
            st.session_state.asked_questions.append(q)
            break

    st.session_state.question_text = q
    st.session_state.correct_answer = a
    st.session_state.question_count += 1
    st.session_state.answered = False
    st.session_state.correct_bool = None
    st.session_state.show_next = False
    st.rerun()