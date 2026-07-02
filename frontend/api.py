import requests

BASE_URL = "http://127.0.0.1:8000"


def get_coach(handle):

    response = requests.get(
        f"{BASE_URL}/coach/{handle}"
    )

    if response.status_code == 200:
        return response.json()

    return None