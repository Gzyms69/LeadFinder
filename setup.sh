#!/bin/bash

# LeadFinder Setup Script
# This script automates the environment setup for new users.

echo "--- Starting LeadFinder Setup ---"

# 1. Create necessary directories
echo "Creating directories..."
mkdir -p raw_data processed_data config

# 2. Check for Python
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 could not be found. Please install Python 3.10+."
    exit 1
fi

# 3. Create Virtual Environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 4. Install Dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Handle Configuration Examples
if [ ! -f "config/query.json" ]; then
    echo "Creating config/query.json from example..."
    cp config/query.json.example config/query.json
fi

if [ ! -f "config/service_account.json" ]; then
    echo "Reminder: Please place your Google Service Account JSON file at config/service_account.json"
fi

echo "--- Setup Complete ---"
echo "Next steps:"
echo "1. Configure config/query.json with your Spreadsheet ID and search parameters."
echo "2. Place your Google Service Account credentials in config/service_account.json."
echo "3. Share your Google Sheet with the client_email found in your service_account.json."
echo "4. Run the tool: source venv/bin/activate && python3 src/main.py"
