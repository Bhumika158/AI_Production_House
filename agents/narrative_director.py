# import openai
# import os

# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def build_storyline(trend: str, format_type: str) -> str:
#     prompt = f"""
# Build a content story for the following trend: "{trend}" in the format: {format_type}.
# Include:
# - Hook
# - Insight
# - Value
# - CTA

# Use clear formatting.
# """
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a creative AI content writer."},
#             {"role": "user", "content": prompt}
#         ],
#     )
#     return response.choices[0].message.content.strip()

from utils.gemini_client import run_gemini

def build_storyline(trend: str, format_type: str) -> str:
    prompt = f"""
Build a content story for the following trend: "{trend}" in the format: {format_type}.
Include:
- Hook
- Insight
- Value
- CTA

Respond clearly formatted.
"""
    return run_gemini(prompt)
