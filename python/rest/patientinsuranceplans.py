import requests
import util

def getPatientInsurancePlans(headerData, pageSize=100, lastId=None, patientId=None):
    """
    Get a batch of patient insurance plans with optional filtering by patient ID
    """
    url = util.baseUrl + "/v1/patientinsuranceplans"
    params = {
        "pageSize": pageSize
    }
    
    # Add filter for specific patient if provided
    if patientId:
        params["filter"] = f"patient.id=={patientId}"
        
    # Add lastId parameter if we have one (for subsequent calls)
    if lastId:
        params["lastId"] = lastId
        
    response = requests.get(url, params=params, headers=headerData)
    util.printResponse("getPatientInsurancePlans", response)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching batch: {response.status_code}")
        
    return response.json()

def getPatientInsurancePlansByPatientId(headerData, patientId, pageSize=100, lastId=None):
    """
    Get patient insurance plans for a specific patient
    """
    return getPatientInsurancePlans(headerData, pageSize, lastId, patientId)

def getAllPatientInsurancePlans(headerData, pageSize=100, max_batches=10):
    """
    Get all patient insurance plans by iterating through all pages using lastId cursor pagination
    """
    print("\n=== Getting ALL Patient Insurance Plans with Cursor Pagination ===")
    allPlans = []
    lastId = None
    batchNumber = 1
    
    while True:
        print(f"\n--- Fetching batch {batchNumber} ---")
        try:
            response = getPatientInsurancePlans(headerData, pageSize, lastId)
            batch = response.get("data", [])
            
            if not batch:
                print("No more data available")
                break
                
            allPlans.extend(batch)
            print(f"Added {len(batch)} plans from batch {batchNumber}")
            
            if len(batch) < pageSize:
                print(f"Last batch had {len(batch)} plans (< pageSize {pageSize})")
                break
                
            lastId = batch[-1]["id"]
            print(f"Last ID in this batch: {lastId}")
            batchNumber += 1
            
            # Check if we've reached the maximum number of batches
            if batchNumber > max_batches:
                print(f"\nReached maximum number of batches ({max_batches})")
                break
            
        except Exception as e:
            print(f"Error fetching batch {batchNumber}: {e}")
            break
            
    return allPlans

def getAllPatientInsurancePlansForPatient(headerData, patientId, pageSize=100, max_batches=10):
    """
    Get all patient insurance plans for a specific patient using cursor pagination
    """
    print(f"\n=== Getting ALL Patient Insurance Plans for Patient {patientId} ===")
    allPlans = []
    lastId = None
    batchNumber = 1
    
    while True:
        print(f"\n--- Fetching batch {batchNumber} ---")
        try:
            response = getPatientInsurancePlansByPatientId(headerData, patientId, pageSize, lastId)
            batch = response.get("data", [])
            
            if not batch:
                print("No more data available")
                break
                
            allPlans.extend(batch)
            print(f"Added {len(batch)} plans from batch {batchNumber}")
            
            if len(batch) < pageSize:
                print(f"Last batch had {len(batch)} plans (< pageSize {pageSize})")
                break
                
            lastId = batch[-1]["id"]
            print(f"Last ID in this batch: {lastId}")
            batchNumber += 1
            
            # Check if we've reached the maximum number of batches
            if batchNumber > max_batches:
                print(f"\nReached maximum number of batches ({max_batches})")
                break
            
        except Exception as e:
            print(f"Error fetching batch {batchNumber}: {e}")
            break
            
    return allPlans

def getPatientInsurancePlanById(headerData, planId):
    """
    Get a specific patient insurance plan by its ID
    """
    print(f"\n=== Getting Patient Insurance Plan with ID: {planId} ===")
    url = util.baseUrl + f"/v1/patientinsuranceplans/{planId}"
    response = requests.get(url, headers=headerData)
    util.printResponse(f"getPatientInsurancePlanById ({planId})", response)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching plan: {response.status_code}")
        
    return response.json() 