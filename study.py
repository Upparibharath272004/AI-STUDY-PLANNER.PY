import openai
import datetime
import json

# Replace with your actual OpenAI API key
OPENAI_API_KEY = AIzaSyCAxJ9fJFPR_-dKqsCqAFz2B-a6fDZW44c
  # Replace with your actual key

def generate_study_plan(topic: str, duration_days: int, hours_per_day: float, existing_knowledge: str = "", target_difficulty: str = "beginner") -> dict | str:
    """
    Generates a study plan for a given topic using the OpenAI API.

    Args:
        topic (str): The subject to be studied.
        duration_days (int): The number of days allocated for studying.
        hours_per_day (float):  The number of hours dedicated to studying each day.
        existing_knowledge (str, optional):  A brief description of the user's existing knowledge of the topic. Defaults to "".
        target_difficulty (str, optional):  The desired level of study (e.g., "beginner", "intermediate", "advanced"). Defaults to "beginner".

    Returns:
        dict: A dictionary representing the study plan, or None if an error occurred.  Each key represents a day, and the value is a list of study activities for that day.
        str: If an error occurred, it returns an error message.
    """

    openai.api_key = OPENAI_API_KEY

    prompt = f"""
You are a study plan generator. Your task is to create a structured study plan for a given topic.

Topic: {topic}
Duration: {duration_days} days
Hours per day: {hours_per_day}
Existing Knowledge: {existing_knowledge if existing_knowledge else "None"}
Target Difficulty: {target_difficulty}

Instructions:

1.  Break down the topic into smaller, manageable subtopics or modules.
2.  Allocate specific subtopics or modules to each day of the study plan.
3.  For each day, suggest specific activities to perform, such as:
    *   Reading chapters or articles
    *   Watching lectures or videos
    *   Solving practice problems
    *   Taking notes
    *   Doing research
    *   Working on projects
    *   Reviewing previous material
4.  Provide realistic time estimates for each activity, ensuring the total time for each day does not exceed the specified hours per day.
5.  The activities should be adjusted for the existing knowledge and target difficulty of the user.  If the user has no existing knowledge and the difficulty is beginner, start with very basic introductory material.  If the user has considerable existing knowledge and the difficulty is advanced, focus on more complex and challenging material.
6.  Provide the study plan in JSON format. The JSON should have the following structure:

    ```json
    {{
      "Day 1": ["Activity 1 (estimated time)", "Activity 2 (estimated time)", ...],
      "Day 2": ["Activity 1 (estimated time)", "Activity 2 (estimated time)", ...],
      ...
      "Day {duration_days}": ["Activity 1 (estimated time)", "Activity 2 (estimated time)", ...]
    }}
    ```

7. Ensure activities are specific and actionable.

Example:
```json
{{
  "Day 1": ["Introduction to Python (1 hour)", "Setting up your Python environment (30 minutes)", "Basic data types and variables (1.5 hours)"],
  "Day 2": ["Control flow: if/else statements (1 hour)", "Loops: for and while loops (1.5 hours)", "Practice problems on control flow and loops (1 hour)"],
  "Day 3": ["Functions: defining and calling functions (1.5 hours)", "Scope and lifetime of variables (1 hour)", "Practice problems on functions (1 hour)"]
}}
"""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003", # Choose the appropriate engine
            prompt=prompt,
            max_tokens=1024,  # Adjust as needed
            n=1,
            stop=None,
            temperature=0.7, # Adjust for creativity vs. predictability
        )

        plan_text = response.choices[0].text.strip()

        try:
            study_plan = json.loads(plan_text)
            return study_plan
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}\nRaw text from OpenAI: {plan_text}"
        except Exception as e:
             return f"An unexpected error occurred after receiving the JSON response: {e}"

    except openai.error.OpenAIError as e:
        return f"OpenAI API error: {e}"
    except Exception as e:
        return f"An unexpected error occurred during the API call: {e}"

# Example Usage:
if __name__ == "__main__":
    topic = "Quantum Mechanics"
    duration_days = 5
    hours_per_day = 3.5
    existing_knowledge = "Some basic physics knowledge."
    target_difficulty = "intermediate"

    study_plan = generate_study_plan(topic, duration_days, hours_per_day, existing_knowledge, target_difficulty)

    if isinstance(study_plan, str):
        print(f"Error: {study_plan}")
    else:
        print("\nStudy Plan:")
        for day, activities in study_plan.items():
            print(f"\n{day}:")
            for activity in activities:
                print(f"- {activity}")