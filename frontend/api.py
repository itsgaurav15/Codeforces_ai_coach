import os

import requests
from dotenv import load_dotenv

load_dotenv()

# Points at the local backend by default; set BACKEND_URL to the deployed
# URL once the backend is hosted (e.g. https://your-app.onrender.com).
BASE_URL = os.getenv("BACKEND_URL", "https://codeforces-ai-coach.onrender.com")


def get_coach(handle):

    response = requests.get(
        f"{BASE_URL}/coach/{handle}",
        timeout=60,
    )

    if response.status_code == 200:
        return response.json()

    return None
