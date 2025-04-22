from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)

IPINFO_TOKEN = os.getenv('IPINFO_TOKEN')  # safer to use environment variables

@app.route('/')
def track():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    try:
        response = requests.get(f"https://ipinfo.io/{user_ip}?token={IPINFO_TOKEN}")
        location_data = response.json()
    except Exception as e:
        location_data = {"error": str(e)}

    print(f"New visitor: {user_ip}")
    print(f"Location info: {location_data}")

    # Save visitor info
    with open("visitors.txt", "a") as f:
        f.write(f"{user_ip} - {location_data}\n")

    return redirect("https://example.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
