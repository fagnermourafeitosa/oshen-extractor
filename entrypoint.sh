#!/bin/bash
set -e

# Run the webhook configuration script in the background
# We wait a few seconds to ensure the API might be up, or we just run it. 
# Actually, since this is an independent script communicating with another service (Evolution),
# it doesn't strictly depend on *this* API being fully up, BUT it tells Evolution where to find *this* API.
# So it's fine to run before the main process, or in parallel.
# However, if we run it before, the API isn't up yet, so if Evolution immediately tries to ping, it might fail?
# Evolution usually doesn't ping on 'set'.

echo "Configuring Evolution Webhook..."
python -m src.scripts.configure_webhook &

echo "Starting Oshen Extractor API..."
exec uvicorn src.main:app --host 0.0.0.0 --port 9009
