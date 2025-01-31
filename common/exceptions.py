class KrakenAPIError(Exception):
    """Base class for all Kraken API errors"""
    pass

class KrakenAPIUnkownPairError(KrakenAPIError):
    """Raised when an unknown asset pair is encountered"""
    pass

class KrakenAPIConnectionError(KrakenAPIError):
    """Raised when there is a connection error with the Kraken API"""
    pass

class KrakenAPIRequestError(KrakenAPIError):
    """Raised when there is an error with the API request"""
    pass

class KrakenAPIResponseError(KrakenAPIError):
    """Raised when there is an error with the API response"""
    pass

class KrakenAPIAuthenticationError(KrakenAPIError):
    """Raised when there is an authentication error with the Kraken API"""
    pass

class KrakenAPIRateLimitError(KrakenAPIError):
    """Raised when the rate limit is exceeded for the Kraken API"""
    pass

class KrakenAPIInvalidInputError(KrakenAPIError):
    """Raised when there is invalid input provided to the Kraken API"""
    pass

class KrakenAPIPermissionError(KrakenAPIError):
    """Raised when there is a permission error with the Kraken API"""
    pass

class KrakenAPINotFoundError(KrakenAPIError):
    """Raised when a requested resource is not found in the Kraken API"""
    pass

class KrakenAPIInternalServerError(KrakenAPIError):
    """Raised when there is an internal server error with the Kraken API"""
    pass


