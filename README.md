# Webhook Integrator Guide

Welcome! 👋 This guide will help you (the **integrator**) connect your own system to the Webhook Exposee project. By the end of this guide, you'll be able to register your webhook endpoint and receive event notifications like `payment_received` or `invoice_completed`.

---

## ✅ What You Need to Know

The webhook system supports:

- Registering your endpoint for specific event types
- Testing all webhooks using `/ping`
- Unregistering it when no longer needed

---

## 📦 Base URL

Your integrator base URL will be provided by the exposee (me) via an ngrok public URL.

**Example Base URL (you’ll be given a real one):**

```
https://a1b2c3d4.ngrok-free.app
```

Replace this with the actual URL provided to you before testing!

---

## 🧪 How to Test the Webhook System

### 🔹 1. Register Your Webhook

**Goal**: Register your server’s endpoint to receive event notifications.

- **Method**: `POST`
- **URL**: `https://e6c1-85-82-70-165.ngrok-free.app/register`

#### Body:

```json
{
  "event": "payment_received",
  "url": "https://my-custom-subdomain.loca.lt/webhook"
}
```

> Replace `event` with the event type you want to listen to (e.g., payment_received, payment_processed, etc.).  
> Replace `url` with your webhook receiver's public URL (e.g., https://my-custom-subdomain.loca.lt/webhook).

✅ You should get:

```json
{
  "message": "Webhook registered successfully",
  "url": "https://my-custom-subdomain.loca.lt/webhook",
  "event": "payment_received"
}
```

Repeat this step for any of the supported event types below:

- `payment_received`
- `payment_processed`
- `invoice_processing`
- `invoice_completed`

---

## 🔹 2. Register a Webhook with an Invalid URL (Optional)

**Goal**: Test how the system handles a failing webhook.

- **Method**: `POST`
- **URL**: `https://e6c1-85-82-70-165.ngrok-free.app/register`

### Body:

```json
{
  "event_type": "payment_received",
  "url": "https://this-needs-to-fail.lt/webhook"
}
```

✅ This webhook will register successfully but will fail during ping.

---

## 🔹 3. Ping All Registered Webhooks

**Goal**: Test if all registered webhooks respond correctly.

- **Method**: `GET`
- **URL**: `https://e6c1-85-82-70-165.ngrok-free.app/ping`

✅ Your valid webhook receiver should log this:

```json
{
  "message": "Ping from Webhook Service"
}
```

❌ For the invalid URL (like `https://this-needs-to-fail.lt/webhook`), you should see an error logged on the exposee side indicating the failure.

---

## 🔹 4. Unregister Your Webhook

**Goal**: Stop receiving events.

- **Method**: `POST`
- **URL**: `https://e6c1-85-82-70-165.ngrok-free.app/unregister`

### Body:

```json
{
  "event_type": "payment_received",
  "url": "https://my-custom-subdomain.loca.lt/webhook"
}
```

✅ You should get:

```json
{
  "message": "Webhook unregistered from event 'payment_received'."
}
```

Repeat this step for each registered webhook you want to remove.

---

## ✅ Supported Event Types

You can register for any of these:

- `payment_received`
- `payment_processed`
- `invoice_processing`
- `invoice_completed`

---

## 🛠️ Testing Workflow Summary

1. **Start the Webhook Service**  
   Run the exposee app and expose it using ngrok:  
   `https://e6c1-85-82-70-165.ngrok-free.app`

2. **Start the Webhook Receiver**  
   Run your webhook server and expose it using localtunnel (or ngrok):  
   `https://my-custom-subdomain.loca.lt`

3. **Register Webhooks**  
   Use the `/register` endpoint for each event you want to handle.

4. **Ping All Webhooks**  
   Use the `/ping` endpoint to test connectivity. Your receiver should print the payload.

5. **Unregister Webhooks**  
   Use the `/unregister` endpoint when done.

6. **Test an Invalid URL**  
   Register a bad URL and check that the ping fails correctly.

---
