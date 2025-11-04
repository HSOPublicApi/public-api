import json
import requests

baseUrl = "https://prod.hs1api.com/ascend-gateway/api" # Henry Schein One base URL

def _is_placeholder(value):
    """Check if a value is a placeholder that needs to be replaced"""
    if not value or not isinstance(value, str):
        return False
    return value.strip().startswith("<") and value.strip().endswith(">")

def _get_config_value(key, default=None):
    """
    Try to load a value from config.py if it exists
    
    Args:
        key: The key to look for (e.g., 'clientId', 'clientSecret', 'organizationId')
        default: Default value if config.py doesn't exist or key not found
    
    Returns:
        The config value or default
    """
    try:
        import config
        return getattr(config, key, default)
    except ImportError:
        # config.py doesn't exist, return default
        return default
    except Exception:
        # Any other error, return default
        return default

def getConfigValue(value, configKey):
    """
    Get a configuration value, checking if the provided value is a placeholder.
    If it's a placeholder, load from config.py instead.
    
    Args:
        value: The value passed in (could be a placeholder like "<clientId>")
        configKey: The key to look for in config.py (e.g., 'clientId')
    
    Returns:
        The actual value to use (either the provided value or from config.py)
    """
    if _is_placeholder(value):
        configValue = _get_config_value(configKey)
        if configValue and not _is_placeholder(configValue):
            return configValue
        else:
            raise ValueError(
                f"Placeholder '{value}' detected but no valid value found in config.py for '{configKey}'. "
                f"Please either:\n"
                f"  1. Provide the value directly in your script, or\n"
                f"  2. Create config.py from config.py.example and fill in your credentials."
            )
    return value

def getAccessToken(clientId, clientSecret):
    """
    Get OAuth access token using client credentials
    
    Args:
        clientId: Your OAuth client ID (or "<clientId>" placeholder to load from config.py)
        clientSecret: Your OAuth client secret (or "<clientSecret>" placeholder to load from config.py)
    
    Returns:
        Authorization header value (e.g., "Bearer <access_token>")
    
    Raises:
        Exception: If authentication fails or credentials are missing
    """
    # Check for placeholders and load from config.py if needed
    clientId = getConfigValue(clientId, "clientId")
    clientSecret = getConfigValue(clientSecret, "clientSecret")
    
    url = "https://prod.hs1api.com/oauth/client_credential/accesstoken?grant_type=client_credentials"
    headerData = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": clientId,
        "client_secret": clientSecret
    }
    response = requests.post(url, data=body, headers=headerData)
    printResponse("getAccessToken", response)
    
    if response.status_code != 200:
        raise Exception(f"Authentication failed: {response.status_code}. Please check your clientId and clientSecret.")
    
    responseJSON = response.json()
    return responseJSON["token_type"] + " " + responseJSON["access_token"]

def getOrganizationId(organizationId):
    """
    Get organization ID, checking if the provided value is a placeholder.
    If it's a placeholder, load from config.py instead.
    
    Args:
        organizationId: The organization ID (or "<organizationId>" placeholder to load from config.py)
    
    Returns:
        The actual organization ID to use
    """
    return getConfigValue(organizationId, "organizationId")

def printResponse(requestName, response):
    print()
    print(requestName)
    print("status code: " + str(response.status_code))
    print(json.dumps(response.json(), indent = 2))