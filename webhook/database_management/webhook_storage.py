import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel
from pydantic_models import PingedWebhooks
from .webhook_errors import (
    WebhookEventNotFoundError, 
    WebhookEventHasNoURLsError, 
    WebhookUrlAlreadyExistsError, 
    WebhookUrlNotFoundError
    )
import requests



# Path to the JSON file for storing webhook data
STORAGE_FILE = Path(__file__).parent / "webhook_data.json"


def read(event: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Read the storage file and return the webhooks for a specific event or all events.

    Args:
        event (str | None): The event name to filter webhooks. If None, return all webhooks.

    Returns:
        data (Dict[str, List[str]]): 
            A dictionary where keys are event names and values are lists of webhook URLs.

    Raises:
        WebhookEventNotFoundError: If the specified event does not exist.
        WebhookEventHasNoURLsError: If the specified event has no registered URLs.
        FileNotFoundError: If the storage file does not exist.
        IOError: If there is an error reading the storage file or if the JSON data is invalid.
    """
    try:
        if STORAGE_FILE.exists():
            with STORAGE_FILE.open("r") as file:
                data: Dict[str, List[str]] = json.load(file)
                if event is not None and isinstance(event, str):
                    if event in data:
                        # Return only the specified event and its list of URLs
                        webhook_urls = data[event]
                        
                        if len(webhook_urls) <= 0:
                            raise WebhookEventHasNoURLsError(event)
                        filtered_data = {event: webhook_urls}
                        return filtered_data
                    else:
                        # Raise an error if the event does not exist
                        raise WebhookEventNotFoundError(event)
                return data  # Return all webhooks if no event is specified
        else:
            raise FileNotFoundError(f"The storage file at path: {STORAGE_FILE} does not exist.")
    except (json.JSONDecodeError, IOError) as e:
        raise IOError(f"Error reading storage file at path {STORAGE_FILE}: {e}")


def update(event: str, url: str) -> None:
    """
    Add a URL to a specific event in the storage file.

    Args:
        event (str): The event name to add the URL to.
        url (str): The webhook URL to add.

    Raises:
        WebhookEventNotFoundError: If the event does not exist in the storage file.
        WebhookUrlAlreadyExistsError: If the URL already exists for the event.
    """
    data: Dict[str, List[str]] = read()
    if event not in data:
        raise WebhookEventNotFoundError(event)
    if url in data[event]:
        raise WebhookUrlAlreadyExistsError(url, event)
    data[event].append(url)
    _write(data)


def remove(event: str, url: str) -> None:
    """
    Remove a URL from a specific event in the storage file.

    Args:
        event (str): The event name to remove the URL from.
        url (str): The webhook URL to remove.

    Raises:
        WebhookEventNotFoundError: If the event does not exist in the storage file.
        WebhookUrlNotFoundError: If the URL does not exist for the event.
    """
    data: Dict[str, List[str]] = read()
    if event not in data:
        raise WebhookEventNotFoundError(event)
    if url not in data[event]:
        raise WebhookUrlNotFoundError(url, event)
    data[event].remove(url)
    _write(data)


def send(data: Dict[str, List[str]], payload: Dict[str, Any]) -> PingedWebhooks:
    """
    Send a test payload to all registered webhooks for the given events.

    Args:
        data (Dict[str, List[str]]): A dictionary where keys are event names and values are lists of webhook URLs.
        payload (Dict[str, Any]): The payload to send to the webhooks.

    Returns:
        PingedWebhooks: A summary of successful and failed webhook calls.
    """
    pinged_webhooks = PingedWebhooks()

    for event, urls in data.items():
        # Add the event name to the payload
        payload_with_event = {"event": event, "data": payload}
        for url in urls:
            try:
                # Send the POST request
                response = requests.post(url, json=payload_with_event, headers={"Content-Type": "application/json"})

                if response.ok:
                    # Parse the JSON response or use an empty dictionary if parsing fails
                    try:
                        received_payload = response.json()
                    except json.JSONDecodeError:
                        received_payload = {}

                    # Add to successful webhooks
                    pinged_webhooks.successful_webhooks_count += 1
                    pinged_webhooks.successful_webhooks.append({
                        "event": event,
                        "url": url,
                        "payload": received_payload,
                        "status_code": response.status_code
                    })
                else:
                    # Add to failed webhooks for non-2xx status codes
                    pinged_webhooks.failed_webhooks_count += 1
                    pinged_webhooks.failed_webhooks.append({
                        "event": event,
                        "url": url,
                        "error": f"HTTP error: {response.reason}",
                        "status_code": response.status_code
                    })
            except requests.RequestException as e:
                # Handle network-related exceptions
                pinged_webhooks.failed_webhooks_count += 1
                pinged_webhooks.failed_webhooks.append({
                    "event": event,
                    "url": url,
                    "error": str(e),
                    "status_code": None  # No status code available for exceptions
                })

    return pinged_webhooks


def trigger_webhooks(event: str, payload: Union[dict, BaseModel]):
    """
    Trigger all webhooks subscribed to a specific event.

    This function sends a payload to all registered webhook URLs for a given event. 
    It reads the registered webhooks from the storage file and sends an HTTP POST request 
    to each URL associated with the specified event.

    Args:
        event (str): The name of the event for which webhooks should be triggered.
        payload (dict | BaseModel): The data to send to the webhooks. 
            If a Pydantic model is provided, it will be converted to a dictionary.

    Behavior:
        - The function reads the registered webhooks from the storage file.
        - It filters the webhooks for the specified event.
        - For each URL associated with the event, it sends an HTTP POST request with the payload.
        - The payload includes the event name and the provided data.

    Notes:
        - If the payload is a Pydantic model, it is converted to a dictionary using `model_dump()`.
        - The function logs the status code of each successful request and any errors encountered.

    Logs:
        - Logs a success message for each webhook triggered, including the URL, payload, and response status code.
        - Logs an error message for each failed webhook, including the URL and the error details.
    """
    # Convert payload to dict if it's a Pydantic model
    if isinstance(payload, BaseModel):
        payload = payload.model_dump()
    
    # Add the event type to the payload
    payload_with_event = {"event": event, "data": payload}
    
    data = read()
    
    for stored_event, urls in data.items():
        if stored_event == event:
                for url in urls:
                    try:
                        response = requests.post(url, json=payload_with_event, headers={"Content-Type": "application/json"})
                        print(f"Webhook triggered: {url} with payload {payload}. Response: {response.status_code}")
                    except Exception as e:
                        print(f"Failed to trigger webhook {url}: {e}")

    

def _write(data: Dict[str, List[str]]) -> None:
    """
    Write the updated data back to the storage file.

    Args:
        data (Dict[str, List[str]]): A dictionary where keys are event names and values are lists of webhook URLs.

    Raises:
        IOError: If there is an error writing to the storage file.
    """
    try:
        with STORAGE_FILE.open("w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error writing to storage file: {e}")