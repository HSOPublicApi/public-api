import requests
import util
import locations
import patients
import patientinsuranceplans

organizationId = "1234" # Replace 1234 with your organization ID

# THESE VALUES SHOULD BE KEPT SECRET!
# Move them to a protected file and don't push them up to a repository
clientId = "<clientId>" # Replace <clientId> with your client ID
clientSecret = "<clientSecret>" # Replace <clientSecret> with your client secret


def main():
    print("="*70)
    print("PATIENT INSURANCE PLANS CURSOR-BASED PAGINATION EXAMPLES")
    print("="*70)
    
    # Get access token
    accessToken = util.getAccessToken(clientId, clientSecret)
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
    print("STARTING PATIENT INSURANCE PLANS CURSOR PAGINATION EXAMPLES")
    print("="*70)
    
    # Example 1: Get first batch of patient insurance plans (no lastId)
    print("\n" + "-"*50)
    print("EXAMPLE 1: First Batch Request (No lastId)")
    print("-"*50)
    print("URL: /v1/patientinsuranceplans?pageSize=100")
    
    try:
        firstBatch = patientinsuranceplans.getPatientInsurancePlans(headerData, pageSize=100)
        print("✓ First batch request successful")
        
        # Example 2: Get next batch using lastId from first batch
        if firstBatch.get("data") and len(firstBatch["data"]) > 0:
            lastId = firstBatch["data"][-1]["id"]
            print(f"\n" + "-"*50)
            print("EXAMPLE 2: Next Batch Request (Using lastId)")
            print("-"*50)
            print(f"URL: /v1/patientinsuranceplans?pageSize=100&lastId={lastId}")
            patientinsuranceplans.getPatientInsurancePlans(headerData, pageSize=100, lastId=lastId)
        else:
            print("\n" + "-"*50)
            print("EXAMPLE 2: Skipped - No data in first batch")
            print("-"*50)
            print("Cannot demonstrate lastId pagination without real data")
            
    except Exception as e:
        print(f"✗ First batch request failed: {e}")
        print("This might indicate:")
        print("- No patient insurance plans exist in your organization")
        print("- API access issues")
        print("- Organization configuration problems")
    
    # Example 3: Get all patient insurance plans using cursor pagination
    print("\n" + "-"*50)
    print("EXAMPLE 3: Get All Batches (Complete Dataset)")
    print("-"*50)
    print("This will automatically chain calls using lastId from each response")
    
    try:
        allPlans = patientinsuranceplans.getAllPatientInsurancePlans(headerData, pageSize=100, max_batches=10)
        print(f"✓ Successfully retrieved {len(allPlans)} total insurance plans")
        
        # Store the last ID for use in Example 7
        lastPlanId = allPlans[-1]["id"] if allPlans else None
    except Exception as e:
        print(f"✗ Get all insurance plans failed: {e}")
        print("This is expected if organization has no insurance plans")
        lastPlanId = None

    # Example 4: Get patient insurance plans for a specific patient (first batch)
    print("\n" + "-"*50)
    print("EXAMPLE 4: Filtered Results with Cursor Pagination")
    print("-"*50)
    print(f"URL: /v1/patientinsuranceplans?filter=patient.id=={patientId}&pageSize=100")
    
    try:
        patientBatch = patientinsuranceplans.getPatientInsurancePlansByPatientId(headerData, patientId, pageSize=100)
        print("✓ Filtered request successful")
        
        # Example 5: Get next batch for the same patient if data exists
        if patientBatch.get("data") and len(patientBatch["data"]) > 0:
            lastIdForPatient = patientBatch["data"][-1]["id"]
            print(f"\n" + "-"*50)
            print("EXAMPLE 5: Next Batch for Same Patient (Using lastId)")
            print("-"*50)
            print(f"URL: /v1/patientinsuranceplans?filter=patient.id=={patientId}&pageSize=5&lastId={lastIdForPatient}")
            patientinsuranceplans.getPatientInsurancePlansByPatientId(headerData, patientId, pageSize=5, lastId=lastIdForPatient)
        else:
            print(f"\n" + "-"*50)
            print("EXAMPLE 5: Skipped - No insurance plans found for this patient")
            print("-"*50)
            print("Cannot demonstrate patient-specific lastId pagination without real data")
            
    except Exception as e:
        print(f"✗ Filtered request failed: {e}")
        print("This is expected if the patient has no insurance plans")
    
    # Example 6: Get ALL insurance plans for a specific patient using cursor pagination
    print(f"\n" + "-"*50)
    print("EXAMPLE 6: Get All Insurance Plans for Patient (Complete Dataset)")
    print("-"*50)
    print("This will automatically chain calls for the patient using lastId")
    
    try:
        allPatientPlans = patientinsuranceplans.getAllPatientInsurancePlansForPatient(headerData, patientId, pageSize=100, max_batches=10)
        print(f"✓ Successfully retrieved {len(allPatientPlans)} insurance plans for patient")
    except Exception as e:
        print(f"✗ Get all patient insurance plans failed: {e}")
        print("This is expected if the patient has no insurance plans")

    # Example 7: Get a specific patient insurance plan by ID
    print("\n" + "-"*50)
    print("EXAMPLE 7: Get Specific Patient Insurance Plan by ID")
    print("-"*50)
    print("This demonstrates how to get a single plan using its ID")
    
    try:
        if lastPlanId:
            print(f"\n=== Getting Patient Insurance Plan with ID: {lastPlanId} ===\n")
            plan = patientinsuranceplans.getPatientInsurancePlanById(headerData, lastPlanId)
            if plan and plan.get("data"):
                print("✓ Successfully retrieved plan with ID:", lastPlanId)
                print("Patient ID:", plan["data"]["patient"]["id"])
                print("Start Date:", plan["data"]["startDate"])
                print("Benefit Year:", plan["data"]["current_benefitYear"])
            else:
                print("✗ No plan found with ID:", lastPlanId)
        else:
            print("✗ Cannot demonstrate plan lookup - no valid plan ID available")
            print("This might indicate:")
            print("- No insurance plans exist in your organization")
            print("- API access issues")
            print("- Organization configuration problems")
    except Exception as e:
        print(f"✗ Failed to get plan: {e}")
        print("This might indicate:")
        print("- The plan ID doesn't exist")
        print("- API access issues")
        print("- Organization configuration problems")

    # Example 8: Get Insurance Plans for Specific Patient ID
    print("\n" + "-"*50)
    print("EXAMPLE 8: Get Insurance Plans for Specific Patient ID")
    print("-"*50)
    print("This demonstrates filtering with a specific patient ID")
    
    specificPatientId = "8000012732615"  # Using a known patient ID
    print(f"\n=== Getting Insurance Plans for Patient ID: {specificPatientId} ===\n")
    try:
        plans = patientinsuranceplans.getPatientInsurancePlansByPatientId(headerData, specificPatientId, pageSize=100)
        if plans and plans.get("data"):
            print("✓ Successfully retrieved plans for patient ID:", specificPatientId)
            print(f"Found {len(plans['data'])} insurance plans:")
            for plan in plans["data"]:
                print(f"\nPlan ID: {plan['id']}")
                print(f"Start Date: {plan['startDate']}")
                print(f"Benefit Year: {plan['current_benefitYear']}")
                print(f"Eligible: {plan['eligible']}")
        else:
            print("No insurance plans found for this patient")
    except Exception as e:
        print(f"✗ Failed to get plans: {e}")
        print("This might indicate:")
        print("- The patient ID doesn't exist")
        print("- API access issues")
        print("- Organization configuration problems")

    print("\n" + "="*70)
    print("CURSOR-BASED PAGINATION PATTERN SUMMARY:")
    print("="*70)
    print("✓ Authentication successful")
    print("✓ URL structure and parameter construction working")
    print("1. First call: /v1/patientinsuranceplans?pageSize=N")
    print("2. Get last ID from response: lastId = response['data'][-1]['id']")
    print("3. Next call: /v1/patientinsuranceplans?pageSize=N&lastId=123456789")
    print("4. Repeat until you get fewer results than pageSize")
    print("5. Works with filters too: add &filter=... to any call")
    print("="*70)
    print("PATIENT INSURANCE PLANS CURSOR PAGINATION EXAMPLES COMPLETED")
    print("="*70)

if __name__ == "__main__":
    main() 