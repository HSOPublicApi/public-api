import requests
import util

#usagereport doesn't use the organizationId, but all requests must have a valid in the organization-id header
organizationId = "<organizationId>" # Replace <organizationId> with your organization ID

#usagereport is directly tied to calls based on your credentials, not orgs that you call on behalf of your connection

# THESE VALUES SHOULD BE KEPT SECRET!
# Move them to a protected file and don't push them up to a repository
clientId = "<clientId>" # Replace <clientId> with your client ID
clientSecret = "<clientSecret>" # Replace <clientSecret> with your client secret


def getAccessToken():
    url = "https://prod.hs1api.com/oauth/client_credential/accesstoken?grant_type=client_credentials"
    headerData = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": clientId,
        "client_secret": clientSecret
    }
    response = requests.post(url, data=body, headers=headerData)
    util.printResponse("getAccessToken", response)
    
    if response.status_code != 200:
        raise Exception(f"Authentication failed: {response.status_code}. Please check your clientId and clientSecret.")
    
    responseJSON = response.json()
    return responseJSON["token_type"] + " " + responseJSON["access_token"]


def getUsageReport(headerData):
    """
    Get usage report with default behavior (no parameters)
    """
    url = util.baseUrl + "/v1/usagereport"
    
    response = requests.get(url, headers=headerData)
    util.printResponse("getUsageReport", response)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching usage report: {response.status_code}")
        
    return response.json()


def main():
    print("="*70)
    print("USAGE REPORT EXAMPLE")
    print("="*70)
    
    try:
        # Get access token
        accessToken = getAccessToken()
    except Exception as e:
        print(f"\n✗ Authentication failed: {e}")
        print("Please verify your clientId and clientSecret are correct.")
        return
    
    # Create header data with access token and organization id
    headerData = {
        "Authorization": accessToken,
        "Organization-ID": organizationId,
        "Content-Type": "application/json"
    }

    # Make the usage report request
    print("\n" + "-"*50)
    print("GET USAGE REPORT")
    print("-"*50)
    print("URL: /v1/usagereport")
    
    try:
        result = getUsageReport(headerData)
        print("✓ Usage report request successful")
    except Exception as e:
        print(f"✗ Usage report request failed: {e}")
        print("This might indicate:")
        print("- API access issues")
        print("- Organization configuration problems")

    print("\n" + "="*70)
    print("USAGE REPORT EXAMPLE COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()

