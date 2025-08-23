# backend/content_generator.py

import os
from dotenv import load_dotenv
from openai import OpenAI  # ✅ NEW way (not `import openai`)

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Read API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env")

asked_questions = set()

# ✅ Correct client creation
client = OpenAI(api_key=api_key)
import random
def generate_math_question(grade, topic, student_name,difficulty):

    variation_prompts = [
        "math question simple numeric format like '23 + 4 = ?' or '9 - 5 = ?'.",
        "math question formatted like a mini puzzle or riddle.",
        "math question as a sequence or pattern that the student needs to complete.",
        "math question where the numbers are part of a short story involving animals or toys, different from previous questions",
        "math question with two steps required to solve but still numeric and simple.",
        "math question formatted as a word problem and numbers should be changed",
    ]
    variation_prompt = random.choice(variation_prompts)
    prompt = (
        f"Create {variation_prompt} of  {topic}  suitable for a grade {grade} student, "
        f"with a difficulty level of {difficulty}. "
        "Ensure the question matches the difficulty level provided. "
        "The answer must be a single numeric value (integer, decimal, or fraction), without any units, words, or explanations. "
        "Do NOT include any steps, hints, or reasoning—only the numeric final answer. "
        "Format your response exactly like this:\n"
        "Question: <question>\n"
        "Answer: <numeric_answer>"
        
        """Rules:
    - Output a single math problem in plain numeric format (no extra text).
    - Do NOT repeat any problem from this list of already asked questions:
      {list(asked_questions)[:10]}  # only pass recent 10 for context
    - Keep it short and clear."""

    )

    if student_name:
        prompt += f"\nThe student's name is {student_name} to make it more personalized."
    print("-==============================")
    print(prompt)
    print("-==============================")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # Slightly more creative
            max_tokens=100,    # Allow longer questions
        )

        content = response.choices[0].message.content.strip()
        print("ehlo",content)
        lines = content.splitlines()
        question = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("question:")), "Unknown question")
        answer = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("answer:")), "Unknown answer")

        return question, answer

    except Exception as e:
        print("OpenAI Error:", e)
        return "Error generating question", "unknown"






