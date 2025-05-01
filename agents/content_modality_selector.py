from utils.gemini_client import run_gemini

def suggest_modalities(trend: str, audience: str = "", goal: str = "") -> list:
    context = f"A trend: {trend}. Target audience: {audience}. Goal: {goal}." if audience or goal else f"A trend: {trend}."
    prompt = f"""
Based on the following context:

{context}

Suggest the top 3 suitable content formats for this topic. Choose from: Blog, Twitter Thread, LinkedIn Post, YouTube Video Script, Audio Podcast, Instagram Reel. Reply as a list.
"""
    response = run_gemini(prompt)
    return [line.strip("-• ") for line in response.splitlines() if line.strip()]
