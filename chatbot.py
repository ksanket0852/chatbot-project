# chatbot.py

from config import send_prompt, ERRORS # Reusing config logic
import requests
import json
import yaml


def chat_with_groq(prompt: str) -> str:
    """Send a prompt to the Groq API and return the chatbot's reply."""
    try:
        response = send_prompt(prompt)

        return response

    except requests.exceptions.RequestException as e:
        return f"{ERRORS['connection']}: {str(e)}"
    except (KeyError, json.JSONDecodeError):
        return ERRORS['parse']
