import os
import re
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save

load_dotenv()

def extract_spoken_lines(script: str) -> str:
    spoken_lines = []

    for line in script.splitlines():
        line = line.strip()

        # Skip lines that are clearly non-verbal cues (music, effects)
        if re.match(r"^\(.*?sound.*?\)$", line.lower()) or re.match(r"^\*+$", line):
            continue

        # Remove markdown, speaker tags, brackets, and parentheticals
        line = re.sub(r"\*\*|__|\*|_", "", line)  # remove markdown bold/italic
        line = re.sub(r"\[.*?\]|\(.*?\)", "", line)  # remove bracketed cues
        if ":" in line and re.match(r"^[A-Za-z]+:", line):
            line = line.split(":", 1)[1].strip()

        cleaned = line.strip()
        if cleaned:
            spoken_lines.append(cleaned)

    return " ".join(spoken_lines)

def create_audio_from_script(script: str, filename="output_audio.mp3"):
    spoken_text = extract_spoken_lines(script)
    try:
        client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        # voice_list = client.voices.get_all()
        # print("✅ Available Voices:\n")
        # for voice in voice_list.voices:
        #     print(f"🎙️ {voice.name} - ID: {voice.voice_id}")
        audio = client.generate(
            text=spoken_text,
            voice="Xb7hH8MSUJpSbSDYk0k2",
            model="eleven_monolingual_v1"
        )
        save(audio, filename)
        return filename
    except Exception as e:
        return f"[ElevenLabs Error] {e}"
    
