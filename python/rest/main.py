import requests
import util
import appointments
import locations
import patients
import operatories
import providers

organizationId = "1234" # Replace 1234 with your organization ID

# THESE VALUES SHOULD BE KEPT SECRET!
# Move them to a protected file and don't push them up to a repository
clientId = "<clientId>" # Replace <clientId> with your client ID
clientSecret = "<clientSecret>" # Replace <clientSecret> with your client secret

# You can uncomment printResponse to see the access token response
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


def init():
    # Get access token
    accessToken = getAccessToken()
    # Create header data with access token and organization id
    headerData = {
        "Authorization": accessToken,
        "Organization-ID": organizationId,
        "Content-Type": "application/json"
    }

    # Make request to the RESTful api, you can comment out the ones you don't want to run
    # get data needed in future requests
    locationId = locations.getLocations(headerData)
    patientId = patients.getPatients(headerData, locationId)
    providerId = providers.getProviders(headerData)
    operatoryId = operatories.getOperatories(headerData)

    # create data
    appointmentId = appointments.createAppointment(headerData, patientId, providerId, operatoryId)

    # update data
    appointments.updateAppointment(headerData, appointmentId, patientId, providerId, operatoryId)

    # get data by id
    appointments.getAppointmentById(headerData, appointmentId)

    # delete created data
    appointments.deleteAppointment(headerData, appointmentId)

if __name__ == "__main__":
    init()