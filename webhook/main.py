from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import sqlite3
import requests

app = FastAPI()

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect("webhooks.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS webhooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        url TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Request body model
class WebhookRegistration(BaseModel):
    event_type: str
    url: HttpUrl

class EventSimulation(BaseModel):
    event_type: str

# Register a webhook
@app.post("/register")
def register_webhook(webhook: WebhookRegistration):
    conn = sqlite3.connect("webhooks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO webhooks (event_type, url) VALUES (?, ?)", (webhook.event_type, str(webhook.url)))
    conn.commit()
    conn.close()
    return {"message": f"Webhook registered for event '{webhook.event_type}'."}

# Unregister a webhook
@app.post("/unregister")
def unregister_webhook(webhook: WebhookRegistration):
    conn = sqlite3.connect("webhooks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM webhooks WHERE event_type = ? AND url = ?", (webhook.event_type, str(webhook.url)))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Webhook not found")
    conn.commit()
    conn.close()
    return {"message": f"Webhook unregistered from event '{webhook.event_type}'."}

# Ping all webhooks
@app.get("/ping")
def ping_all():
    conn = sqlite3.connect("webhooks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT url FROM webhooks")
    urls = cursor.fetchall()
    conn.close()

    results = []
    for (url,) in urls:
        try:
            response = requests.post(url, json={"ping": "hello"})
            results.append({"url": url, "status": response.status_code})
        except Exception as e:
            results.append({"url": url, "error": str(e)})
    return results

# Simulate an event
@app.post("/simulate-event")
def simulate_event(event: EventSimulation):
    conn = sqlite3.connect("webhooks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM webhooks WHERE event_type = ?", (event.event_type,))
    urls = cursor.fetchall()
    conn.close()

    if not urls:
        raise HTTPException(status_code=404, detail="No webhooks registered for this event")

    responses = []
    for (url,) in urls:
        try:
            response = requests.post(url, json={"event": event.event_type, "data": "Sample payload"})
            responses.append({"url": url, "status": response.status_code})
        except Exception as e:
            responses.append({"url": url, "error": str(e)})
    return responses
