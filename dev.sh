#!/bin/bash

# LeadFinder Dev Utility Script

PROJECT_DIR="/home/gzyms/Dev Projects/LeadFinder"
VENV_PATH="$PROJECT_DIR/venv"
SCRAPER_IMAGE="gosom/google-maps-scraper"

function start_pipeline() {
    echo "--- [STARTING LEADFINDER] ---"
    
    # Check for Virtual Environment
    if [ ! -d "$VENV_PATH" ]; then
        echo "Error: Virtual environment not found at $VENV_PATH"
        exit 1
    fi

    # Activate and Run
    source "$VENV_PATH/bin/activate"
    python3 "$PROJECT_DIR/src/main.py" "$@"
}

function stop_pipeline() {
    echo "--- [STOPPING LEADFINDER & CLEANING PROCESSES] ---"
    
    # 1. Kill running scraper containers
    CONTAINER_IDS=$(docker ps -q --filter ancestor="$SCRAPER_IMAGE")
    
    if [ -n "$CONTAINER_IDS" ]; then
        echo "Stopping active scraper containers..."
        docker stop $CONTAINER_IDS
    else
        echo "No active scraper containers found."
    fi

    # 2. Kill any orphan python processes from this project
    pkill -f "src/main.py"
    
    echo "Cleanup complete. Memory cleared."
}

case "$1" in
    start)
        shift # Remove 'start' from arguments
        start_pipeline "$@"
        ;;
    stop)
        stop_pipeline
        ;;
    *)
        echo "Usage: ./dev.sh {start|stop} [options]"
        echo "Example: ./dev.sh start --max-reviews 10"
        exit 1
        ;;
esac
