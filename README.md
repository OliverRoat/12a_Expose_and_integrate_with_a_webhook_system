# Webhook Integrator Guide

Welcome! 👋 This guide will help you (the **integrator**) connect your own system to the Webhook Exposee project. By the end of this guide, you'll be able to register your webhook endpoint and receive event notifications like `payment_received` or `invoice_completed`.

---

## ✅ What You Need to Know

The webhook system supports:

- Registering your endpoint for specific event types
- Unregistering it when no longer needed
- Simulating an event to test delivery
- Testing all webhooks using `/ping`

---

## 📦 Base URL

Your integrator base URL will be provided by the exposee (me) via an ngrok public URL.

**Example Base URL (you’ll be given a real one):**

```
https://a1b2c3d4.ngrok-free.app
```

Replace this with the actual URL provided to you before testing!

---

## 🧪 How to Integrate Using Postman

### 🔹 1. Register Your Webhook

**Goal**: Register your server’s endpoint (e.g. `http://localhost:9000/`) to receive event notifications.

- **Method**: `POST`
- **URL**: `https://<ngrok-url>/register`

#### Body:

```json
{
  "event_type": "payment_received",
  "url": "http://localhost:9000/"
}
```

> Replace `event_type` with the type you want to listen to  
> Replace `url` with your own server’s webhook endpoint

✅ You should get:

```json
{
  "message": "Webhook registered for event 'payment_received'."
}
```

---

### 🔹 2. Simulate an Event

**Goal**: Trigger a test event and verify that your server receives the webhook.

- **Method**: `POST`
- **URL**: `https://<ngrok-url>/simulate-event`

#### Body:

```json
{
  "event_type": "payment_received"
}
```

✅ Your webhook server should receive:

```json
{
  "event": "payment_received",
  "data": "Sample payload"
}
```

---

### 🔹 3. Test `/ping`

**Goal**: Receive a basic test message at your webhook from the system.

- **Method**: `GET`
- **URL**: `https://<ngrok-url>/ping`

✅ Your webhook should receive:

```json
{
  "ping": "hello"
}
```

---

### 🔹 4. Unregister Your Webhook

**Goal**: Remove your endpoint from receiving notifications.

- **Method**: `POST`
- **URL**: `https://<ngrok-url>/unregister`

#### Body:

```json
{
  "event_type": "payment_received",
  "url": "http://localhost:9000/"
}
```

✅ You should get:

```json
{
  "message": "Webhook unregistered from event 'payment_received'."
}
```

---

## ✅ Supported Event Types

These are the valid event types you can subscribe to:

- `payment_received`
- `payment_processed`
- `invoice_processing`
- `invoice_completed`

---
