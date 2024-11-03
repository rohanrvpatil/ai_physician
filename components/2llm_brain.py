import os
from dotenv import load_dotenv
import re

load_dotenv(dotenv_path="../.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

import requests

def is_valid_medical_query(prompt):
    # Define a list of accepted question patterns
    accepted_patterns = [
        r"what are the (latest|best) treatments? for retinal blindness",
        r"how does (retinal blindness|blood flow) work\??",
        r"what is (retinal blindness|blood flow)?",
        r"can you explain (treatment|clinical trials) for retinal blindness\??",
        r"what are the symptoms of retinal blindness\??",
        r"how to improve blood flow\??",
        r"what research is being done on (retinal blindness|blood flow)\??",
        r"tell me about clinical trials for retinal blindness\??"
    ]
    
    # Check if prompt matches any of the accepted patterns
    return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in accepted_patterns)

def send_message_to_chatbot(gemini_api_key, prompt):
    if not is_valid_medical_query(prompt):
        return "I'm sorry, but I can only provide information about retinal blindness, blood flow, and related medical treatments. Please ask a specific question."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}"

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    },
                ],
            },
        ],
    }

    try:
        response = requests.post(url, json=body, headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            raise Exception(f"Failed to generate content: {response.text}")

        data = response.json()
        bot_response = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
        return bot_response

    except Exception as error:
        print("Error generating content:", error)
        raise

if __name__ == "__main__":
    api_key = GEMINI_API_KEY
    prompt_text = "What are the symptoms of retinal blindness"
    response = send_message_to_chatbot(api_key, prompt_text)
    print("Generated response:", response)
