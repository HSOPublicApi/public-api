# Java StreamingAPI Example

## Prerequisites

### Java Development Kit (JDK)
Make sure you have Java 11 or higher installed:
```bash
java -version
```

If you don't have Java installed, you can install it using:
```bash
# On macOS with Homebrew
brew install openjdk@11

# On Ubuntu/Debian
sudo apt-get install openjdk-11-jdk

# On CentOS/RHEL
sudo yum install java-11-openjdk-devel
```

### Maven
Make sure you have Maven installed:
```bash
mvn -version
```

If you don't have Maven installed:
```bash
# On macOS with Homebrew
brew install maven

# On Ubuntu/Debian
sudo apt-get install maven

# On CentOS/RHEL
sudo yum install maven
```

## Starting the application for the first time:

1. Replace $${\color{orange}clientId}$$ and $${\color{orange}clientSecret}$$ with your organization's values
   * The values you need to replace can be found near the top of `Main.java`
   * $${\color{orange}THESE \space VALUES \space SHOULD \space BE \space KEPT \space SECRET!}$$
   * If you copy this code, these values should be moved to a protected file that is included in your `.gitignore`

2. Navigate to the streaming directory:
```bash
cd java/streaming
```

3. Install dependencies and compile:
```bash
mvn clean compile
```

4. Run the application:
```bash
mvn exec:java
```

## Alternative ways to run the application:

### Using Maven to create a runnable JAR:
```bash
mvn clean package
java -jar target/streaming-api-example-1.0-SNAPSHOT.jar
```

### Using Maven to run directly:
```bash
mvn clean compile exec:java -Dexec.mainClass="Main"
```

### Compiling and running manually:
```bash
# Compile with dependencies on classpath
mvn dependency:copy-dependencies
javac -cp "target/dependency/*" Main.java

# Run with dependencies on classpath
java -cp ".:target/dependency/*" Main
```

## What this example does:

1. **Authentication**: Uses OAuth2 client credentials flow to get an access token
2. **API Discovery**: Retrieves streaming API connection information
3. **RabbitMQ Connection**: Connects to the message broker using the provided connection details
4. **Message Consumption**: Sets up a consumer to receive and process streaming messages
5. **Message Processing**: Displays routing keys, headers, and JSON message bodies

## Routing Key Examples:

The example uses `*.*.*.*` to receive all messages, but you can be more specific:

- `1234.*.*.*` - Get all messages for organization ID 1234
- `1234.1234567890.*.*` - Get all messages for a specific location
- `1234.1234567890.AppointmentV1.*` - Get all AppointmentV1 messages for a specific location
- `1234.*.AppointmentV1.UPDATE` - Get all UPDATE AppointmentV1 messages for a specific organization

## Dependencies:

- **RabbitMQ AMQP Client** - For connecting to the message broker
- **OkHttp** - For making HTTP requests to the REST API
- **Jackson** - For JSON parsing and processing
- **SLF4J** - For logging

## Notes:

- The application will run continuously until interrupted (Ctrl+C)
- Make sure your client credentials have the necessary permissions for the streaming API
- The queue is created as non-durable and auto-delete for this example
- In production, you may want to implement proper error handling and reconnection logic 