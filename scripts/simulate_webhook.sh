#!/bin/bash

URL="http://localhost:9009/api/v1/whatsapp/webhook"

echo "Sending webhook to $URL..."

curl -X POST "$URL" \
     -H "Content-Type: application/json" \
     -H "x-token: 12345" \
     -d '{
  "event": "MESSAGES_UPSERT",
  "instance": "oshen",
  "data": {
    "key": {
      "remoteJid": "123456789@g.us",
      "fromMe": false,
      "id": "TestMessageID"
    },
    "pushName": "John Doe",
    "message": {
      "conversation": "Hello from simulation!"
    },
    "messageTimestamp": 1678886400
  }
}'

echo -e "\nDone."
