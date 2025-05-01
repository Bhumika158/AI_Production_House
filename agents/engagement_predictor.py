from utils.gemini_client import run_gemini

def predict_engagement(storyline: str) -> float:
    prompt = f"""
You are an AI social media analyst. Analyze the following content and predict how engaging it will be on a scale from 1 to 10.

Content:
{storyline}

Respond with a single number only.
"""
    response = run_gemini(prompt)
    try:
        return float(response.strip())
    except ValueError:
        return 7.5  # fallback if parsing fails