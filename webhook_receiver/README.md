# Webhook Receiver (FOR TESTING!!!!)

This is a simple FastAPI server that acts as a webhook receiver.  
It is used to test incoming webhook calls from the main Webhook Exposee project.

---

## ✅ Pre-requisites

Make sure both apps are running:

| App              | Command                                       | Port             |
| ---------------- | --------------------------------------------- | ---------------- |
| Main Webhook API | `poetry run uvicorn main:app --reload`        | `localhost:8000` |
| Receiver         | `poetry run uvicorn receiver:app --port 9000` | `localhost:9000` |

---

## 🚀 How to Use Postman to Test

### 🔹 1. Register Webhook

**Goal**: Tell the webhook API to send a webhook to your receiver.

- **Method**: `POST`
- **URL**: `http://localhost:8000/register`

#### Body:

1. Go to the `Body` tab
2. Select `raw`
3. Change format to `JSON`
4. Paste this JSON:

```json
{
  "event_type": "payment_received",
  "url": "http://localhost:9000/"
}
```

5. Click **Send**

✅ You should get a response:

```json
{
  "message": "Webhook registered for event 'payment_received'."
}
```

---

### 🔹 2. Simulate the Event

**Goal**: Trigger the webhook and make sure your receiver prints it.

- **Method**: `POST`
- **URL**: `http://localhost:8000/simulate-event`

#### Body:

```json
{
  "event_type": "payment_received"
}
```

Click **Send**

✅ Check the terminal where your `webhook_receiver` is running. You should see something like:

```
[2025-05-03 12:00:00] Webhook received: {'event': 'payment_received', 'data': 'Sample payload'}
```

---

### 🔹 3. Test `/ping`

**Goal**: Make sure a basic ping goes to all registered webhooks.

- **Method**: `GET`
- **URL**: `http://localhost:8000/ping`
- Click **Send**

✅ In your webhook receiver terminal, you'll see:

```
[2025-05-03 12:01:10] Webhook received: {'ping': 'hello'}
```

---

### 🔹 4. Unregister Webhook

**Goal**: Remove the webhook so your receiver no longer gets called.

- **Method**: `POST`
- **URL**: `http://localhost:8000/unregister`

#### Body:

```json
{
  "event_type": "payment_received",
  "url": "http://localhost:9000/"
}
```

Click **Send**

✅ You should get:

```json
{
  "message": "Webhook unregistered from event 'payment_received'."
}
```

Now if you simulate the event again, nothing should happen in your receiver terminal.

---
