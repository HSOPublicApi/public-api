import util
import requests

def getProviders(headerData):
    url = util.baseUrl + "/v1/providers"
    providersParams = {
        "pageSize": 2
    }
    response = requests.get(url, params=providersParams, headers=headerData)
    util.printResponse("getProviders", response)
    responseJSON = response.json()
    return (responseJSON["data"][0]["id"])