#!/bin/bash

# ==============================================================================
# OSHEN REMOTE MANAGEMENT SCRIPT (MAC MINI)
# ==============================================================================
# Usage: ./scripts/remote-mini.sh "your-command-here"
# Example: ./scripts/remote-mini.sh "docker ps"
# ==============================================================================

# Credentials
REMOTE_USER="macprom1"
REMOTE_PASS="Waldo228!"
REMOTE_IP="192.168.0.23"

# Check if command is provided
if [ -z "$1" ]; then
    echo "❌ Error: No command provided."
    echo "Usage: $0 \"command\""
    exit 1
fi

# Determine if sshpass is available
if command -v sshpass >/dev/null 2>&1; then
    # Run using sshpass (non-interactive)
    sshpass -p "$REMOTE_PASS" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_IP" "$1"
else
    # Fallback to standard ssh (will prompt for password if keys are not set)
    echo "⚠️  Note: 'sshpass' is not installed. Manual password entry may be required."
    echo "💡 To automate this, run: brew install hudochenkov/sshpass/sshpass"
    ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_IP" "$1"
fi
