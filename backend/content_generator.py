# backend/content_generator.py

import openai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_math_question(grade_level, topic="basic operations"):
    prompt = f"""
    You are a friendly math tutor. Generate a math word problem suitable for a student in {grade_level}.
    Topic: {topic}. Do not provide the answer.
    Keep it concise and understandable.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        question = response['choices'][0]['message']['content'].strip()
        return question
    except Exception as e:
        return f"Error generating question: {str(e)}"
