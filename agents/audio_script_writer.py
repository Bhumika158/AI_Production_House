from utils.gemini_client import run_gemini

def generate_audio_script(trend: str, audience: str = "") -> str:
    prompt = f"""
Create a 60-second podcast audio script on "{trend}".
Make it conversational, engaging, and informative.
"""
    return run_gemini(prompt)
