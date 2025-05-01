# # whatsapp_poster.py

# import requests
# import os
# from dotenv import load_dotenv
# from get_public_url import upload_to_transfersh

# load_dotenv() 

# def send_whatsapp_audio(recipient_number: str, audio_url: str, access_token: str, phone_number_id: str):
#     """
#     Send an audio file via WhatsApp using Meta's WhatsApp Business Cloud API.

#     Args:
#         recipient_number (str): The recipient's phone number in international format, e.g., '+919999999999'
#         audio_url (str): The publicly accessible URL of the audio file
#         access_token (str): Your WhatsApp Cloud API access token
#         phone_number_id (str): Your WhatsApp Business Phone Number ID

#     Returns:
#         dict: API response from WhatsApp
#     """
#     endpoint = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "messaging_product": "whatsapp",
#         "to": recipient_number,
#         "type": "audio",
#         "audio": {
#             "link": audio_url
#         }
#     }

#     response = requests.post(endpoint, json=payload, headers=headers)

#     try:
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.HTTPError as e:
#         return {"error": str(e), "response": response.text}

# # Optional: Test it standalone
# if __name__ == "__main__":
#     resp = send_whatsapp_audio(
#         recipient_number=os.getenv("TEST_RECIPIENT_PHONE"),
#         audio_url=upload_to_transfersh("output_audio.mp3"),
#         access_token=os.getenv("WHATSAPP_TOKEN"),
#         phone_number_id=os.getenv("WHATSAPP_PHONE_ID")
#     )
#     print(resp)

# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()
# print("TOKEN from .env:", os.getenv("WHATSAPP_TOKEN"))

# def upload_audio_to_whatsapp(file_path, access_token, phone_number_id):
#     """Upload an audio file to WhatsApp and get media ID"""
#     url = f"https://graph.facebook.com/v22.0/{phone_number_id}/media"
#     headers = {"Authorization": f"Bearer {access_token}"}
#     files = {'file': (file_path, open(file_path, 'rb'), 'audio/mpeg')}
#     data = {'messaging_product': 'whatsapp'}

#     response = requests.post(url, headers=headers, files=files, data=data)
#     try:
#         response.raise_for_status()
#         return response.json()['id']
#     except requests.exceptions.HTTPError as e:
#         print("❌ Upload failed:", response.text)
#         return {"error": str(e), "response": response.text}


# def send_whatsapp_text_message(recipient_number, message_text, access_token, phone_number_id):
#     """Send a plain text WhatsApp message"""
#     url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "messaging_product": "whatsapp",
#         "to": recipient_number,
#         "type": "text",
#         "text": {"body": message_text}
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     try:
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.HTTPError as e:
#         print("❌ Text message failed:", response.text)
#         return {"error": str(e), "response": response.text}


# def send_whatsapp_audio_message(recipient_number, media_id, access_token, phone_number_id):
#     """Send a WhatsApp audio message using uploaded media_id"""
#     url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "messaging_product": "whatsapp",
#         "to": recipient_number,
#         "type": "audio",
#         "audio": {"id": media_id}
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     try:
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.HTTPError as e:
#         print("❌ Audio message failed:", response.text)
#         return {"error": str(e), "response": response.text}


# # === Optional Standalone Test ===
# if __name__ == "__main__":
#     access_token = os.getenv("WHATSAPP_TOKEN")
#     phone_number_id = os.getenv("WHATSAPP_PHONE_ID")
#     recipient_number = os.getenv("TEST_RECIPIENT_PHONE")
#     audio_path = "output_audio.mp3"
#     message_text = "🎧 Here's your AI-generated audio from the Production Studio!"
#     print("test with just message", send_whatsapp_text_message(recipient_number, message_text, access_token, phone_number_id))
#     media_id = upload_audio_to_whatsapp(audio_path, access_token, phone_number_id)
#     print("Uploaded media_id:", media_id)

#     if isinstance(media_id, str):
#         print("Sending message...")
#         print(send_whatsapp_text_message(recipient_number, message_text, access_token, phone_number_id))
#         print("Sending audio...")
#         print(send_whatsapp_audio_message(recipient_number, media_id, access_token, phone_number_id))
#     else:
#         print("❌ Upload failed, media ID not retrieved.")

import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv("WHATSAPP_TOKEN")
phone_number_id = os.getenv("WHATSAPP_PHONE_ID")
recipient_number = os.getenv("TEST_RECIPIENT_PHONE")
# audio_path = "output_audio.mp3"
# text_message = "🎧 Here's your AI-generated audio. Let me know what you think!"

def send_hello_world_template():
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    print("📤 Sending hello_world template...")
    r = requests.post(url, headers=headers, json=payload)
    print("✅ Template response:", r.status_code, r.text)


def upload_audio(file_path):
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/media"
    headers = {"Authorization": f"Bearer {access_token}"}
    files = {'file': (file_path, open(file_path, 'rb'), 'audio/mpeg')}
    data = {'messaging_product': 'whatsapp'}

    print("📤 Uploading audio file...")
    r = requests.post(url, headers=headers, files=files, data=data)
    try:
        r.raise_for_status()
        media_id = r.json()['id']
        print("✅ Uploaded media_id:", media_id)
        return media_id
    except Exception:
        print("❌ Upload failed:", r.text)
        return None


def send_text(message):
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "text",
        "text": {"body": message}
    }
    print("📤 Sending text...")
    r = requests.post(url, headers=headers, json=payload)
    print("✅ Text response:", r.status_code, r.text)


def send_audio(media_id):
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "audio",
        "audio": {"id": media_id}
    }
    print("📤 Sending audio...")
    r = requests.post(url, headers=headers, json=payload)
    print("✅ Audio response:", r.status_code, r.text)


# if __name__ == "__main__":
#     # Step 1: Send hello_world template
#     send_hello_world_template()

#     # Step 2: Wait for user confirmation (manual or time delay)
#     input("⏳ Waiting for user reply... Press Enter to continue once replied.")

#     # Step 3: Upload & send audio + message
#     media_id = upload_audio(audio_path)
#     if media_id:
#         send_text(text_message)
#         send_audio(media_id)

