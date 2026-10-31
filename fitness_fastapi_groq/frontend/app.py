import os

from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()

API_URL = os.getenv(
    "WORKOUT_API_URL",
    "http://127.0.0.1:8000",
)
 
st.set_page_config(
    page_title="GROQ Workout Planner",
    page_icon="💪",
    layout="wide",
)

st.title("💪 GROQ Workout Planner")

st.write(
    "Create a personalized workout plan based on your goals, "
    "experience, equipment"
)

with st.form("workout_form"):

    st.subheader("1. Your Fitness Goals")
    name = st.text_input(
        "What is your Name",
    )
    goal = st.selectbox(
        "What is your primary fitness goal?",
        [
            "Build muscle",
            "Lose fat",
            "General fitness",
            "Improve endurance",
        ],
    )
    experience = st.selectbox(
        "What is your training experience?",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )

    st.subheader("2. Your Schedule")
    days_per_week = st.slider(
        "How many days can you train per week?",
        min_value=1,
        max_value=7,
        value=3,
    )

    st.subheader("3. Available Equipment")
    equipment = st.selectbox(
        "Where will you exercise?",
        [
            "No equipment",
            "Home dumbbells",
            "Full gym",
        ],
    )

    st.subheader("4. Limitations and Preferences")
    limitations = st.text_area(
        "Any injuries or exercise limitations? (Optional)",
        placeholder=(
            "Example: Avoid overhead pressing or "
            "exercises that aggravate my knees."
        ),
        max_chars=1000,
    )

    submitted = st.form_submit_button(
        "Generate My Workout Plan",
        type="primary",
        use_container_width=True,
    )



if submitted:
    if not name.strip():
    st.warning("Please enter your name.")
    st.stop()

    payload = {
        "name": name or "User",
        "goal": goal,
        "experience": experience,
        "days_per_week": days_per_week,
        "equipment": equipment,
        "limitations": limitations.strip(),
    }

    try:
        with st.spinner(
            "Creating your personalized workout plan..."
        ):
            response = requests.post(
                f"{API_URL}/workout-plan",
                json=payload,
                timeout=120,
            )

        if response.status_code == 200:
            result = response.json()
            plan = result.get("workout_plan", "")

            if not isinstance(plan, str) or not plan.strip():
                st.error(
                    "The AI returned an empty plan. Please try again."
                )
            else:
                st.session_state["workout_plan"] = plan
                st.session_state["workout_profile"] = payload

        elif response.status_code == 422:
           try:
                errors = response.json().get("detail", [])
                if isinstance(errors, list):
                    messages = [
                        error.get("msg", "Invalid input")
                        for error in errors
                    ]
                    st.warning("Please check your inputs: " + "; ".join(messages))
                else:
                    st.warning(str(errors))
            except ValueError:
                st.warning("Some inputs are invalid. Please check your form.")

        else:
            try:
                detail = response.json().get("detail")
            except ValueError:
                detail = None

            st.error(
                detail
                if isinstance(detail, str)
                else "Unable to generate your plan. Please try again."
            )

    except requests.exceptions.Timeout:
        st.error(
            "The request took too long. Please try again."
        )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to the workout service. "
            "Please check whether the backend is running."
        )

    except requests.exceptions.RequestException:
        st.error(
            "A network error occurred. Please try again."
        )

    except ValueError:
        st.error(
            "The server returned an invalid response."
        )


if st.session_state.get("workout_plan"):
    st.divider()

    st.subheader("Your Personalized Workout Plan")

    profile = st.session_state.get("workout_profile", {})

    st.caption(
        f"Goal: {profile.get('goal', '')} | "
        f"Experience: {profile.get('experience', '')} | "
        f"Training days: {profile.get('days_per_week', '')}"
    )

    st.markdown(st.session_state["workout_plan"])

    st.download_button(
        label="Download Workout Plan",
        data=st.session_state["workout_plan"],
        file_name="my_workout_plan.md",
        mime="text/markdown",
    )