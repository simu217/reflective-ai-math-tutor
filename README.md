# Reflective AI Math Tutor"

An adaptive AI-powered math tutoring platform that provides personalized guidance, reflection-based learning, and motivational feedback for students.  
Built with **FastAPI** (backend), **Streamlit** (frontend), **MongoDB** (database), and **Docker** for containerization.

## Features

- **Adaptive Learning:** Adjusts difficulty dynamically based on student reflections and performance.
- **Reflection Analysis:** Uses AI sentiment analysis to tailor motivational feedback.
- **Progress Tracking:** Stores user history, reflections, and emotional states to guide learning.
- **Fast & Interactive UI:** Built with Streamlit for a clean and responsive interface.
- **Secure APIs:** JWT authentication and CRUD APIs for user data and progress tracking.
- **Dockerized:** Run the entire stack (frontend + backend + MongoDB) with one command.

## Quick Start

1. Install Docker & Docker Compose
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Clone this repo:

   ```bash
   git clone https://github.com/simu217/reflective-ai-math-tutor.git

   ```

3. Environment Variables: Create a .env file in the root directory and configure:
   OPENAI_API_KEY=your_openai_api_key
   MONGO_URI=mongodb://mongo:27017

4. Run with Docker Compose

   docker-compose up --build

   Backend: Runs on http://localhost:8000
   Frontend: Runs on http://localhost:8501
   MongoDB: Runs inside Docker (default port 27017)

   cd reflective-ai-math-tutor

Author

Developed by Simarjit Kaur ✨

```

```
