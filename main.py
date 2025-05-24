from fastapi import FastAPI
import requests
import time

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API is live"}

@app.post("/mail")
def create_temp_and_confirm():
    register_url = "https://api.mail.tm/accounts"
    domain = "dcpa.net"
    email = f"testuser{int(time.time())}@{domain}"
    password = "YourSecurePassword123!"

    payload = {"address": email, "password": password}
    res = requests.post(register_url, json=payload)
    if res.status_code != 201:
        return {"error": "Failed to create account"}

    account_data = res.json()
    token_res = requests.post("https://api.mail.tm/token", json=payload)
    token = token_res.json().get("token")

    if not token:
        return {"error": "Failed to get token"}

    headers = {"Authorization": f"Bearer {token}"}

    for _ in range(30):
        inbox_res = requests.get("https://api.mail.tm/messages", headers=headers)
        messages = inbox_res.json().get("hydra:member", [])

        for msg in messages:
            if msg["from"]["address"] == "noreply@magicloops.dev" and "Confirm your email" in msg["subject"]:
                message_id = msg["id"]
                message_detail_res = requests.get(f"https://api.mail.tm/messages/{message_id}", headers=headers)
                message_text = message_detail_res.json().get("text", "")

                lines = message_text.splitlines()
                confirm_link = ""
                for line in lines:
                    if "http" in line:
                        confirm_link = line.strip()
                        break

                if confirm_link:
                    click_res = requests.get(confirm_link)
                    return {
                        "email": email,
                        "confirm_link": confirm_link,
                        "confirm_status": click_res.status_code
                    }

        time.sleep(2)

    return {"status": "No MagicLoops confirmation mail received."}
