import json

def _get_base_url():
    """Get the base URL based on environment setting from config.py"""
    try:
        import config
        environment = getattr(config, "environment", "test")
        if environment == "prod":
            return "https://prod.hs1api.com"
        else:
            return "https://test.hs1api.com"
    except ImportError:
        # config.py doesn't exist, default to test
        return "https://test.hs1api.com"

baseUrl = _get_base_url()  # Henry Schein One base URL

def print_response(request_name, response):
    """
    Print formatted response information including status code and JSON body.
    
    Args:
        request_name (str): Name of the request being made
        response: Response object from requests library
    """
    print()
    print(request_name)
    print("status code: " + str(response.status_code))
    try:
        print(json.dumps(response.json(), indent=2))
    except (json.JSONDecodeError, ValueError):
        # If response is not valid JSON, just print the text
        print(response.text)

