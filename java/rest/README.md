# Java RESTful API example

## How to install Java 21 and Maven if you don't already have them
1. Run the following brew commands
```bash
brew install openjdk@21
brew install maven
```
2. Add the following lines to the end of your profile or bash_profile or .zshrc
```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
export PATH="$JAVA_HOME/bin:$PATH"
```
3. Now you can check that it's installed and the path is setup using the following commands. You may need to restart the terminal.
```bash 
java -version
mvn -version
```

## Starting the application for the first time:
1. Replace $${\color{orange}clientId}$$ and $${\color{orange}clientSecret}$$ with your organizations values
  * The values you need to replace can be found in src/main/resources/application.properties
  * $${\color{orange}THESE \space VALUES \space SHOULD \space BE \space KEPT \space SECRET!}$$
  * If you copy this code, these values should be moved to a protected file that is included in your .gitignore
2. Build the application
```bash
mvn clean package -DskipTests
```
3. Start application
```bash
java -jar target/papi-sample-0.0.1-SNAPSHOT.jar
```

## Starting the application again:
1. Build the application (if you made changes)
```bash
mvn clean package -DskipTests
```
2. Start application
```bash
java -jar target/papi-sample-0.0.1-SNAPSHOT.jar
```

## Project Structure

```
src/main/java/com/hs1/
├── model/           # Data models
├── service/         # API service implementations
├── Authenticator.java   # OAuth2 authentication
├── AppConfig.java      # Spring configuration
├── DemoRunner.java     # Example usage
└── RestApiApp.java     # Main application
```

## Troubleshooting

1. **Java version issues:**
```bash
# Check Java version
java -version

# If not Java 21, set JAVA_HOME
export JAVA_HOME=/path/to/java21
export PATH=$JAVA_HOME/bin:$PATH

# Verify Maven is using correct Java
mvn -version
```

2. **Maven/Spring Boot plugin issues:**
   - Ensure Maven is using Java 21 (not Java 11)
   - The Spring Boot 3.x requires Java 17+
   - Use `mvn -version` to verify Java version

3. **Shell environment issues:**
```bash
# Use bash explicitly if needed
bash -c 'export JAVA_HOME=/path/to/java21 && export PATH=$JAVA_HOME/bin:$PATH && mvn clean package'
```

4. **API Connection issues:**
   - Verify your client ID and secret
   - Check network connectivity to API endpoints
   - Review logs for detailed error messages 