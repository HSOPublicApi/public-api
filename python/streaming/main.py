import sys
import json
import asyncio
import requests
from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage
import util

# Load configuration from config.py via util module
baseUrl = util.baseUrl  # Henry Schein One base URL (test or prod based on config)
clientId = util.getClientId()
clientSecret = util.getClientSecret()

def printResponse(requestName, response):
    print()
    print(requestName)
    print("status code: " + str(response.status_code))
    print(json.dumps(response.json(), indent = 2))

def getAccessToken():
    url = baseUrl + "/oauth/client_credential/accesstoken?grant_type=client_credentials"
    headerData = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": clientId,
        "client_secret": clientSecret
    }
    response = requests.post(url, data = body, headers = headerData)
    printResponse("getAccessToken", response)
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
    printResponse("getStreamApiInfo", response)

    return response.json()

# Define a callback function to display messages in the console
async def messageCallback(message: AbstractIncomingMessage) -> None:
    async with message.process():
        print()
        print("Routing key:")
        print(message.routing_key)
        print("Message headers:")
        print(message.headers)
        print("Message body:")
        jsonBody = json.loads(str(message.body, 'utf-8'))
        print(jsonBody)

async def connectToStreamingApi(loop):
    try:
        if clientId == "<clientId>" or clientSecret == "<clientSecret>":
            print("Please create config.py from config.py.example and fill in your clientId and clientSecret")
            loop.stop()
            return

        # Authentication
        print("Step 1: Getting access token...")
        bearerToken = getAccessToken()
        print(f"✓ Access token obtained: {bearerToken[:20]}...")
        
        print("\nStep 2: Getting streaming API info...")
        streamApiInfo = getStreamApiInfo(bearerToken)
        print(f"✓ API response received. Keys in response: {list(streamApiInfo.keys())}")
        print(f"Full response: {json.dumps(streamApiInfo, indent=2)}")
        
        # Check if the response has the expected structure
        if "url" not in streamApiInfo:
            print("\n❌ ERROR: The API response doesn't contain a 'url' key!")
            print("This might indicate:")
            print("  - Authentication failed (check your clientId and clientSecret)")
            print("  - API endpoint changed")
            print("  - Network/API issue")
            print(f"\nFull response received: {json.dumps(streamApiInfo, indent=2)}")
            loop.stop()
            return

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