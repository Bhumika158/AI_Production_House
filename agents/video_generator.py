import os
import re
import cv2
import numpy as np
import ffmpeg
from PIL import Image

WIDTH, HEIGHT = 1280, 720
FPS = 2
os.makedirs("frames", exist_ok=True)

def parse_video_script(script: str) -> list:
    parsed = []
    pattern = r'\((\d+)-(\d+) seconds\)\s*(.*?):\s*(.*)'
    matches = re.findall(pattern, script, re.IGNORECASE)
    for match in matches:
        start = int(match[0])
        end = int(match[1])
        label = match[2].strip().lower()
        content = match[3].strip()
        if label == "visuals":
            continue  # Skip visuals completely from appearing in the video
        parsed.append({'start': start, 'end': end, 'label': label, 'content': content})
    return parsed

def create_text_overlay_frame(background_color, text):
    img = np.full((HEIGHT, WIDTH, 3), background_color, dtype=np.uint8)
    overlay = img.copy()

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    color = (255, 255, 255)
    thickness = 2
    line_spacing = 10

    def wrap_text(text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            size = cv2.getTextSize(test_line, font, font_scale, thickness)[0]
            if size[0] > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        return lines

    wrapped_lines = wrap_text(text, WIDTH - 100)
    total_text_height = len(wrapped_lines) * (cv2.getTextSize("A", font, font_scale, thickness)[0][1] + line_spacing)
    y_start = (HEIGHT - total_text_height) // 2

    for i, line in enumerate(wrapped_lines):
        text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
        text_x = (WIDTH - text_size[0]) // 2
        text_y = y_start + i * (text_size[1] + line_spacing)
        cv2.putText(overlay, line, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

    return overlay

def generate_video_frames(parsed_script: list):
    background_colors = [(40, 40, 80), (30, 60, 90), (50, 50, 100), (70, 40, 100)]
    frame_idx = [0]

    def save_frames(text, duration_sec, color_idx):
        num_frames = max(1, int(duration_sec * FPS))
        frame = create_text_overlay_frame(background_colors[color_idx % len(background_colors)], text)
        for _ in range(num_frames):
            cv2.imwrite(f"frames/frame_{frame_idx[0]:03d}.png", frame)
            frame_idx[0] += 1

    for idx, part in enumerate(parsed_script):
        duration = part['end'] - part['start']
        save_frames(part['content'].strip(), duration, idx)

def create_final_video(output_video="final_dynamic_video.mp4", music_file="assets/upbeat_music.mp3"):
    # Step 1: Create video from frames
    (
        ffmpeg
        .input("frames/frame_%03d.png", framerate=FPS)
        .output("temp_video.mp4", vcodec='libx264', pix_fmt='yuv420p')
        .run(overwrite_output=True)
    )

    # Step 2: Merge temp_video.mp4 + music.mp3
    input_video = ffmpeg.input("temp_video.mp4")

    if os.path.exists(music_file):
        input_audio = ffmpeg.input(music_file)

        (
            ffmpeg
            .output(
                input_video['v'],   # map only video stream
                input_audio['a'],   # map only audio stream
                output_video,
                vcodec='libx264',
                acodec='aac',
                audio_bitrate='192k',
                movflags='faststart',
                shortest=None  # tell ffmpeg to end at shorter one
            )
            .global_args('-shortest')
            .run(overwrite_output=True)
        )
    else:
        print("⚠️ No background music found, creating video without music.")
        (
            ffmpeg
            .output(input_video, output_video, vcodec='libx264')
            .run(overwrite_output=True)
        )

    # Step 3: Clean up frames
    os.remove("temp_video.mp4")
    for f in os.listdir("frames"):
        os.remove(os.path.join("frames", f))
    os.rmdir("frames")
    return output_video

# === Main Dynamic Execution ===

# if __name__ == "__main__":
#     # Example dynamic script input
#     script_text = """
#     Visuals: (Rapid cuts, dynamic transitions)

# (0-3 seconds) HOOK: Fast-paced montage of various tasks – emails piling up, spreadsheets overflowing, someone looking stressed at a computer. Text overlay: "Drowning in busywork?"

# (3-10 seconds) NARRATION (upbeat, energetic voice): "Stop letting mundane tasks steal your time! AI tools are here to automate the chaos. Imagine: emails automatically sorted, spreadsheets analyzed in seconds, social media posts scheduled effortlessly."

# (10-18 seconds) VISUALS: Screenshots/short video clips showcasing various AI tools in action (e.g., Grammarly correcting text, Zapier connecting apps, an AI writing tool generating content). Text overlays highlighting key features like "Automated Email Responses," "Smart Scheduling," "Data Analysis."

# (18-25 seconds) NARRATION: "From writing to scheduling to data analysis, AI handles the grunt work, freeing you to focus on what truly matters. Boost your productivity, cut down on stress, and reclaim your time."

# (25-28 seconds) VISUALS: A person smiling and relaxed, working on a laptop with a clean, organized desktop. Text overlay: "Reclaim Your Time!"

# (28-30 seconds) CTA: "Check out the link in the description for a list of top AI automation tools! #AI #Automation #Productivity"

# (Optional Sound effects: Upbeat background music throughout, short sound effects to emphasize transitions.)
#     """
    
#     parsed_script = parse_video_script(script_text)
#     generate_video_frames(parsed_script)
#     create_final_video()
#     print("✅ Final Dynamic Video Created: final_dynamic_video.mp4")