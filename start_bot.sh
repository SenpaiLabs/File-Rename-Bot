#!/bin/bash
# SenpaiLabs File Rename Bot - Environment Setup Script
# This script properly loads .env file with special characters

set -a  # Export all variables
source .env
set +a  # Stop exporting

# Verify required variables
if [ -z "$BOT_TOKEN" ] || [ -z "$API_ID" ] || [ -z "$API_HASH" ]; then
    echo "❌ Error: Missing required environment variables in .env file"
    echo "Please check BOT_TOKEN, API_ID, and API_HASH"
    exit 1
fi

echo "✅ Environment loaded successfully"
echo "🤖 Starting SenpaiRenameBot..."
python3 bot.py
