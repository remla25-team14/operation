#!/bin/bash

echo "Starting Sentiment Analysis Application..."
echo "----------------------------------------"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

# Check for docker compose (v2)
if ! docker compose version &> /dev/null; then
    echo "Error: docker compose (v2) is not available"
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

# If MODEL_SERVICE_IMAGE is set, extract the tag and set MODEL_SERVICE_IMAGE_TAG
if [ -n "$MODEL_SERVICE_IMAGE" ]; then
    TAG="${MODEL_SERVICE_IMAGE##*:}"
    if [ "$TAG" = "$MODEL_SERVICE_IMAGE" ]; then
        TAG="latest"
    fi
    export MODEL_SERVICE_IMAGE_TAG="$TAG"
fi

# Start the application
echo "Launching services..."
docker compose up --build 