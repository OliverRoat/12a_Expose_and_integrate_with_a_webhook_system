import requests

exposee_base_url = "https://exposee-webhook.loca.lt"
integrator_base_url = "https://7027-85-82-70-165.ngrok-free.app"

subscriptions = [
    {
        "event": "user_registered",
        "url": f"{integrator_base_url}/webhook"
    },
    {
        "event": "user_send_message",
        "url": f"{integrator_base_url}/webhook"
    }
]

for subscription in subscriptions:
    response = requests.post(
        f"{exposee_base_url}/webhook",
        json=subscription
    )
    if response.ok:
        print(f"Subscribed to {subscription['event']} successfully.")
    else:
        print(f"Failed to subscribe to {subscription['event']}: {response.text}")