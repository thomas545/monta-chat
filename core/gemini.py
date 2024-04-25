import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


def call_gemini_model(prompt: str):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GOOGLE_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
    except Exception as exc:
        return {}

    return response.json()


def call_langchain_gemini(prompt: str):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        result = llm.invoke(prompt)
        return result.content
    except Exception as exc:
        return f"Error occurred while calling LLM: {str(exc)}"
