from fastapi import FastAPI, Request
import datetime

app = FastAPI()

@app.post("/")
async def receive_webhook(request: Request):
    body = await request.json()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Webhook received: {body}")
    return {"status": "ok"}
