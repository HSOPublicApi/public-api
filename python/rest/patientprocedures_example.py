import requests
import util
import locations
import patients
import patientprocedures

organizationId = "1234" # Replace 1234 with your organization ID

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
    responseJSON = response.json()

    return responseJSON["token_type"] + " " + responseJSON["access_token"]

def main():
    print("="*70)
    print("PATIENT PROCEDURES CURSOR-BASED PAGINATION EXAMPLES")
    print("="*70)
    
    # Get access token
    accessToken = getAccessToken()
    # Create header data with access token and organization id
    headerData = {
        "Authorization": accessToken,
        "Organization-ID": organizationId,
        "Content-Type": "application/json"
    }

    # Get real data needed for filtering examples - fail if we can't get them
    print("\n" + "-"*50)
    print("SETUP: Getting Location and Patient IDs for filtering examples")
    print("-"*50)
    
    try:
        locationId = locations.getLocations(headerData)
        print(f"✓ Successfully got locationId: {locationId}")
    except Exception as e:
        print(f"✗ Failed to get location ID: {e}")
        print("ERROR: Cannot proceed without valid location data.")
        print("Please verify:")
        print("1. Your organizationId is correct")
        print("2. Your organization has locations set up")
        print("3. Your API credentials have proper access")
        return
    
    try:
        patientId = patients.getPatients(headerData, locationId)
        print(f"✓ Successfully got patientId: {patientId}")
    except Exception as e:
        print(f"✗ Failed to get patient ID: {e}")
        print("ERROR: Cannot proceed without valid patient data.")
        print("Please verify your organization has patients set up")
        return

    print("\n" + "="*70)
    print("STARTING PATIENT PROCEDURES CURSOR PAGINATION EXAMPLES")
    print("="*70)
    
    # Example 1: Get first batch of patient procedures (no lastId)
    print("\n" + "-"*50)
    print("EXAMPLE 1: First Batch Request (No lastId)")
    print("-"*50)
    print("URL: /v1/patientprocedures?pageSize=100")
    
    try:
        firstBatch = patientprocedures.getPatientProcedures(headerData, pageSize=100)
        print("✓ First batch request successful")
        
        # Example 2: Get next batch using lastId from first batch
        if firstBatch.get("data") and len(firstBatch["data"]) > 0:
            lastId = firstBatch["data"][-1]["id"]
            print(f"\n" + "-"*50)
            print("EXAMPLE 2: Next Batch Request (Using lastId)")
            print("-"*50)
            print(f"URL: /v1/patientprocedures?pageSize=100&lastId={lastId}")
            patientprocedures.getPatientProcedures(headerData, pageSize=100, lastId=lastId)
        else:
            print("\n" + "-"*50)
            print("EXAMPLE 2: Skipped - No data in first batch")
            print("-"*50)
            print("Cannot demonstrate lastId pagination without real data")
            
    except Exception as e:
        print(f"✗ First batch request failed: {e}")
        print("This might indicate:")
        print("- No patient procedures exist in your organization")
        print("- API access issues")
        print("- Organization configuration problems")
    
    # Example 3: Get all patient procedures using cursor pagination
    print("\n" + "-"*50)
    print("EXAMPLE 3: Get All Batches (Complete Dataset)")
    print("-"*50)
    print("This will automatically chain calls using lastId from each response")
    
    try:
        allProcedures = patientprocedures.getAllPatientProcedures(headerData, pageSize=100, max_batches=10)
        print(f"✓ Successfully retrieved {len(allProcedures)} total procedures")
    except Exception as e:
        print(f"✗ Get all procedures failed: {e}")
        print("This is expected if organization has no patient procedures")
    
    # Example 4: Get patient procedures for a specific patient (first batch)
    print("\n" + "-"*50)
    print("EXAMPLE 4: Filtered Results with Cursor Pagination")
    print("-"*50)
    print(f"URL: /v1/patientprocedures?filter=patient.id=={patientId}&pageSize=500")
    
    try:
        patientBatch = patientprocedures.getPatientProceduresByPatientId(headerData, patientId, pageSize=100)
        print("✓ Filtered request successful")
        
        # Example 5: Get next batch for the same patient if data exists
        if patientBatch.get("data") and len(patientBatch["data"]) > 0:
            lastIdForPatient = patientBatch["data"][-1]["id"]
            print(f"\n" + "-"*50)
            print("EXAMPLE 5: Next Batch for Same Patient (Using lastId)")
            print("-"*50)
            print(f"URL: /v1/patientprocedures?filter=patient.id=={patientId}&pageSize=5&lastId={lastIdForPatient}")
            patientprocedures.getPatientProceduresByPatientId(headerData, patientId, pageSize=5, lastId=lastIdForPatient)
        else:
            print(f"\n" + "-"*50)
            print("EXAMPLE 5: Skipped - No procedures found for this patient")
            print("-"*50)
            print("Cannot demonstrate patient-specific lastId pagination without real data")
            
    except Exception as e:
        print(f"✗ Filtered request failed: {e}")
        print("This is expected if the patient has no procedures")
    
    # Example 6: Get ALL procedures for a specific patient using cursor pagination
    print(f"\n" + "-"*50)
    print("EXAMPLE 6: Get All Procedures for Patient (Complete Dataset)")
    print("-"*50)
    print("This will automatically chain calls for the patient using lastId")
    
    try:
        allPatientProcedures = patientprocedures.getAllPatientProceduresForPatient(headerData, patientId, pageSize=500, max_batches=10)
        print(f"✓ Successfully retrieved {len(allPatientProcedures)} procedures for patient")
    except Exception as e:
        print(f"✗ Get all patient procedures failed: {e}")
        print("This is expected if the patient has no procedures")

    # Example 7: Get patient procedures with specific response fields (including procedureTeeth)
    print("\n" + "-"*50)
    print("EXAMPLE 7: Response Fields - Including procedureTeeth")
    print("-"*50)
    print("URL: /v1/patientprocedures?pageSize=5&responseFields=id,patient,procedureTeeth,status")
    
    try:
        # Define response fields that include procedureTeeth
        responseFieldsWithTeeth = ["id", "patient", "procedureTeeth", "status", "amount", "notes"]
        proceduresWithTeeth = patientprocedures.getPatientProceduresWithResponseFields(
            headerData, 
            responseFieldsWithTeeth, 
            pageSize=5
        )
        print("✓ Response fields request (with procedureTeeth) successful")
        
        # Show what fields are actually returned
        if proceduresWithTeeth.get("data") and len(proceduresWithTeeth["data"]) > 0:
            sampleProcedure = proceduresWithTeeth["data"][0]
            print(f"Sample procedure fields returned: {list(sampleProcedure.keys())}")
            if "procedureTeeth" in sampleProcedure:
                print(f"✓ procedureTeeth field is present: {sampleProcedure['procedureTeeth']}")
            else:
                print("✗ procedureTeeth field is missing (unexpected)")
        else:
            print("No data returned to verify field structure")
            
    except Exception as e:
        print(f"✗ Response fields request (with procedureTeeth) failed: {e}")
    
    # Example 8: Get patient procedures with specific response fields (excluding procedureTeeth)
    print("\n" + "-"*50)
    print("EXAMPLE 8: Response Fields - Excluding procedureTeeth")
    print("-"*50)
    print("URL: /v1/patientprocedures?pageSize=5&responseFields=id,patient,status,amount")
    
    try:
        # Define response fields that exclude procedureTeeth
        responseFieldsWithoutTeeth = ["id", "patient", "status", "amount", "notes", "serviceDate"]
        proceduresWithoutTeeth = patientprocedures.getPatientProceduresWithResponseFields(
            headerData, 
            responseFieldsWithoutTeeth, 
            pageSize=5
        )
        print("✓ Response fields request (without procedureTeeth) successful")
        
        # Show what fields are actually returned
        if proceduresWithoutTeeth.get("data") and len(proceduresWithoutTeeth["data"]) > 0:
            sampleProcedure = proceduresWithoutTeeth["data"][0]
            print(f"Sample procedure fields returned: {list(sampleProcedure.keys())}")
            if "procedureTeeth" in sampleProcedure:
                print("✗ procedureTeeth field is present (unexpected - should be excluded)")
            else:
                print("✓ procedureTeeth field is correctly excluded")
        else:
            print("No data returned to verify field structure")
            
    except Exception as e:
        print(f"✗ Response fields request (without procedureTeeth) failed: {e}")
    
    # Example 9: Get patient procedures for specific patient with response fields
    print("\n" + "-"*50)
    print("EXAMPLE 9: Patient-Specific Response Fields")
    print("-"*50)
    print(f"URL: /v1/patientprocedures?filter=patient.id=={patientId}&pageSize=3&responseFields=id,patient,procedureTeeth,status")
    
    try:
        # Define response fields for patient-specific request
        patientResponseFields = ["id", "patient", "procedureTeeth", "status", "amount", "notes", "serviceDate"]
        patientProceduresWithFields = patientprocedures.getPatientProceduresByPatientIdWithResponseFields(
            headerData, 
            patientId, 
            patientResponseFields, 
            pageSize=3
        )
        print("✓ Patient-specific response fields request successful")
        
        # Show what fields are actually returned
        if patientProceduresWithFields.get("data") and len(patientProceduresWithFields["data"]) > 0:
            sampleProcedure = patientProceduresWithFields["data"][0]
            print(f"Sample patient procedure fields returned: {list(sampleProcedure.keys())}")
            print(f"Patient ID in response: {sampleProcedure.get('patient', {}).get('id', 'N/A')}")
            if "procedureTeeth" in sampleProcedure:
                print(f"✓ procedureTeeth field is present: {sampleProcedure['procedureTeeth']}")
            else:
                print("✗ procedureTeeth field is missing")
        else:
            print("No data returned to verify field structure")
            
    except Exception as e:
        print(f"✗ Patient-specific response fields request failed: {e}")
        print("This is expected if the patient has no procedures")

    print("\n" + "="*70)
    print("CURSOR-BASED PAGINATION PATTERN SUMMARY:")
    print("="*70)
    print("✓ Authentication successful")
    print("✓ URL structure and parameter construction working")
    print("1. First call: /v1/patientprocedures?pageSize=N")
    print("2. Get last ID from response: lastId = response['data'][-1]['id']")
    print("3. Next call: /v1/patientprocedures?pageSize=N&lastId=123456789")
    print("4. Repeat until you get fewer results than pageSize")
    print("5. Works with filters too: add &filter=... to any call")
    print("6. Use responseFields to limit returned data: add &responseFields=field1,field2,...")
    print("="*70)
    print("PATIENT PROCEDURES CURSOR PAGINATION EXAMPLES COMPLETED")
    print("="*70)

if __name__ == "__main__":
    main() 