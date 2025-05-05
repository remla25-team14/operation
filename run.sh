#!/bin/bash
# Read version from VERSION file
export APP_VERSION=$(cat ../app/VERSION)
echo "Using App Version: $APP_VERSION"

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
  echo "WARNING: GITHUB_TOKEN environment variable is not set."
  echo "The model service might not be able to download model artifacts."
  echo "Set it with: export GITHUB_TOKEN=your_github_token"
fi

docker-compose down && docker-compose up --build -d

echo "Application started!"
echo "- Frontend+Backend: http://localhost:5001"
echo "- Model Service: http://localhost:5002" 