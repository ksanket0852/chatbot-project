import os
import requests
import yaml
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load YAML config
try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    raise RuntimeError("config.yaml not found. Make sure it's in the project directory.")

# Load API secrets and config
API_KEY = os.getenv("GROQ_API_KEY")
API = config.get("API")
UI = config.get("UI")
ERRORS = config.get("ERRORS")

# Validate critical configs
if not API_KEY:
    raise RuntimeError(ERRORS["missing"]["api_key"])
if not API.get("URL"):
    raise RuntimeError(ERRORS["missing"]["api_url"])
if not API.get("MODEL"):
    raise RuntimeError(ERRORS["missing"]["model"])

API_URL = API["URL"]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_payload(prompt: str, model: str = API["MODEL"]) -> dict:
    """Construct the payload for the API request."""
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

def send_prompt(prompt: str) -> str:
    """Send prompt to Groq API and return the response."""
    try:
        response = requests.post(
            API["URL"],
            headers=HEADERS,
            json=get_payload(prompt)
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"{ERRORS['request']} {e}"
    except (KeyError, TypeError):
        return ERRORS["not_found"]
