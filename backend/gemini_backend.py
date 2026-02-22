import requests
import config

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

    try:
        response = requests.post(URL, headers=headers, json=data)
    except Exception as e:
        return f"Connection Error: {str(e)}"

    if response.status_code != 200:
        print("Gemini API Error:", response.text)
        return f"API Error: {response.status_code}"

    try:
        result = response.json()
    except:
        return "Invalid JSON response from Gemini"

    if "candidates" not in result:
        print("\nFULL ERROR RESPONSE:\n")
        print(result)
        return "ERROR: No candidates returned"

    return result["candidates"][0]["content"]["parts"][0]["text"]