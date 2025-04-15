import requests
import json

baseUrl = "https://prod.hs1api.com" # Henry Schein One base URL

patientId = "1234"; # Replace 1234 with a patient ID
organizationId = "1234" # Replace 1234 with your organization ID

# THESE VALUES SHOULD BE KEPT SECRET!
# Move them to a protected file and don't push them up to a repository
clientId = "<clientId>" # Replace <clientId> with your client ID
clientSecret = "<clientSecret>" # Replace <clientSecret> with your client secret

def printResponse(requestName, response):
    print()
    print(requestName)
    print("status code: " + str(response.status_code))
    print(json.dumps(response.json(), indent = 2))

# You can uncomment printResponse to see the access token response
def getAccessToken():
    url = baseUrl + "/oauth/client_credential/accesstoken?grant_type=client_credentials"
    headerData = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": clientId,
        "client_secret": clientSecret
    }
    response = requests.post(url, data = body, headers = headerData)
    printResponse("getAccessToken", response)
    responseJSON = response.json()

    return responseJSON["token_type"] + " " + responseJSON["access_token"]

def getExamImageData(headers, patientId):
    url = baseUrl + "/ascend-imaging/ExamImage/v2/" + patientId
    response = requests.get(url, headers=headers)
    printResponse("getExamImageData", response)
    responseJSON = response.json()
    return responseJSON

def imageRetrieval(headers, imageId):
    url = baseUrl + "/ascend-imaging/ImageRetrieval/v2/" + imageId
    response = requests.get(url, headers=headers)
    print()
    print(response.text)

def init():
    # Get access token
    accessToken = getAccessToken()
    # Create header data with access token and organization id
    headerData = {
        "Authorization": accessToken,
        "Organization-ID": organizationId
    }

    examImageData = getExamImageData(headerData, patientId)
    for exam in examImageData:
        imageRetrieval(headerData, str(exam["examImageId"]))

if __name__ == "__main__":
    init()