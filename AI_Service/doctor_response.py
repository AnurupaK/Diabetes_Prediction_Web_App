from dotenv import load_dotenv
import google.generativeai as genai
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold, StopCandidateException


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key for Google Generative AI is not set in the environment variables.")

genai.configure(api_key=api_key)

def Doc_instruction(outcome,glucose,bp,insulin,bmi,age):
    system_instruction = (
        f"You are a diabetes doctor. Do not entertain or answer any inappropriate questions. Only respond to inquiries related to health, patient reports, or diagnoses."
        f"Review the following patient data for analysis: Glucose: {glucose} mg/dL, Blood Pressure: {bp} mm Hg, "
        f"Insulin: {insulin} µIU/mL, BMI: {bmi} kg/m², Age: {age} years. Diagnosis: {outcome}. "
        f"Provide a brief three short points report focusing on the implications of these results, including insights into the patient's condition and  advice on health management strategies. "
        
    )
      
    return system_instruction


def initialize_models(doctor_instruction):
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
        system_instruction=f'{doctor_instruction}',
        safety_settings=safety_settings
    )

   
    return doctor


# Initialize models globally
doctor = initialize_models(" ")

chat_session_doctor = doctor.start_chat(history=[])


def get_doc_response(user_text):
    try:
        doc_response = chat_session_doctor.send_message(user_text)
        return doc_response.text
    except StopCandidateException:
        return "I am sorry but I can't help you with that"


def reset_chat_session():
    global chat_session_doctor
    chat_session_doctor = doctor.start_chat(history=[])


def update_model(doctor_instruction):
    global doctor
    doctor = initialize_models(doctor_instruction)
    reset_chat_session()

