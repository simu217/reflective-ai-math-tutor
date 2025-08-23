from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/reflectiveai")
client = MongoClient(MONGO_URI)
db = client["reflectiveai"]

# Collections
users_collection = db["users"]
questions_collection = db["questions"]
feedback_collection = db["feedback"]
performance_collection = db["performance"]

# ---------------- USER ----------------
def create_user(name, grade, topic):
    user = {
        "name": name,
        "grade": grade,
        "topic": topic,
        "created_at": datetime.utcnow()
    }
    result = users_collection.insert_one(user)
    return str(result.inserted_id)

# ---------------- QUESTIONS ----------------
def log_question(user_id, question, answer, correct):
    doc = {
        "user_id": user_id,
        "question": question,
        "answer": answer,
        "correct": correct,
        "timestamp": datetime.utcnow()
    }
    result = questions_collection.insert_one(doc)
    return str(result.inserted_id)

# ---------------- FEEDBACK ----------------
def log_feedback(question_id, reflection, emotion, confidence, user_id=None):
    doc = {
        "question_id": question_id,
        "user_id": user_id,  # optional but useful for queries
        "reflection": reflection,
        "emotion": emotion,
        "confidence": confidence,
        "timestamp": datetime.utcnow()
    }
    feedback_collection.insert_one(doc)

# ---------------- PERFORMANCE ----------------
def log_performance(user_id, topic, score, difficulty):
    """
    score: float (0.0 → 1.0, e.g. 0.8 for 8/10 correct)
    difficulty: int (difficulty level when quiz ended)
    """
    doc = {
        "user_id": user_id,
        "topic": topic,
        "score": score,
        "difficulty": difficulty,
        "timestamp": datetime.utcnow()
    }
    performance_collection.insert_one(doc)

# ---------------- QUERY PERFORMANCE ----------------
def get_recent_performance(user_id, limit=5):
    logs = (
        performance_collection
        .find({"user_id": user_id})
        .sort("timestamp", -1)
        .limit(limit)
    )
    return list(logs)

# ---------------- INDEXES (ensure once) ----------------
def ensure_indexes():
    """Create indexes for faster queries (safe to call multiple times)."""
    users_collection.create_index("name")
    questions_collection.create_index("user_id")
    feedback_collection.create_index([("question_id", 1), ("user_id", 1)])
    performance_collection.create_index("user_id")
