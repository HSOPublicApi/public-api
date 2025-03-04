import requests
import util

def getLocations(headers):
    url = util.baseUrl + "/v1/locations"
    response = requests.get(url, headers=headers)
    util.printResponse("getLocations", response)
    responseJSON = response.json()
    return (responseJSON["data"][0]["id"])