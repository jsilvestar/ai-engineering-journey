import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Groq Fitness API")

class WorkoutPlannerRequest(BaseModel):
    name: str =Field(min_length=2, max_length=50)
    goal: str = Field(
        description="The user's primary fitness goal."
    )
    experience: str
    days_per_week: int = Field(ge=1, le=7)
    equipment: str
    limitations: str = Field(default="", max_length=1000)

def generate_workout_plan(request: WorkoutPlannerRequest) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing GROQ_API_KEY in environment")

    client = Groq()
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    system_prompt = """
    You are an experienced fitness workout planning assistant.

    Generate a practical weekly workout plan based on the user's profile.

    Rules:
    1. Respect the user's fitness goal and experience level.
    2. Schedule exactly the requested number of workout days.
    3. Use only the available equipment.
    4. Keep each workout within the requested duration.
    5. Include warm-up, exercises, sets, reps and rest periods.
    6. Include recovery days.
    7. Respect injuries and physical limitations.
    8. Do not make medical diagnoses or claims.
    9. If limitations are provided, include a safety disclaimer.
    10. Return the plan in clear Markdown format.
    """

    user_prompt = f"""
    Create a personalized weekly workout plan.
    Name: {request.name}
    Fitness goal: {request.goal}
    Experience level: {request.experience}
    Workout days per week: {request.days_per_week}
    Available equipment: {request.equipment}
    Injuries or limitations: {request.limitations or "None provided"}

    Generate the complete weekly workout plan.
    """

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
        max_tokens=1000,
    )

    workoutplan = completion.choices[0].message.content
    if not workoutplan:
        raise HTTPException(status_code=502, detail="LLM returned an empty Finess Plan")

    return workoutplan.strip()

@app.post("/workout-plan")
def create_fitness_plan(request: WorkoutPlannerRequest):
    workout_plan = generate_workout_plan(request)
    return {
        "name": request.name,
        "goal": request.goal,
        "experience": request.experience,
        "days_per_week": request.days_per_week,
        "workout_plan": workout_plan
    }

@app.get("/")
def root():
    return {"message": "Groq Fitness API is running"}
