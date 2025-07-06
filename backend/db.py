# backend/db.py

import os
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["math_tutor"]

# Define collections
users = db["users"]
questions = db["questions"]
feedback = db["feedback"]
performance = db["performance"]

# -----------------------
# USER OPERATIONS
# -----------------------

def create_user(name, grade_level):
    user = {
        "name": name,
        "grade_level": grade_level,
        "preferences": {},
        "created_at": datetime.datetime.utcnow()
    }
    return users.insert_one(user).inserted_id

def get_user_by_name(name):
    return users.find_one({"name": name})

def get_user_by_id(user_id):
    return users.find_one({"_id": user_id})

# -----------------------
# QUESTION OPERATIONS
# -----------------------

def log_question(user_id, question_text, answer_given, correct):
    entry = {
        "user_id": user_id,
        "question_text": question_text,
        "answer_given": answer_given,
        "correct": correct,
        "timestamp": datetime.datetime.utcnow()
    }
    return questions.insert_one(entry).inserted_id

def get_last_n_questions(user_id, n=5):
    return list(questions.find({"user_id": user_id}).sort("timestamp", -1).limit(n))

# -----------------------
# FEEDBACK OPERATIONS
# -----------------------

def log_feedback(question_id, reflection_text, emoji, confidence_level):
    entry = {
        "question_id": question_id,
        "reflection": reflection_text,
        "emoji": emoji,
        "confidence": confidence_level,
        "timestamp": datetime.datetime.utcnow()
    }
    return feedback.insert_one(entry).inserted_id

def get_feedback_by_question(question_id):
    return feedback.find_one({"question_id": question_id})

# -----------------------
# PERFORMANCE TRACKING
# -----------------------

def log_performance(user_id, topic, correct, emotion):
    entry = {
        "user_id": user_id,
        "topic": topic,
        "correct": correct,
        "emotion": emotion,
        "timestamp": datetime.datetime.utcnow()
    }
    return performance.insert_one(entry).inserted_id

def get_recent_performance(user_id, limit=10):
    return list(performance.find({"user_id": user_id}).sort("timestamp", -1).limit(limit))
