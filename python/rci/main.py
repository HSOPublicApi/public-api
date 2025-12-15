import requests
import config
import util


# You can uncomment print_response to see the access token response
def getAccessToken():
    url = util.baseUrl + "/oauth/client_credential/accesstoken?grant_type=client_credentials"
    headerData = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": config.clientId,
        "client_secret": config.clientSecret
    }
    response = requests.post(url, data=body, headers=headerData)
    util.print_response("getAccessToken", response)
    responseJSON = response.json()

    return responseJSON["token_type"] + " " + responseJSON["access_token"]


def getExamImageData(headers, patientId):
    url = util.baseUrl + "/ascend-imaging/ExamImage/v2/" + patientId
    response = requests.get(url, headers=headers)
    util.print_response("getExamImageData", response)
    if response.status_code != 200:
        return None
    responseJSON = response.json()
    return responseJSON


def imageRetrieval(headers, imageId):
    url = util.baseUrl + "/ascend-imaging/ImageRetrieval/v2/" + imageId
    response = requests.get(url, headers=headers)
    print()
    print(response.text)


def init():
    # Get access token
    accessToken = getAccessToken()
    # Create header data with access token and organization id
    headerData = {
        "Authorization": accessToken,
        "Organization-ID": config.organizationId
    }

    examImageData = getExamImageData(headerData, config.patientId)
    if examImageData is None:
        print("Error: Failed to retrieve exam image data. Please check your patientId and organizationId.")
        return
    if not isinstance(examImageData, list):
        print("Error: Expected a list of exam images, but received:", type(examImageData))
        return
    for exam in examImageData:
        imageRetrieval(headerData, str(exam["examImageId"]))

if __name__ == "__main__":
    init()