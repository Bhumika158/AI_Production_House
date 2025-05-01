# import openai
# import os

# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def filter_by_audience(trends: list, audience: str, goal: str) -> str:
#     prompt = f"""
# You're an AI content strategist. Here are trending topics: {trends}
# The target audience is: {audience}
# The goal is: {goal}

# Pick the **best matching trend** that aligns with both the audience and the goal. Reply with ONLY the topic.
# """
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You're a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#     )
#     return response.choices[0].message.content.strip()

from utils.gemini_client import run_gemini

def filter_by_audience(trends: list, audience: str, goal: str) -> str:
    prompt = f"""
You're an AI content strategist. Here are trending topics: {trends}
The target audience is: {audience}
The goal is: {goal}

Pick the best matching trend and reply ONLY with the topic name.
"""
    return run_gemini(prompt)
