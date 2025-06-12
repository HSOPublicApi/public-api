# Java RESTful API Example

## How to install Java 11 and Maven if you don't already have them
1. Run the following brew commands
```bash
brew install openjdk@11
brew install maven
```
2. Add the following lines to the end of your profile or bash_profile or .zshrc
```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home"
export PATH="$JAVA_HOME/bin:$PATH"
```
3. Now you can check that it's installed and the path is setup using the following commands. You may need to restart the terminal.
```bash 
java -version
mvn -version
```

## Starting the application for the first time:
1. Set up your credentials:
   * Create a `.env` file in the project root (this file should be in your .gitignore)
   * Add your credentials to the `.env` file:
   ```
   # Required credentials
   CLIENT_ID=your_client_id_here
   CLIENT_SECRET=your_client_secret_here
   ORGANIZATION_ID=your_organization_id_here
   ```
   * **NEVER commit credentials to version control!**
   * The application will read these environment variables automatically
   * For development, you can also set them directly in your terminal:
   ```bash
   export CLIENT_ID=your_client_id_here
   export CLIENT_SECRET=your_client_secret_here
   export ORGANIZATION_ID=your_organization_id_here
   ```

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

## What the application does:
This demo shows how to use the Henry Schein One API to:
1. Get required data (locations, patients, providers, operatories)
2. Create an appointment
3. Update the appointment
4. Get the appointment by ID
5. Delete the appointment

Each API call will show detailed request/response information.

## Alternative way to run:
You can also run the application directly with Maven:
```bash
mvn spring-boot:run
```

## API Features

### Available Operations
- **Locations**: Retrieve location data
- **Patients**: Retrieve patient data
- **Providers**: Retrieve provider data  
- **Operatories**: Retrieve operatory data
- **Appointments**: Create, read, update, delete appointments

### Pagination
All API endpoints are limited to **maximum 5 results** for performance:
- Reduces response size and network overhead
- Improves response times
- Configurable via `MAX_PAGE_SIZE` constant

### Response Logging
Every API call displays detailed request/response information including:
- Operation name
- HTTP status code
- Pretty-printed JSON response

## Architecture

### Template Method Pattern
The application uses a `TemplateMethodService<T>` base class that provides common CRUD operations:
- `findAll()` - Retrieve all entities (paginated)
- `findById(String id)` - Retrieve entity by ID
- `create(Map<String, Object> data)` - Create new entity
- `update(String id, Map<String, Object> data)` - Update existing entity
- `delete(String id)` - Delete entity

### Service Classes
Each entity has its own service class extending `TemplateMethodService`:
- `AppointmentService` - Appointment management
- `LocationService` - Location data retrieval
- `PatientService` - Patient data retrieval
- `ProviderService` - Provider data retrieval
- `OperatoryService` - Operatory data retrieval

## Project Structure
```
src/main/java/com/hs1/
├── model/                    # Data models
│   ├── Appointment.java
│   ├── Location.java
│   ├── Patient.java
│   └── ...
├── service/                  # API service implementations
│   ├── TemplateMethodService.java  # Base CRUD operations
│   ├── AppointmentService.java
│   ├── LocationService.java
│   └── ...
├── util/                     # Utility classes
│   └── ApiUtil.java         # Response logging utilities
├── Authenticator.java        # OAuth2 authentication
├── AppConfig.java           # Spring configuration
├── DemoRunner.java          # Example usage workflow
└── RestApiApp.java          # Main application class
```

## Troubleshooting

### Java Version Issues
```bash
# Check Java version
java -version

# Set JAVA_HOME if needed
export JAVA_HOME=/path/to/java21
export PATH=$JAVA_HOME/bin:$PATH

# Verify Maven is using correct Java
mvn -version
```

### API Connection Issues
- Verify your client ID and secret are correct
- Check network connectivity to API endpoints
- Review application logs for detailed error messages
- Ensure organization ID is valid

### Build Issues
```bash
# Clean and rebuild
mvn clean compile

# Skip tests if needed
mvn clean package -DskipTests
```

## Example Output
When you run the application, you'll see output like:
```
=== Starting PAPI Demo ===
=== Step 1: Getting required data ===
getLocations
status code: 200
{
  "statusCode": 200,
  "data": [...]
}

=== Step 2: Creating appointment ===
createAppointment
status code: 201
...
```

## Customization
- Modify `MAX_PAGE_SIZE` in `TemplateMethodService` to change result limits
- Add new entity services by extending `TemplateMethodService`
- Customize logging format in `logResponse()` method
- Update appointment data structure in `getAppointmentData()`