import requests

BASE_URL = "https://codeforces.com/api"


def get_user_info(handle: str):
    url = f"{BASE_URL}/user.info?handles={handle}"

    response = requests.get(url)

    data = response.json()

    if data["status"] != "OK":
        raise Exception("Invalid handle")

    return data["result"][0]


def get_submissions(handle):
    url = f"{BASE_URL}/user.status?handle={handle}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    print("Status Code:", response.status_code)
    print("URL:", response.url)
    print("Response Preview:")
    print(response.text[:500])

    data = response.json()

    return data["result"]

def get_rating_history(handle):
    url = f"{BASE_URL}/user.rating?handle={handle}"

    response = requests.get(url)

    data = response.json()

    if data["status"] != "OK":
        raise Exception("Unable to fetch rating history")

    return data["result"]

def get_contest_history(handle):

    url = f"{BASE_URL}/user.rating?handle={handle}"

    response = requests.get(url)

    data = response.json()

    if data["status"] != "OK":
        raise Exception("Unable to fetch contest history")

    return data["result"]