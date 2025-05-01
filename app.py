import streamlit as st
import concurrent.futures
import os

from agents.trend_hunter import fetch_trending_topics
from agents.audience_mapper import filter_by_audience
from agents.content_modality_selector import suggest_modalities
from agents.summary_writer import generate_summary
from agents.narrative_director import build_storyline
from agents.video_script_writer import generate_video_script
from agents.audio_script_writer import generate_audio_script
from agents.engagement_predictor import predict_engagement
from agents.editor_in_chief import finalize_content
from agents.video_generator import parse_video_script, generate_video_frames, create_final_video
from agents.audio_generator import create_audio_from_script
from agents.poster_agent import decide_posting_plan
from agents.poster import send_hello_world_template
from agents.poster import upload_audio, send_text, send_audio

# --- Initialize session state ---
if "content_ready" not in st.session_state:
    st.session_state.update({
        "content_ready": False,
        "modalities": [],
        "video_path": None,
        "audio_path": None,
        "summary": None,
        "storyline": None,
        "plan": [],
    })

st.set_page_config(page_title="AI Production Studio", layout="wide")
st.title("🎬 AI Production Studio")

niche = st.text_input("Enter your niche (optional)", "current trending topic")
audience = st.text_input("Target audience (optional)", "")
goal = st.text_input("Growth goal (optional)", "")

use_serpapi = st.checkbox("🔍 Use Real-Time Trends (Consumes API Calls)", value=True)

formats = st.multiselect(
    "Select content formats to generate",
    ["Summary", "Storyline", "Video Script", "Audio Script"],
    default=["Summary"]
)

if st.button("Generate Content"):
    st.subheader("🔥 Fetching Trends...")
    if use_serpapi and niche:
        raw_trends = fetch_trending_topics(niche)
    else:
        raw_trends = [
            "Zero-to-Hero AI Agents",
            "Open Interpreter",
            "Small Language Models",
            "AI Tools for Automation",
            "Latest AI in API Security"
        ]

    st.subheader("🎯 Matching to Audience/Goal...")
    relevant_trend = filter_by_audience(raw_trends, audience, goal)
    st.success(f"Selected Trend: {relevant_trend}")

    st.subheader("🧠 Suggesting Formats...")
    modalities = suggest_modalities(relevant_trend, audience, goal)
    st.session_state["modalities"] = modalities
    st.markdown(f"**Recommended Formats:** {', '.join(modalities)}")

    if "Summary" in formats:
        st.subheader("📄 Summary")
        summary = generate_summary(relevant_trend, audience, goal)
        st.session_state["summary"] = summary
        st.markdown(summary)

    if "Storyline" in formats:
        st.subheader("📚 Storyline")
        storyline = build_storyline(relevant_trend, modalities[0] if modalities else "LinkedIn Post")
        score = predict_engagement(storyline)
        final_post = finalize_content(storyline, score)
        st.session_state["storyline"] = final_post
        st.markdown(final_post)

    # --- Parallel Video/Audio ---
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_video = None
        future_audio = None

        left_output, right_output = st.columns(2)

        with left_output:
            if "Video Script" in formats:
                st.subheader("🎥 Video Script")
                video_script = generate_video_script(relevant_trend, audience)
                st.markdown(video_script)
                parsed_script = parse_video_script(video_script)
                generate_video_frames(parsed_script)
                with st.spinner("🎥 Generating video..."):
                    video_path = create_final_video()
                    st.session_state["video_path"] = video_path
                    if os.path.exists(video_path):
                        st.video(video_path)
                    else:
                        st.error(f"Video generation failed: {video_path}")

        with right_output:
            if "Audio Script" in formats:
                st.subheader("🎧 Audio Script")
                audio_script = generate_audio_script(relevant_trend, audience)
                st.markdown(audio_script)
                with st.spinner("🎧 Generating audio..."):
                    audio_path = create_audio_from_script(audio_script)
                    st.session_state["audio_path"] = audio_path
                    if os.path.exists(audio_path):
                        st.audio(audio_path)
                    else:
                        st.error(f"Audio generation failed: {audio_path}")

        

    st.session_state["content_ready"] = True

# --- Suggest Posting Plan ---
if st.session_state["content_ready"]:
    st.divider()
    show_posting_plan = st.checkbox("🚀 Show Suggested Posting Plan")

    if show_posting_plan:
        st.subheader("📝 Preview Your Posts")
        if not st.session_state["plan"]:
            # first time build plan
            st.session_state["plan"] = decide_posting_plan(
                st.session_state["modalities"],
                st.session_state["video_path"],
                st.session_state["audio_path"],
                st.session_state["summary"],
                st.session_state["storyline"],
            )

        approved_items = []
        for idx, item in enumerate(st.session_state["plan"]):
            with st.expander(f"📢 {item['platform']} Content Preview", expanded=True):
                if item['content_type'] == 'video':
                    st.video(item['content_path'])
                elif item['content_type'] == 'audio':
                    st.audio(item['content_path'])
                else:
                    st.markdown(item['content_text'])
                    if 'attachment_path' in item and item['attachment_path']:
                        if item['attachment_path'].lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                            st.video(item['attachment_path'])
                        elif item['attachment_path'].lower().endswith(('.mp3', '.wav', '.ogg')):
                            st.audio(item['attachment_path'])

                approve = st.checkbox(f"✅ Approve for posting on {item['platform']}", key=f"approve_{idx}")
                if approve:
                    approved_items.append(item)

        if approved_items:
            if st.button("🚀 Confirm and Post Approved Items"):
                st.success(f"Posting {len(approved_items)} approved content items! 🚀")
                send_hello_world_template()

                input("⏳ Waiting for user reply... Press Enter to continue once replied.")

                for item in approved_items:
                    if item["platform"] == "WhatsApp":
                        audio_path = item.get("attachment_path")
                        text_message = item.get("content_text")
                        if audio_path and text_message:
                            media_id = upload_audio(audio_path)
                            if media_id:
                                send_text(text_message)
                                send_audio(media_id)
        else:
            st.warning("⚡ Please approve at least one content piece to post.")