import http from 'http';
import axios from 'axios';
import amqplib from 'amqplib';
import { getConfigs } from './config/base.js';

const config = getConfigs();
const server = http.createServer();

async function getAccessToken() {
    try {
        const url = `${config.baseURL}/oauth/client_credential/accesstoken?grant_type=client_credentials`;
        const response = await axios.post(url,
            {
                client_id: config.clientId,
                client_secret: config.clientSecret
            },
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }
        );

        return `${response.data.token_type} ${response.data.access_token}`;
    } catch (error) {
        console.error('Error getting access token:', error.message);
        throw error;
    }
}

// Get streaming API info
async function getStreamApiInfo(bearerToken) {
    try {
        const url = `${config.baseURL}/ascend-streaming-api/url`;
        const response = await axios.get(url, {
            headers: {
                'Authorization': bearerToken,
                'Content-Type': 'application/json'
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error getting stream API info:', error.message);
        throw error;
    }
}

// Message callback function
function messageCallback(msg) {
    if (msg) {
        console.log('\nRouting key:', msg.fields.routingKey);
        console.log('Message headers:', msg.properties.headers);
        console.log('Message body:', JSON.parse(msg.content.toString()));
    }
}

// Connect to streaming API
async function connectToStreamingApi() {
  console.log('Connecting to Streaming Api...');

    try {
        if (!config.clientId || !config.clientSecret) {
            console.error('Please replace <clientId> and <clientSecret> in config/base.js');
            return;
        }

        // Authentication
        const bearerToken = await getAccessToken();
        const streamApiInfo = await getStreamApiInfo(bearerToken);

        // Prepare connection URL
        let url = streamApiInfo.url;
        const idx = url.indexOf('@');
        const streamingApiUrl = url.slice(0, idx) + ':' + url.slice(idx) + "?no_verify_ssl=1";

        // Connect to RabbitMQ
        const connection = await amqplib.connect(streamingApiUrl, {
            timeout: 60000,
            ssl: false
        });
        const channel = await connection.createChannel();

        // Create routing key
        const routingKey = "*.*.*.*"; // This key will get all messages
        // Routing key format: <OrganizationID>.<LocationID>.<Type>.<Method>
        // Examples:
        // "1234.*.*.*" - Get all messages for a specific organization
        // "1234.1234567890.*.*" - Get all messages for a specific location
        // "1234.1234567890.AppointmentV1.*" - Get all AppointmentV1 messages for a specific location
        // "1234.*.AppointmentV1.UPDATE" - Get all UPDATE AppointmentV1 messages for a specific organization

        const exchangeName = streamApiInfo.exchanges;
        const queueName = `${exchangeName}.exampleQueue`;

        // Declare queue
        await channel.assertQueue(queueName, {
            durable: false,
            autoDelete: true,
            exclusive: false
        });

        // Bind queue to exchange with routing key
        await channel.bindQueue(queueName, exchangeName, routingKey);

        // Set up consumer
        await channel.consume(queueName, messageCallback, {
            noAck: true
        });

        console.log('\nSuccessfully connected to the StreamingAPI!');
        console.log('Waiting for messages. To exit press CTRL+C');

        // Handle connection closure
        process.on('SIGINT', async () => {
            await channel.close();
            await connection.close();
            process.exit(0);
        });

    } catch (error) {
        console.error('\nUnexpected Error:', error);
        process.exit(1);
    }
}

server.listen(config.port, async () => {
  console.log(`Server running on port: ${config.port}`);
  await connectToStreamingApi();
});