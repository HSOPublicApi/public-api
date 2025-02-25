import sys
import json
import asyncio
import requests
from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage

baseUrl = "https://prod.hs1api.com" # Henry Schein One base URL

# THESE VALUES SHOULD BE KEPT SECRET!
# Move them to a protected file and don't push them up to a repository
clientId = "<clientId>" # Replace <clientId> with your client ID
clientSecret = "<clientSecret>" # Replace <clientSecret> with your client secret

def printResponse(requestName, response):
    print(requestName)
    print("status code: " + str(response.status_code))
    print(json.dumps(response.json(), indent = 2))
    print()

def getAccessToken():
    url = baseUrl + "/oauth/client_credential/accesstoken?grant_type=client_credentials"
    headerData = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": clientId,
        "client_secret": clientSecret
    }
    response = requests.post(url, data = body, headers = headerData)
    # printResponse("getAccessToken", response)
    responseJSON = response.json()

    return responseJSON["token_type"] + " " + responseJSON["access_token"]

def getStreamApiInfo(bearerToken):
    url = baseUrl + "/ascend-streaming-api/url"
    headerData = {
        "Authorization": bearerToken,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers = headerData)
    response.encoding = "utf-8"
    # printResponse("getStreamApiInfo", response)

    return response.json()

# Define a callback function to display messages in the console
async def messageCallback(message: AbstractIncomingMessage) -> None:
    async with message.process():
        print()
        print("Routing key:")
        print(message.routing_key)
        print("Message body:")
        jsonBody = json.loads(str(message.body, 'utf-8'))
        print(jsonBody)

async def connectToStreamingApi(loop):
    try:
        if clientId == "<clientId>" or clientSecret == "<clientSecret>":
            print("Please replace <clientId> and <clientSecret> at the top of main.py")
            loop.stop()
            return

        # Authentication
        bearerToken = getAccessToken()
        streamApiInfo = getStreamApiInfo(bearerToken)

        # Define connection parameters using the connection string
        url = streamApiInfo["url"]
        idx = url.index('@')
        streamingApiUrl = url[:idx] + ':' + url[idx:] + "?no_verify_ssl=1"

        # Establish connection to RabbitMQ
        connection = await connect_robust(
            url=streamingApiUrl,
            loop=loop,
            timeout=60,
            ssl=False,
            ssl_options=None
        )
        channel = await connection.channel()

        # Creating routing key
        routingKey = "*.*.*.*" # This key will get all messages
        # Routing key format: <OrganizationID>.<LocationID>.<Type>.<Method>
        # here are some other examples of routing keys to demonstrate how specific you can be
        # "1234.*.*.*" Get all messages for a specific organization
        # "1234.1234567890.*.*" Get all messages for a specific location
        # "1234.1234567890.AppointmentV1.*" Get all AppointmentV1 messages for a specific location
        # "1234.*.AppointmentV1.UPDATE" Get all UPDATE AppointmentV1 messages for a specific organization

        # Get exchange name
        exchangeName = streamApiInfo["exchanges"]

        # Name your queue
        # you can name this whatever you want but you need to have the exchange as a prefix
        queueName = f"{exchangeName}.exampleQueue"

        # Create queue if it doesn't already exist
        # durable: Survive reboots of the broker
        # auto_delete: Delete after all consumers cancels or disconnects
        # exclusive: Exclusive queues may only be accessed by the current connection, and are deleted when that connection closes
        queue = await channel.declare_queue(
            queueName,
            durable=False,
            auto_delete=True,
            exclusive=False
        )

        # Bind the queue to the exchange with a routing key
        await queue.bind(exchange=exchangeName, routing_key=routingKey)

        # Set up a consumer for that queue you just created
        await queue.consume(callback=messageCallback)

        print()
        print("Successfully connected to the StreamingAPI!")
        print("Waiting for messages. To exit press CTRL+C")
    except:
        print()
        print("UnexpectedError:", sys.exc_info())
        loop.stop()

def init():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(connectToStreamingApi(loop))
    loop.run_forever()

if __name__ == "__main__":
    init()