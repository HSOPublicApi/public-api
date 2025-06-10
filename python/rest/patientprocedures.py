import requests
import util

def getPatientProcedures(headerData, pageSize=100, lastId=None):
    """
    Get patient procedures with cursor-based pagination using lastId
    """
    url = util.baseUrl + "/v1/patientprocedures"
    params = {
        "pageSize": pageSize
    }
    
    # Add lastId parameter if provided (for subsequent calls)
    if lastId:
        params["lastId"] = lastId
        
    response = requests.get(url, params=params, headers=headerData)
    
    # Create a descriptive label for the response
    if lastId:
        util.printResponse(f"getPatientProcedures (after ID {lastId})", response)
    else:
        util.printResponse("getPatientProcedures (first batch)", response)
        
    return response.json()

def getAllPatientProcedures(headerData, pageSize=100):
    """
    Get all patient procedures by iterating through all pages using lastId cursor pagination
    """
    print("\n=== Getting ALL Patient Procedures with Cursor Pagination ===")
    allProcedures = []
    lastId = None
    batchNumber = 1
    
    while True:
        print(f"\n--- Fetching batch {batchNumber} ---")
        url = util.baseUrl + "/v1/patientprocedures"
        params = {
            "pageSize": pageSize,
            "filter": "lastModified>=2024-01-01T00:00:00.000Z"
        }
        
        # Add lastId parameter if we have one (for subsequent calls)
        if lastId:
            params["lastId"] = lastId
            
        response = requests.get(url, params=params, headers=headerData)
        
        if response.status_code != 200:
            print(f"Error fetching batch {batchNumber}: {response.status_code}")
            break
            
        responseData = response.json()
        
        # Create descriptive label for response
        if lastId:
            util.printResponse(f"getPatientProcedures (batch {batchNumber}, after ID {lastId})", response)
        else:
            util.printResponse(f"getPatientProcedures (batch {batchNumber}, first batch)", response)
        
        # Add procedures from this batch to our collection
        if "data" in responseData and responseData["data"]:
            currentBatch = responseData["data"]
            allProcedures.extend(currentBatch)
            print(f"Added {len(currentBatch)} procedures from batch {batchNumber}")
            
            # Get the last ID from this batch for the next request
            lastId = currentBatch[-1]["id"]
            print(f"Last ID in this batch: {lastId}")
            
            # Check if we got fewer results than pageSize (indicating last page)
            if len(currentBatch) < pageSize:
                print(f"Received {len(currentBatch)} procedures (less than pageSize {pageSize})")
                print("This indicates we've reached the end of the data")
                break
        else:
            print(f"No more data found in batch {batchNumber}")
            break
            
        batchNumber += 1
    
    print(f"\n=== Total Procedures Retrieved: {len(allProcedures)} ===")
    return allProcedures

def getPatientProceduresByPatientId(headerData, patientId, pageSize=100, lastId=None):
    """
    Get patient procedures for a specific patient with cursor-based pagination
    """
    print(f"\n=== Getting Patient Procedures for Patient ID: {patientId} ===")
    url = util.baseUrl + "/v1/patientprocedures"
    params = {
        "filter": f"patient.id=={patientId}",
        "pageSize": pageSize
    }
    
    # Add lastId parameter if provided
    if lastId:
        params["lastId"] = lastId
        
    response = requests.get(url, params=params, headers=headerData)
    
    # Create descriptive label for response
    if lastId:
        util.printResponse(f"getPatientProceduresByPatientId ({patientId}, after ID {lastId})", response)
    else:
        util.printResponse(f"getPatientProceduresByPatientId ({patientId}, first batch)", response)
        
    return response.json()

def getAllPatientProceduresForPatient(headerData, patientId, pageSize=500):
    """
    Get ALL patient procedures for a specific patient using cursor pagination
    """
    print(f"\n=== Getting ALL Patient Procedures for Patient ID: {patientId} ===")
    allProcedures = []
    lastId = None
    batchNumber = 1
    
    while True:
        print(f"\n--- Fetching batch {batchNumber} for patient {patientId} ---")
        
        # Get this batch of procedures for the patient
        responseData = getPatientProceduresByPatientId(headerData, patientId, pageSize, lastId)
        
        # Add procedures from this batch to our collection
        if "data" in responseData and responseData["data"]:
            currentBatch = responseData["data"]
            allProcedures.extend(currentBatch)
            print(f"Added {len(currentBatch)} procedures from batch {batchNumber}")
            
            # Get the last ID from this batch for the next request
            lastId = currentBatch[-1]["id"]
            print(f"Last ID in this batch: {lastId}")
            
            # Check if we got fewer results than pageSize (indicating last page)
            if len(currentBatch) < pageSize:
                print(f"Received {len(currentBatch)} procedures (less than pageSize {pageSize})")
                print("This indicates we've reached the end of the data for this patient")
                break
        else:
            print(f"No more data found in batch {batchNumber} for patient {patientId}")
            break
            
        batchNumber += 1
    
    print(f"\n=== Total Procedures Retrieved for Patient {patientId}: {len(allProcedures)} ===")
    return allProcedures 