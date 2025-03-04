import requests
import json
import util

def getAppointmentData(patientId, providerId, operatoryId):
    return {
        "start": "2025-01-01T17:00:00.000Z",
        "patient": {
            "id": patientId
        },
        "provider": {
            "id": providerId
        },
        "operatory": {
            "id": operatoryId
        },
        "needsPremedicate": False,
        "insuranceEligibilityVerified": "2024-01-01",
        "status": "LATE",
        "note": "My appointment test Note!!",
        "other": "My Other Test Note!!",
        "bookedOnline": False,
        "needsFollowup": False
    }

def getAppointments(headers):
    url = util.baseUrl + "/v1/appointments"
    appointmentParams = {
        "pageSize": 2
    }
    response = requests.get(url, params=appointmentParams, headers=headers)
    util.printResponse("getAppointmentById", response)

def getAppointmentById(headers, appointmentId):
    url = util.baseUrl + "/v1/appointments/" + appointmentId
    response = requests.get(url, headers=headers)
    util.printResponse("getAppointmentById", response)

def createAppointment(headers, patientId, providerId, operatoryId):
    url = util.baseUrl + "/v1/appointments"
    appointmentData = getAppointmentData(patientId, providerId, operatoryId)
    jsonData = json.dumps(appointmentData)
    response = requests.post(url, data=jsonData, headers=headers)
    util.printResponse("createAppointment", response)
    responseJSON = response.json()
    return (responseJSON["data"]["id"])

def updateAppointment(headers, appointmentId, patientId, providerId, operatoryId):
    url = util.baseUrl + "/v1/appointments/" + appointmentId
    appointmentData = getAppointmentData(patientId, providerId, operatoryId)
    appointmentData["status"] = "HERE"
    jsonData = json.dumps(appointmentData)
    response = requests.put(url, data=jsonData, headers=headers)
    util.printResponse("updateAppointment", response)

def deleteAppointment(headers, appointmentId):
    url = util.baseUrl + "/v1/appointments/" + appointmentId
    response = requests.delete(url, headers=headers)
    util.printResponse("deleteAppointment", response)