def decide_posting_plan(modalities, video_path=None, audio_path=None, text_summary=None, storyline=None):
    plan = []

    for mode in modalities:
        if "YouTube Video Script" in mode and video_path:
            plan.append({
                "platform": "YouTube",
                "content_path": video_path,
                "content_type": "video",
                "title": "Generated AI Short 🎬",
                "description": "Automated by AI Production Studio."
            })
        
        if "Instagram Reel" in mode and video_path:
            plan.append({
                "platform": "Instagram",
                "content_path": video_path,
                "content_type": "video",
                "caption": "Your AI Reel is here! #AI #Reels"
            })

        if "LinkedIn Post" in mode and text_summary and storyline and video_path:
            combined_content = f"📄 Summary:\n{text_summary}\n\n📚 Storyline:\n{storyline}\n\n🎥 [Video Attached]"
            plan.append({
                "platform": "LinkedIn",
                "content_text": combined_content,
                "content_type": "text",
                "attachment_path": video_path
            })

        if "Blog" in mode and text_summary and storyline and video_path:
            combined_content = f"# Blog Post\n\n## Summary\n{text_summary}\n\n## Storyline\n{storyline}\n\n## Watch Video\n🎥 [Video Attached]"
            plan.append({
                "platform": "Medium",
                "content_text": combined_content,
                "content_type": "text",
                "attachment_path": video_path
            })

        if "Twitter Thread" in mode and text_summary:
            plan.append({
                "platform": "Twitter",
                "content_text": text_summary,
                "content_type": "text"
            })

        if "Audio Podcast" in mode or audio_path:
            combined_audio_content = f"🎧 AI Podcast Summary:\n{text_summary}\n\nStoryline:\n{storyline}"
            plan.append({
                "platform": "WhatsApp",
                "content_text": combined_audio_content,
                "content_type": "text",
                "attachment_path": audio_path
            })

    return plan
