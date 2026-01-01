#!/bin/bash
set -e

echo "Building Docker image..."
docker build -t oshen-extractor .

echo "Starting Oshen Extractor API (Docker)..."
# Using -it to allow interactive Ctrl+C and logs
docker run --rm -it -p 9009:9009 oshen-extractor
