import requests
import util

organizationId = "<organizationId>" # Replace <organizationId> with your organization ID

# THESE VALUES SHOULD BE KEPT SECRET!
# Move them to a protected file and don't push them up to a repository
clientId = "<clientId>" # Replace <clientId> with your client ID
clientSecret = "<clientSecret>" # Replace <clientSecret> with your client secret

# Configurable parameters for the aging balances request
locationId = "<locationId>"  # Replace <locationId> with your location ID
patientId = "<patientId>"   # Replace <patientId> with your patient ID


def getAccessToken():
    url = "https://prod.hs1api.com/oauth/client_credential/accesstoken?grant_type=client_credentials"
    headerData = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": clientId,
        "client_secret": clientSecret
    }
    response = requests.post(url, data=body, headers=headerData)
    util.printResponse("getAccessToken", response)
    responseJSON = response.json()

    return responseJSON["token_type"] + " " + responseJSON["access_token"]


def getAgingBalancesReport(headerData, locationId, patientId):
    """
    Get aging balances report asynchronously with location and patient filters
    """
    url = util.baseUrl + "/beta/agingbalances/reportasync"
    params = {
        "filter": f"location.id=={locationId},patient.id->[{patientId}]"
    }
    
    response = requests.get(url, params=params, headers=headerData)
    util.printResponse("getAgingBalancesReport", response)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching aging balances report: {response.status_code}")
        
    return response.json()


def main():
    print("="*70)
    print("AGING BALANCES REPORT EXAMPLE")
    print("="*70)
    
    # Get access token
    accessToken = getAccessToken()
    # Create header data with access token and organization id
    headerData = {
        "Authorization": accessToken,
        "Organization-ID": organizationId,
        "Content-Type": "application/json"
    }

    # Make the aging balances request
    print("\n" + "-"*50)
    print("GET AGING BALANCES REPORT")
    print("-"*50)
    print(f"URL: /beta/agingbalances/reportasync?filter=location.id=={locationId},patient.id={patientId}")
    print(f"Location ID: {locationId}")
    print(f"Patient ID: {patientId}")
    
    try:
        result = getAgingBalancesReport(headerData, locationId, patientId)
        print("✓ Aging balances report request successful")
    except Exception as e:
        print(f"✗ Aging balances report request failed: {e}")
        print("This might indicate:")
        print("- Invalid location ID or patient ID")
        print("- API access issues")
        print("- Organization configuration problems")

    print("\n" + "="*70)
    print("AGING BALANCES REPORT EXAMPLE COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()
