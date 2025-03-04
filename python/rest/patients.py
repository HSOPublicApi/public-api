import json
import util
import requests

def getPatientData(locationId):
    return  {
    "firstName": "John",
    "middleInitial": "A",
    "lastName": "Doe",
    "contactMethod": "EMAIL ME",
    "chartNumber": "RhnCm888",
    "emailAddress": "johnadoe@test.com",
    "patientStatus": "Active",
    "dateOfBirth": "1999-01-01",
    "gender": "M",
    "address1": "Address 1",
    "address2": "Address 2",
    "city": "Salt Lake",
    "state": "UT",
    "postalCode": "88888-7777",
    "languageType": "ENGLISH",
    "preferredName": "JD",
    "title": "Title",
    "suffix": "Sufix",
    "phones": [
        {
            "number": "1112223333",
            "phoneType": "Mobile",
            "sequence": 1
        }
    ],
    "preferredLocation": {
        "id": locationId
    }
}

def getPatientById(headerData, patientId):
    url = util.baseUrl + f"/v1/patients/{patientId}"
    response = requests.get(url, headers = headerData)
    util.printResponse("getPatient", response)

def getPatients(headerData, locationId):
    url = util.baseUrl + "/v1/patients"
    patientParams = {
        "filter": f"preferredLocation.id=={locationId}",
        "pageSize": 10
    }
    response = requests.get(url, params=patientParams, headers=headerData)
    util.printResponse("getPatients", response)
    responseJSON = response.json()
    return (responseJSON["data"][0]["id"])

def createPatient(headerData, locationId):
    url = util.baseUrl + "/v1/patients"
    patientData = getPatientData(locationId)
    jsonData = json.dumps(patientData)
    response = requests.post(url, data=jsonData, headers=headerData)
    util.printResponse("createPatient", response)
    responseJSON = response.json()
    return (responseJSON["data"]["id"])