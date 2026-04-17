#!/bin/bash
set -e

# Docker entrypoint script for Marketing Planning Assistant

echo "=========================================="
echo "Marketing Planning Assistant - Starting"
echo "=========================================="

# Function to check if a command exists
command_exists() {
    command -v "$@" > /dev/null 2>&1
}

# Wait for database if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
    echo "Waiting for database to be ready..."
    max_attempts=30
    attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if python -c "
import os
from urllib.parse import urlparse

db_url = os.getenv('DATABASE_URL')
if db_url:
    parsed = urlparse(db_url)
    import socket
    try:
        socket.create_connection((parsed.hostname, parsed.port or 5432), timeout=2)
        print('Database is ready!')
        exit(0)
    except:
        exit(1)
"; then
            break
        fi
        
        attempt=$((attempt + 1))
        echo "Database not ready yet (attempt $attempt/$max_attempts). Retrying in 2 seconds..."
        sleep 2
    done
    
    if [ $attempt -eq $max_attempts ]; then
        echo "ERROR: Database connection failed after $max_attempts attempts"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "[WARNING] .env file not found. Using environment variables."
fi

# Run database migrations if they exist
if [ -f "migrations/apply.py" ]; then
    echo "Running database migrations..."
    python migrations/apply.py
fi

# Execute the main command
echo "Starting application..."
exec "$@"
