#!/bin/bash

# Enhanced Java PAPI Demo Runner
# This script runs the enhanced Java application that matches the Python workflow

echo "=== Enhanced Java PAPI Demo ==="
echo "Starting application that now matches Python workflow..."
echo ""

# Set Java environment
export JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
export PATH="$JAVA_HOME/bin:$PATH"

# Navigate to the correct directory
cd "$(dirname "$0")"

# Check if JAR exists
if [ ! -f "target/papi-sample-0.0.1-SNAPSHOT.jar" ]; then
    echo "ERROR: JAR file not found. Please run 'mvn clean package -DskipTests' first."
    exit 1
fi

# Run the application
echo "Running enhanced Java application with detailed API logging..."
echo "This will demonstrate the same workflow as the Python version:"
echo "1. Get locations, patients, providers, operatories"
echo "2. Create appointment with detailed response"
echo "3. Update appointment (LATE → HERE)"
echo "4. Get appointment by ID"
echo "5. Delete appointment"
echo ""

java -jar target/papi-sample-0.0.1-SNAPSHOT.jar 