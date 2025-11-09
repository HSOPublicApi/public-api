import requests
import util
from datetime import datetime, timedelta, timezone

organizationId = "<organizationId>" # Replace <organizationId> with your organization ID

# THESE VALUES SHOULD BE KEPT SECRET!
# Move them to a protected file and don't push them up to a repository
clientId = "<clientId>" # Replace <clientId> with your client ID
clientSecret = "<clientSecret>" # Replace <clientSecret> with your client secret


def getAppointmentsWithLastModified(headers, lastModifiedDate, pageSize=100):
    """
    Get appointments modified after a specific date (initial request using lastModified filter)
    
    Args:
        headers: Request headers with authorization
        lastModifiedDate: ISO 8601 date string (e.g., "2024-01-01T00:00:00.000Z")
        pageSize: Number of results per page (default: 100)
    
    Returns:
        JSON response containing appointments data
    """
    url = util.baseUrl + "/v1/appointments"
    params = {
        "pageSize": pageSize,
        "filter": f"lastModified>={lastModifiedDate}"
    }
    
    # Print the actual URL being called for debugging
    full_url = requests.Request('GET', url, params=params).prepare().url
    print(f"DEBUG: Full URL: {full_url}")
    
    response = requests.get(url, params=params, headers=headers)
    util.printResponse(f"getAppointmentsWithLastModified (lastModified>={lastModifiedDate})", response)
    
    if response.status_code != 200:
        print(f"ERROR: Request failed with status code {response.status_code}")
        return response.json()
    
    return response.json()


def getAppointmentsWithLastId(headers, lastId, pageSize=100, lastModifiedDate=None):
    """
    Get appointments using lastId for pagination (subsequent requests)
    
    Args:
        headers: Request headers with authorization
        lastId: The ID of the last appointment from the previous page
        pageSize: Number of results per page (default: 100)
        lastModifiedDate: Optional - include lastModified filter if continuing from initial request
    
    Returns:
        JSON response containing appointments data
    """
    url = util.baseUrl + "/v1/appointments"
    params = {
        "pageSize": pageSize,
        "lastId": lastId
    }
    
    # Optionally include lastModified filter if continuing from initial request
    if lastModifiedDate:
        params["filter"] = f"lastModified>={lastModifiedDate}"
    
    response = requests.get(url, params=params, headers=headers)
    
    if lastModifiedDate:
        util.printResponse(f"getAppointmentsWithLastId (lastId={lastId}, lastModified>={lastModifiedDate})", response)
    else:
        util.printResponse(f"getAppointmentsWithLastId (lastId={lastId})", response)
    
    if response.status_code != 200:
        print(f"ERROR: Request failed with status code {response.status_code}")
        return response.json()
    
    return response.json()


def getAllAppointmentsPaginated(headers, lastModifiedDate, pageSize=100, max_batches=10):
    """
    Get all appointments modified after a specific date by paginating through all pages
    
    Args:
        headers: Request headers with authorization
        lastModifiedDate: ISO 8601 date string (e.g., "2024-01-01T00:00:00.000Z")
        pageSize: Number of results per page (default: 100)
        max_batches: Maximum number of batches to fetch (default: 10, set to None for unlimited)
    
    Returns:
        List of all appointments retrieved
    """
    print("\n=== Getting ALL Appointments with Pagination ===")
    print(f"Using lastModified filter: lastModified>={lastModifiedDate}")
    print(f"Page size: {pageSize}")
    
    allAppointments = []
    lastId = None
    batchNumber = 1
    isFirstRequest = True
    
    while True:
        if max_batches and batchNumber > max_batches:
            print(f"\nReached maximum batch limit ({max_batches})")
            break
            
        print(f"\n--- Fetching batch {batchNumber} ---")
        
        if isFirstRequest:
            # Initial request: use lastModified filter
            print(f"Initial request with lastModified filter")
            responseData = getAppointmentsWithLastModified(headers, lastModifiedDate, pageSize)
            isFirstRequest = False
        else:
            # Subsequent requests: use lastId
            print(f"Subsequent request with lastId={lastId}")
            responseData = getAppointmentsWithLastId(headers, lastId, pageSize, lastModifiedDate)
        
        if responseData.get("statusCode") and responseData["statusCode"] != 200:
            print(f"Error fetching batch {batchNumber}: {responseData.get('statusCode')}")
            break
        
        # Check if we have data
        if not responseData.get("data") or len(responseData["data"]) == 0:
            print(f"No more appointments found (batch {batchNumber})")
            break
        
        currentBatch = responseData["data"]
        allAppointments.extend(currentBatch)
        print(f"Retrieved {len(currentBatch)} appointments in batch {batchNumber}")
        print(f"Total appointments so far: {len(allAppointments)}")
        
        # Check if we got fewer results than pageSize (indicates last page)
        if len(currentBatch) < pageSize:
            print(f"Received fewer results than pageSize ({len(currentBatch)} < {pageSize}), this is the last page")
            break
        
        # Get the last ID for the next request
        lastId = currentBatch[-1]["id"]
        print(f"Last ID in this batch: {lastId}")
        
        batchNumber += 1
    
    print(f"\n=== Pagination Complete ===")
    print(f"Total batches fetched: {batchNumber - 1}")
    print(f"Total appointments retrieved: {len(allAppointments)}")
    
    return allAppointments


def main():
    print("="*70)
    print("APPOINTMENTS PAGINATION EXAMPLE")
    print("="*70)
    print("This example demonstrates correct pagination using:")
    print("  1. lastModified filter on the initial request")
    print("  2. lastId parameter for subsequent requests")
    print("="*70)
    
    # Get access token (this will load from config.py if placeholders are used)
    accessToken = util.getAccessToken(clientId, clientSecret)
    # Get organization ID (this will load from config.py if placeholder is used)
    orgId = util.getOrganizationId(organizationId)
    # Create header data with access token and organization id
    headerData = {
        "Authorization": accessToken,
        "Organization-ID": orgId,
        "Content-Type": "application/json"
    }
    
    # Use a specific date for testing
    # You can adjust this to any date you want
    lastModifiedDate = "2016-07-08T16:54:13.657Z"
    
    print(f"\nUsing lastModified filter: lastModified>={lastModifiedDate}")
    print("(This will get appointments modified on or after this date)")
    
    # Example 1: Initial request with lastModified filter
    print("\n" + "-"*50)
    print("EXAMPLE 1: Initial Request (Using lastModified Filter)")
    print("-"*50)
    print(f"URL: /v1/appointments?pageSize=100&filter=lastModified>={lastModifiedDate}")
    
    try:
        firstBatch = getAppointmentsWithLastModified(headerData, lastModifiedDate, pageSize=100)
        print("✓ Initial request successful")
        
        # Example 2: Subsequent request using lastId
        if firstBatch.get("data") and len(firstBatch["data"]) > 0:
            lastId = firstBatch["data"][-1]["id"]
            print(f"\n" + "-"*50)
            print("EXAMPLE 2: Subsequent Request (Using lastId)")
            print("-"*50)
            print(f"URL: /v1/appointments?pageSize=100&lastId={lastId}&filter=lastModified>={lastModifiedDate}")
            print(f"Note: Including lastModified filter ensures we continue filtering by modification date")
            
            secondBatch = getAppointmentsWithLastId(headerData, lastId, pageSize=100, lastModifiedDate=lastModifiedDate)
            print("✓ Subsequent request successful")
            
            # Example 3: Show what happens if you forget the lastModified filter
            if secondBatch.get("data") and len(secondBatch["data"]) > 0:
                nextLastId = secondBatch["data"][-1]["id"]
                print(f"\n" + "-"*50)
                print("EXAMPLE 3: Common Mistake - Forgetting lastModified Filter")
                print("-"*50)
                print("WARNING: If you don't include the lastModified filter in subsequent requests,")
                print("you may get appointments that were modified BEFORE your initial date!")
                print(f"URL: /v1/appointments?pageSize=100&lastId={nextLastId}")
                print("(This example shows what NOT to do)")
                
                # This would be incorrect - no lastModified filter
                incorrectBatch = getAppointmentsWithLastId(headerData, nextLastId, pageSize=100)
                print("⚠ This request may return appointments outside your date range!")
        else:
            print("\n" + "-"*50)
            print("EXAMPLE 2: Skipped - No data in first batch")
            print("-"*50)
            print("Cannot demonstrate lastId pagination without real data")
            print("This might mean:")
            print("- No appointments were modified in the last 30 days")
            print("- Your organization has no appointments")
            
    except Exception as e:
        print(f"✗ Initial request failed: {e}")
        print("This might indicate:")
        print("- Invalid organization ID")
        print("- API access issues")
        print("- Organization configuration problems")
        return
    
    # Example 4: Get all appointments using pagination
    print("\n" + "-"*50)
    print("EXAMPLE 4: Get All Appointments (Complete Pagination)")
    print("-"*50)
    print("This will automatically chain calls:")
    print("  1. First call: Uses lastModified filter")
    print("  2. Subsequent calls: Use lastId + lastModified filter")
    print("  3. Continues until all pages are retrieved")
    
    try:
        allAppointments = getAllAppointmentsPaginated(headerData, lastModifiedDate, pageSize=100, max_batches=10)
        print(f"✓ Successfully retrieved {len(allAppointments)} total appointments")
    except Exception as e:
        print(f"✗ Get all appointments failed: {e}")
        print("This is expected if organization has no appointments in the date range")
    
    # Summary
    print("\n" + "="*70)
    print("PAGINATION PATTERN SUMMARY:")
    print("="*70)
    print("✓ CORRECT PATTERN:")
    print("  1. Initial request: /v1/appointments?pageSize=N&filter=lastModified>=YYYY-MM-DDTHH:MM:SS.000Z")
    print("  2. Get last ID from response: lastId = response['data'][-1]['id']")
    print("  3. Subsequent requests: /v1/appointments?pageSize=N&lastId=123456789&filter=lastModified>=YYYY-MM-DDTHH:MM:SS.000Z")
    print("  4. IMPORTANT: Keep the lastModified filter in ALL subsequent requests!")
    print("  5. Repeat until you get fewer results than pageSize")
    print()
    print("✗ COMMON MISTAKES:")
    print("  - Forgetting to include lastModified filter in subsequent requests")
    print("  - Using lastModified as a parameter instead of in the filter")
    print("  - Not using lastId for subsequent requests (using page numbers instead)")
    print("="*70)
    print("APPOINTMENTS PAGINATION EXAMPLE COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()

