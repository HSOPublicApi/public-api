def _get_config_value(key, default=None):
    """
    Try to load a value from config.py if it exists
    
    Args:
        key: The key to look for (e.g., 'clientId', 'clientSecret', 'environment')
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

def _get_base_url():
    """Get the base URL based on environment setting from config.py"""
    environment = _get_config_value("environment", "test")
    if environment == "prod":
        return "https://prod.hs1api.com"
    else:
        return "https://test.hs1api.com"

# Export the base URL
baseUrl = _get_base_url()  # Henry Schein One base URL (test or prod based on config)

def getClientId():
    """Get client ID from config.py"""
    return _get_config_value("clientId", "<clientId>")

def getClientSecret():
    """Get client secret from config.py"""
    return _get_config_value("clientSecret", "<clientSecret>")

