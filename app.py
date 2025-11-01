#!/usr/bin/env python3
import os
import requests
from flask import Flask, render_template_string, request

# Africa's Talking credentials
AT_USERNAME = os.getenv("AT_USERNAME", "YOUR_AT_USERNAME")
AT_API_KEY = os.getenv("AT_API_KEY", "YOUR_AT_API_KEY")
AT_URL = "https://api.africastalking.com/version1/messaging"

app = Flask(__name__)

# 🧱 HTML dashboard (Bootstrap + inline)
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>TCC Bulk SMS</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: Arial; padding: 20px; background: #0f172a; color: white; }
h2 { color: #22c55e; text-align: center; }
form { max-width: 500px; margin: auto; background: #1e293b; padding: 20px; border-radius: 10px; }
input, textarea { width: 100%; padding: 10px; margin-top: 8px; border-radius: 5px; border: none; }
button { background: #22c55e; border: none; color: white; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
button:hover { background: #16a34a; }
p { text-align: center; }
</style>
</head>
<body>
  <h2>📨 TCC Bulk SMS</h2>
  <form method="post" action="/send">
    <label>Recipients (comma-separated)</label>
    <input type="text" name="recipients" placeholder="+234801..., +234802..." required>
    <label>Message</label>
    <textarea name="message" rows="4" placeholder="Type your SMS here..." required></textarea>
    <br>
    <button type="submit">🚀 Send SMS</button>
  </form>
  {% if result %}
  <p><b>Result:</b> {{ result }}</p>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML)

@app.route("/send", methods=["POST"])
def send_sms():
    recipients = request.form.get("recipients").replace(" ", "")
    message = request.form.get("message")

    headers = {
        "apiKey": AT_API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "username": AT_USERNAME,
        "to": recipients,
        "message": message
    }

    try:
        res = requests.post(AT_URL, headers=headers, data=data)
        return render_template_string(HTML, result=res.json())
    except Exception as e:
        return render_template_string(HTML, result=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
