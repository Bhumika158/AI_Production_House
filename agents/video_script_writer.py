from utils.gemini_client import run_gemini

def generate_video_script(trend: str, audience: str = "") -> str:
    prompt = f"""
Write a 30-second YouTube Short script for the trend: "{trend}".

**IMPORTANT FORMAT INSTRUCTIONS:**
- For each part (HOOK, NARRATION, CTA), specify timing at the beginning like: (start-end seconds) TYPE: Text
- Only include the spoken text (no visual descriptions inside narration or hook lines).
- Do not embed "(Visual: ...)" inside narration or hook.
- If you want to suggest visuals, list them separately after the script under a 'Suggested Visuals' section (optional).
- Keep the spoken text natural, energetic, and concise.

**Example Format:**
(0-3 seconds) HOOK: Your hook text here.
(3-10 seconds) NARRATION: Your narration text here.
(10-20 seconds) NARRATION: Continue narration here.
(25-30 seconds) CTA: Your call to action here.

Only output the script in this format.

Target Audience: {audience if audience else 'general tech-savvy audience'}
"""
    return run_gemini(prompt)
