from fastapi import FastAPI, HTTPException, status

app = FastAPI()


from database_management import (
    update, 
    remove, 
    read,
    send,
    WebhookEventNotFoundError,
    WebhookUrlNotFoundError,
    WebhookUrlAlreadyExistsError
    )

from pydantic_models import (
    WebhookResponse, 
    WebhookRequest,
    PingResponse
)

# Register a webhook
@app.post("/register", response_model=WebhookResponse)
def register_webhook(webhook: WebhookRequest):
    """
    Register a new webhook for a specific event.

    This endpoint allows the integrator to register a webhook URL for a specific event. 
    The webhook will be triggered whenever the specified event occurs.

    Args:
        webhook (WebhookRequest): The webhook object containing the event name and URL.

    Returns:
        response (WebhookResponse): A success message indicating that the webhook was registered, 
        along with the event name and URL.

    Raises:
        HTTPException: 
            - 404: If the specified event does not exist.
            - 400: If the URL is already registered for the given event.
    """
    try:
        update(webhook.event, str(webhook.url))
        return WebhookResponse(
            message="Webhook registered successfully",
            url=webhook.url,
            event=webhook.event
        )
        
    except WebhookEventNotFoundError:
        raise HTTPException(status_code=404, detail=f"Event '{webhook.event}' not found")
    except WebhookUrlAlreadyExistsError:
        raise HTTPException(status_code=400, detail=f"Webhook URL '{webhook.url}' already exists for event '{webhook.event}'")
    
# Unregister a webhook
@app.post("/unregister", status_code=status.HTTP_204_NO_CONTENT)
def unregister_webhook(webhook: WebhookRequest):
    """
    Unregister a webhook for a specific event.

    This endpoint allows the integrator to remove a previously registered webhook URL 
    for a specific event. Once unregistered, the webhook will no longer be triggered 
    for the specified event.

    Args:
        webhook (WebhookRequest): The webhook object containing the event name and URL.

    Returns:
        response (None): Returns a 204 No Content status code on successful deletion.

    Raises:
        HTTPException: 
            - 404: If the specified event does not exist.
            - 404: If the URL is not registered for the given event.
    """
    try:
        return remove(webhook.event, str(webhook.url))
        
    except WebhookEventNotFoundError:
        raise HTTPException(status_code=404, detail=f"Event '{webhook.event}' not found")
    except WebhookUrlNotFoundError:
        raise HTTPException(status_code=404, detail=f"Webhook URL '{webhook.url}' not found for event '{webhook.event}'")


# Ping all webhooks
@app.get("/ping", response_model=PingResponse)
def ping_all_webhooks():
    """
    Ping all registered webhooks across all events.

    This endpoint sends a test payload to all registered webhooks for all events.
    It provides a summary of successful and failed webhook calls.

    Returns:
        response (PingResponse): A summary of the ping operation, including the number of successful and failed webhooks.

    Raises:
        HTTPException: 
            - 404: If no webhooks are registered for a queried event.
            - 404: If the specified event exists but has no registered URLs.
    """
    # Read webhooks from storage
    data = read()

    # Use the provided payload or fall back to the default payload
    payload = {"message": "Ping from Webhook Service"}

    # Send pings to the webhooks
    pinged_webhooks = send(data, payload)

    # Construct the response message
    message = "Pinged all registered webhooks successfully."
        

    # Return the PingResponse
    return PingResponse(
        message=message,
        **pinged_webhooks.model_dump()
    )

