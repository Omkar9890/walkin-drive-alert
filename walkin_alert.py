import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import date
import os

EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_RECEIVER = os.environ["EMAIL_RECEIVER"]

ROLES = [
    "Java",
    "Salesforce",
    "SQL",
    "Python",
    "Associate Software Engineer",
    "Software Engineer",
    "Data Engineer",
    "Data Analyst",
    "IT Fresher",
    "Graduate Engineer Trainee",
    "Fresher"
]

BASE_QUERY = "Walk in drive Bangalore fresher IT"

HEADERS = {"User-Agent": "Mozilla/5.0"}
results = []

for role in ROLES:
    query = f"{BASE_QUERY} {role}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    for g in soup.select(".tF2Cxc")[:4]:
        title = g.select_one("h3").text
        link = g.select_one("a")["href"]
        results.append(f"🔹 [{role}] {title}\n{link}\n")

if results:
    body = f"📅 Walk-in Drives – Bangalore ({date.today()})\n\n" + "\n".join(results)
else:
    body = "No walk-in drives found today."

msg = MIMEText(body)
msg["Subject"] = "Daily Walk-in Drives – Bangalore (Java | Salesforce | SQL | Python)"
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL_SENDER, EMAIL_PASSWORD)
server.send_message(msg)
server.quit()
