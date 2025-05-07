from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import List, Dict, Any

class WebhookRequest(BaseModel):
    event: str = Field(
        default=..., 
        description="The event name for the webhook. Must be a valid identifier (e.g., '').",
        example=""
    )
    url: HttpUrl = Field(
        default=..., 
        description="The URL to send the webhook to. Must be a valid HTTP or HTTPS URL.",
        example="http://example.com/webhook1"
    )
    
    @field_validator("event")
    def validate_event(cls, value: str) -> str:
        """
        Validate the event name to ensure it is lowercase and contains only valid characters.
        Converts any uppercase letters to lowercase.
        """
        # Convert to lowercase
        value = value.lower()

        # Ensure the event name contains only alphanumeric characters and underscores
        if not value.isidentifier():
            raise ValueError("Event name must be a valid identifier (alphanumeric and underscores only).")

        return value

class WebhookResponse(BaseModel):
    message: str = Field(..., example="Webhook registered successfully")
    url: HttpUrl = Field(..., example="http://example.com/webhook1")
    event: str = Field(..., example="")


class Webhook(BaseModel):
    event: str = Field(..., example="")
    urls: List[str] = Field(..., example=["http://example.com/webhook1", "http://example.com/webhook2"])

class RegisteredWebhooksResponse(BaseModel):
    webhooks: List[Webhook]


class PingedWebhooks(BaseModel):
    successful_webhooks_count: int = Field(
        default=0, 
        description="The number of webhooks that were successfully pinged and returned a 2xx status code.", 
        examples=[2]
    )
    
    successful_webhooks: List[Dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "A list of successfully pinged webhooks. Each entry contains the event name, "
            "the URL of the webhook, the payload response (if any), and the HTTP status code."
        ),
        example=[
            {
                "event": "", 
                "url": "http://example.com/webhook1", 
                "payload_response": {"message": "Webhook received successfully"}, 
                "status_code": 200
            },
            {
                "event": "", 
                "url": "http://example.com/webhook2", 
                "payload_response": {}, 
                "status_code": 200
            }
        ]
    )
    
    failed_webhooks_count: int = Field(
        default=0, 
        description="The number of webhooks that failed to be pinged due to HTTP errors or network issues.", 
        examples=[2]
    )
    
    failed_webhooks: List[Dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "A list of webhooks that failed to be pinged. Each entry contains the event name, "
            "the URL of the webhook, an error message describing the failure, and the HTTP status code (if available). "
            "If the failure was due to a network issue, the status code will be None."
        ),
        example=[
            {
                "event": "", 
                "url": "http://example.com/webhook3", 
                "error": "HTTP error: Not Found", 
                "status_code": 404
            },
            {
                "event": "", 
                "url": "http://nonexistent.example.com/webhook", 
                "error": "Connection refused", 
                "status_code": None
            }
        ]
    )


class PingResponse(PingedWebhooks):
    message: str = Field(..., example="Ping completed for all events")
    