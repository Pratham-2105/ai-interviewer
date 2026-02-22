import requests
import config as config

API_KEY = config.GEMINI_API_KEY

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}"


def generate_response(prompt):

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(URL, headers=headers, json=data)

    result = response.json()

    # Debug print (very important)
    if "candidates" not in result:

        print("\nFULL ERROR RESPONSE:\n")
        print(result)
        return "ERROR: Check terminal for details"

    return result["candidates"][0]["content"]["parts"][0]["text"]