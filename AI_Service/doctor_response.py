from dotenv import load_dotenv
import google.generativeai as genai
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold, StopCandidateException


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key for Google Generative AI is not set in the environment variables.")

genai.configure(api_key=api_key)



generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1000,
        "response_mime_type": "text/plain",
    }

safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }


doctor = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=f'You are a diabetes doctor. Do not entertain or answer any inappropriate questions. Only respond to inquiries related to health, patient reports, or diagnoses.',
        safety_settings=safety_settings
    )

def reset_chat_session():
    global chat_session_doctor
    chat_session_doctor = doctor.start_chat(history=[])
    
chat_session_doctor = doctor.start_chat(history=[])


def get_doc_response(user_text):
    try:
        doc_response = chat_session_doctor.send_message(user_text)
        return doc_response.text
    except StopCandidateException:
        return "I am sorry but I can't help you with that"
    
reset_chat_session()
