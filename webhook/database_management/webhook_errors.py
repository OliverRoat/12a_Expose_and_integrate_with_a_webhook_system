# Custom Exceptions for Webhook Storage Errors
class WebhookStorageError(Exception):
    """
    Base class for all webhook storage-related errors.
    """
    pass


class WebhookEventNotFoundError(WebhookStorageError):
    """
    Raised when the specified event does not exist in the storage file.
    """
    def __init__(self, event: str):
        super().__init__(f"Event '{event}' does not exist.")


class WebhookUrlAlreadyExistsError(WebhookStorageError):
    """
    Raised when the specified URL already exists for the given event.
    """
    def __init__(self, url: str, event: str):
        super().__init__(f"URL '{url}' already exists for event '{event}'.")


class WebhookUrlNotFoundError(WebhookStorageError):
    """
    Raised when the specified URL does not exist for the given event.
    """
    def __init__(self, url: str, event: str):
        super().__init__(f"URL '{url}' does not exist for event '{event}'.")

class WebhookEventHasNoURLsError(WebhookStorageError):
    """
    Raised when the event has no registered URLs.
    """
    def __init__(self, event: str):
        super().__init__(f"Event '{event}' has no registered URLs.")