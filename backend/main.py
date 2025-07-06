# backend/main.py

from db import (
    create_user, get_user_by_name, log_question,
    log_feedback, log_performance, get_recent_performance
)
from content_generator import generate_math_question
from adaptive_logic import adjust_difficulty

def run():
    print("\n🎓 Welcome to Reflective AI Math Tutor 🎓\n")

    # Step 1: User Registration
    name = input("Enter your name: ")
    grade = input("Enter your grade level (e.g., Grade 4): ")
    topic = input("Enter a math topic (e.g., multiplication): ")

    user = get_user_by_name(name)
    if user:
        print(f"\n👋 Welcome back, {user['name']}!")
        user_id = user["_id"]
    else:
        user_id = create_user(name, grade)
        print(f"\n✅ New user created with ID: {user_id}")

    # Step 2: Adjust difficulty based on recent performance
    recent_logs = get_recent_performance(user_id, limit=5)
    difficulty = adjust_difficulty(recent_logs)
    print(f"\n📊 Difficulty adjustment based on performance: {difficulty}")

    # Step 3: Generate a GPT question
    question = generate_math_question(grade, topic)
    print(f"\n📘 Math Question: {question}")

    # Step 4: Collect user's answer
    answer = input("Your answer: ")
    correct_input = input("Was your answer correct? (y/n): ").strip().lower()
    correct = correct_input == 'y'

    # Step 5: Log the question
    question_id = log_question(user_id, question, answer, correct)

    # Step 6: Get reflection
    reflection = input("Why did you choose that answer? ")
    emoji = input("How do you feel? (😊 😕 😠 😐): ")
    confidence = input("Confidence level (low / medium / high): ")

    log_feedback(question_id, reflection, emoji, confidence)

    # Step 7: Log performance
    log_performance(user_id, topic, correct, emoji)

    # Step 8: Show performance history
    print("\n📊 Your Recent Performance:")
    logs = get_recent_performance(user_id)
    for log in logs:
        print(f"- [{log['timestamp']}] Topic: {log['topic']} | Correct: {log['correct']} | Emotion: {log['emotion']}")

if __name__ == "__main__":
    run()
