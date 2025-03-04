import util
import requests

def getOperatories(headers):
    url = util.baseUrl + "/v1/operatories"
    operatoryParams = {
        "pageSize": 2
    }
    response = requests.get(url, params=operatoryParams, headers=headers)
    util.printResponse("getOperatories", response)
    responseJSON = response.json()
    return (responseJSON["data"][0]["id"])