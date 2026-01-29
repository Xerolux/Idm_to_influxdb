#!/bin/bash
set -e

# Xerolux 2026

# Ensure we are in the project root
SCRIPT_DIR=$(dirname "$0")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$PROJECT_ROOT"

# Read version
if [ ! -f VERSION ]; then
    echo "Error: VERSION file not found!"
    exit 1
fi

BASE_VERSION=$(cat VERSION | tr -d '[:space:]')
COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Construct APP_VERSION
APP_VERSION="${BASE_VERSION}.${COMMIT_HASH}"

echo "Building Docker image for version: $APP_VERSION"

# Build the image
# Assuming the image name is idm-metrics-collector, adjust if necessary
docker build \
  --build-arg APP_VERSION="$APP_VERSION" \
  -t idm-metrics-collector:latest \
  -t idm-metrics-collector:"$APP_VERSION" \
  .

echo "Build complete."
