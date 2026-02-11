#!/bin/bash

# LeadFinder Dev Utility Script

PROJECT_DIR="/home/gzyms/Dev Projects/LeadFinder"
VENV_PATH="$PROJECT_DIR/venv"
SCRAPER_IMAGE="ghcr.io/gzyms69/google-maps-scraper:latest"

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
    
    # 1. Kill ANY running scraper containers (searching by image name)
    CONTAINER_IDS=$(docker ps -a -q --filter "ancestor=ghcr.io/gzyms69/google-maps-scraper")
    
    if [ -n "$CONTAINER_IDS" ]; then
        echo "Stopping and removing scraper containers..."
        docker stop $CONTAINER_IDS > /dev/null 2>&1
        docker rm $CONTAINER_IDS > /dev/null 2>&1
    else
        echo "No active scraper containers found."
    fi

    # 2. Kill orphan scraper binaries (handling root processes if needed)
    if pgrep -f "google-maps-scraper" > /dev/null; then
        echo "Terminating orphaned scraper processes..."
        sudo pkill -9 -f "google-maps-scraper"
    fi

    # 3. Kill any orphan python processes from this project
    pkill -f "src/main.py"
    pkill -f "src/filter_leads.py"
    
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
