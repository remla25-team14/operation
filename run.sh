#!/bin/bash

echo "Starting Sentiment Analysis Application..."
echo "----------------------------------------"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

# Check for docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed or not in PATH"
    exit 1
fi

# Check for GitHub token in secrets
if [ ! -f "./secrets/github_token.txt" ]; then
    echo "Warning: GitHub token file not found"
    echo "Creating placeholder file in secrets/github_token.txt"
    echo "Please replace with your actual GitHub token before using the model service"
    mkdir -p secrets
    echo "your_github_token_here" > secrets/github_token.txt
fi

# Start the application
echo "Launching services..."
docker-compose up 