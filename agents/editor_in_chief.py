from utils.gemini_client import run_gemini

def finalize_content(storyline: str, score: float) -> str:
    prompt = f"""
Take the following content and finalize it for posting. Ensure it is polished, concise, and formatted clearly for social media. Append an engagement score at the end.

Content:
{storyline}

Engagement Score: {score}
"""
    return run_gemini(prompt)