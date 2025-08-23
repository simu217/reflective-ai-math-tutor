from openai import OpenAI
import os
import json
from fastapi import FastAPI

app = FastAPI()


# include routers
# app.include_router(some_router)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def adjust_difficulty_with_ai(reflection, last_problem, current_level):
    """
    Uses OpenAI to analyze reflection and decide:
    - student sentiment
    - difficulty adjustment
    - motivational message
    """

    prompt = f"""
    You are an adaptive math tutor.

    Student Reflection: "{reflection}"
    Last Problem: "{last_problem}"
    Current Difficulty Level: {current_level} (1 = easiest, 10 = hardest)

    Please:
    1. Detect the student’s sentiment (confident, curious, confused, frustrated, bored, neutral).
    2. Suggest a new difficulty level (1-10).
    3. Give one short motivational teacher-like message.

    Respond ONLY in strict JSON format with keys:
    sentiment, new_difficulty, motivation.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful adaptive math tutor."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )

    raw_output = response.choices[0].message.content.strip()
    print("Raw AI Output:", raw_output)

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        parsed = {
            "sentiment": "neutral",
            "new_difficulty": current_level,
            "motivation": "Let’s keep going, you’re doing great!"
        }

    return parsed



def generate_motivation(student_answer, correctness,student):
    """
    Generates a motivational/appreciation message for *every* student answer.
    Uses student name, correctness, confidence, and reflection for personalization.
    """

    prompt = f"""
    You are a supportive and encouraging math tutor.

    Student details:
    - Name: {student}
    - Just answered: "{student_answer}"
    - Correctness: {"Correct ✅" if correctness else "Incorrect ❌"}


    Your task:
    - Give a short, kind motivational message.
    - Personalize it to the student (use their name occasionally).
    - Vary the tone so it doesn’t sound repetitive.
    - If the student is correct → celebrate progress and boost confidence.
    - If incorrect → gently encourage, remind them mistakes are part of learning.
    - If confidence is low → reassure and uplift.
    - If confidence is high but answer is wrong → motivate persistence with optimism.
    - Keep it short (1–2 sentences max).
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a supportive teacher."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )

    return response.choices[0].message.content.strip()




def analyze_reflections(all_reflections, name):
    """
    Takes a list of reflection dicts and returns one short overall summary
    including sentiment and suggestions.
    """
    reflections_text = "\n".join([f"- {r['reflection']}" for r in all_reflections])

    prompt = f"""
    You are Rachel, a kind, friendly tutor that young kids love. You are helping {name}, a Grade 1–4 student. 
    Here are {name}'s reflections on 10 math questions:
    {reflections_text}

    Please do the following:
    1. For each reflection, say if the feeling is happy, neutral, or a little sad (instead of 'positive/neutral/negative').
    2. Give a short overall summary (2-3 sentences) written in simple, friendly words that a child can understand. 
       - Celebrate what {name} did well with cheerful encouragement 🎉
       - Gently explain one way {name} can get even better
       - End with a motivating message to keep practicing, in a warm Rachel-like tone
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a supportive teacher."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error analyzing reflections:", e)
        return "Could not generate summary. Great effort!"