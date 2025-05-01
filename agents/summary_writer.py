from utils.gemini_client import run_gemini

def generate_summary(trend: str, audience: str = "", goal: str = "") -> str:
    prompt = f"Write a concise summary for the trend: {trend}."
    if audience:
        prompt += f" Tailor it for: {audience}."
    if goal:
        prompt += f" Goal: {goal}."
    return run_gemini(prompt)
