import requests
import util
import appointments
import locations
import patients
import operatories
import providers
organizationId = "<organizationId>" # Replace <organizationId> with your organization ID, or hardcode a value directly

# THESE VALUES SHOULD BE KEPT SECRET!
# Move them to a protected file and don't push them up to a repository
clientId = "<clientId>" # Replace <clientId> with your client ID
clientSecret = "<clientSecret>" # Replace <clientSecret> with your client secret


def init():
    # Get access token (this will load from config.py if placeholders are used)
    accessToken = util.getAccessToken(clientId, clientSecret)
    # Get organization ID (uses hardcoded value if provided, otherwise loads from config.py)
    orgId = util.getOrganizationId(organizationId)
    # Create header data with access token and organization id
    headerData = {
        "Authorization": accessToken,
        "Organization-ID": orgId,
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