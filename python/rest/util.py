import json

baseUrl = "https://prod.hs1api.com/ascend-gateway/api" # Henry Schein One base URL

def printResponse(requestName, response):
    print()
    print(requestName)
    print("status code: " + str(response.status_code))
    print(json.dumps(response.json(), indent = 2))