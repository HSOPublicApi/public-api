import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import okhttp3.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    private static final String BASE_URL = "https://prod.hs1api.com"; // Henry Schein One base URL
    
    // Get credentials from environment variables
    private static final String CLIENT_ID = System.getenv().getOrDefault("CLIENT_ID", "<clientId>");
    private static final String CLIENT_SECRET = System.getenv().getOrDefault("CLIENT_SECRET", "<clientSecret>");
    
    // Limit the number of messages to receive
    private static final int MAX_MESSAGES = 10;
    private static final AtomicInteger messageCount = new AtomicInteger(0);
    
    private static final OkHttpClient httpClient = new OkHttpClient();
    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    public static void main(String[] args) {
        try {
            if ("<clientId>".equals(CLIENT_ID) || "<clientSecret>".equals(CLIENT_SECRET)) {
                System.out.println("Please set CLIENT_ID and CLIENT_SECRET environment variables");
                System.out.println("Example:");
                System.out.println("  export CLIENT_ID=your_client_id_here");
                System.out.println("  export CLIENT_SECRET=your_client_secret_here");
                return;
            }
            
            // Authentication
            String bearerToken = getAccessToken();
            JsonNode streamApiInfo = getStreamApiInfo(bearerToken);
            
            // Connect to streaming API
            connectToStreamingApi(streamApiInfo);
            
        } catch (Exception e) {
            System.err.println("Unexpected error: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static void printResponse(String requestName, Response response) throws IOException {
        System.out.println();
        System.out.println(requestName);
        System.out.println("status code: " + response.code());
        String responseBody = response.body().string();
        
        try {
            JsonNode jsonNode = objectMapper.readTree(responseBody);
            System.out.println(objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(jsonNode));
        } catch (Exception e) {
            System.out.println(responseBody);
        }
    }
    
    private static String getAccessToken() throws IOException {
        String url = BASE_URL + "/oauth/client_credential/accesstoken?grant_type=client_credentials";
        
        RequestBody formBody = new FormBody.Builder()
                .add("client_id", CLIENT_ID)
                .add("client_secret", CLIENT_SECRET)
                .build();
        
        Request request = new Request.Builder()
                .url(url)
                .post(formBody)
                .addHeader("Content-Type", "application/x-www-form-urlencoded")
                .build();
        
        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Failed to get access token: " + response);
            }
            
            String responseBody = response.body().string();
            JsonNode jsonResponse = objectMapper.readTree(responseBody);
            
            return jsonResponse.get("token_type").asText() + " " + jsonResponse.get("access_token").asText();
        }
    }
    
    private static JsonNode getStreamApiInfo(String bearerToken) throws IOException {
        String url = BASE_URL + "/ascend-streaming-api/url";
        
        Request request = new Request.Builder()
                .url(url)
                .get()
                .addHeader("Authorization", bearerToken)
                .addHeader("Content-Type", "application/json")
                .build();
        
        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Failed to get stream API info: " + response);
            }
            
            String responseBody = response.body().string();
            return objectMapper.readTree(responseBody);
        }
    }
    
    private static void connectToStreamingApi(JsonNode streamApiInfo) throws IOException, TimeoutException {
        // Extract connection information
        String url = streamApiInfo.get("url").asText();
        String exchangeName = streamApiInfo.get("exchanges").asText();
        
        // Parse the RabbitMQ connection URL
        // Format: amqp://username:password@host:port/vhost
        ConnectionFactory factory = new ConnectionFactory();
        try {
            factory.setUri(url);
            factory.setConnectionTimeout(60000); // 60 seconds
        } catch (Exception e) {
            throw new IOException("Failed to parse connection URL: " + e.getMessage(), e);
        }
        
        try (com.rabbitmq.client.Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {
            
            // Creating routing key
            String routingKey = "*.*.*.*"; // This key will get all messages
            // Routing key format: <OrganizationID>.<LocationID>.<Type>.<Method>
            // Here are some other examples of routing keys to demonstrate how specific you can be:
            // "1234.*.*.*" Get all messages for a specific organization
            // "1234.1234567890.*.*" Get all messages for a specific location
            // "1234.1234567890.AppointmentV1.*" Get all AppointmentV1 messages for a specific location
            // "1234.*.AppointmentV1.UPDATE" Get all UPDATE AppointmentV1 messages for a specific organization
            
            // Name your queue
            // You can name this whatever you want but you need to have the exchange as a prefix
            String queueName = exchangeName + ".exampleQueue";
            
            // Create queue if it doesn't already exist
            // durable: Survive reboots of the broker
            // autoDelete: Delete after all consumers cancel or disconnect
            // exclusive: Exclusive queues may only be accessed by the current connection, and are deleted when that connection closes
            channel.queueDeclare(queueName, false, false, true, null);
            
            // Bind the queue to the exchange with a routing key
            channel.queueBind(queueName, exchangeName, routingKey);
            
            System.out.println();
            System.out.println("Successfully connected to the StreamingAPI!");
            System.out.println("Waiting for messages (will stop after " + MAX_MESSAGES + " messages). To exit early, press CTRL+C");
            
            // Define a callback function to display messages in the console
            DeliverCallback deliverCallback = (consumerTag, delivery) -> {
                try {
                    int currentCount = messageCount.incrementAndGet();
                    
                    System.out.println();
                    System.out.println("=== Message " + currentCount + " of " + MAX_MESSAGES + " ===");
                    System.out.println("Routing key:");
                    System.out.println(delivery.getEnvelope().getRoutingKey());
                    System.out.println("Message headers:");
                    System.out.println(delivery.getProperties().getHeaders());
                    System.out.println("Message body:");
                    
                    String messageBody = new String(delivery.getBody(), StandardCharsets.UTF_8);
                    try {
                        JsonNode jsonBody = objectMapper.readTree(messageBody);
                        System.out.println(objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(jsonBody));
                    } catch (Exception e) {
                        System.out.println(messageBody);
                    }
                    
                    // Check if we've reached the message limit
                    if (currentCount >= MAX_MESSAGES) {
                        System.out.println();
                        System.out.println("Received " + MAX_MESSAGES + " messages. Stopping...");
                        // Close the connection to stop receiving messages
                        try {
                            channel.close();
                            connection.close();
                        } catch (Exception e) {
                            System.err.println("Error closing connection: " + e.getMessage());
                        }
                        System.exit(0);
                    }
                } catch (Exception e) {
                    System.err.println("Error processing message: " + e.getMessage());
                }
            };
            
            CancelCallback cancelCallback = consumerTag -> {
                System.out.println("Consumer was cancelled: " + consumerTag);
            };
            
            // Set up a consumer for the queue
            channel.basicConsume(queueName, true, deliverCallback, cancelCallback);
            
            // Keep the main thread alive to continue receiving messages
            // In a real application, you might want to use a different approach
            try {
                Thread.currentThread().join();
            } catch (InterruptedException e) {
                System.out.println("Application interrupted");
                Thread.currentThread().interrupt();
            }
        }
    }
} 