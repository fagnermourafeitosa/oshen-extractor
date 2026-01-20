import asyncio
import logging
import httpx
from tabulate import tabulate
from src.core.config import settings

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("check-webhooks")

async def check_evolution_webhooks():
    if not settings.EVOLUTION_API_URL or not settings.EVOLUTION_API_KEY:
        print("Error: EVOLUTION_API_URL or EVOLUTION_API_KEY not configured.")
        return

    base_url = settings.EVOLUTION_API_URL.rstrip("/")
    headers = {
        "apikey": settings.EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        # 1. Fetch all instances
        print(f"Fetching instances from {base_url}...")
        try:
            resp = await client.get(f"{base_url}/instance/fetchInstances", headers=headers)
            resp.raise_for_status()
            instances = resp.json()
        except Exception as e:
            print(f"Failed to fetch instances: {e}")
            return

        if not instances:
            print("No instances found.")
            return

        table_data = []

        # 2. Check webhook for each instance
        for instance in instances:
            name = instance.get("name", "Unknown")
            status = instance.get("connectionStatus", "Unknown")
            
            webhook_url = "None"
            enabled = "-"
            events = "-"
            
            try:
                # Evolution API v2: /webhook/find/:instanceName
                wh_resp = await client.get(f"{base_url}/webhook/find/{name}", headers=headers)
                
                if wh_resp.status_code == 200:
                    wh_data = wh_resp.json()
                    # If webhook is configured, it returns the object, otherwise might return null or empty?
                    # Based on manual check, returns JSON with url, enabled, etc.
                    if wh_data and "url" in wh_data:
                        webhook_url = wh_data.get("url")
                        enabled = "Yes" if wh_data.get("enabled") else "No"
                        events_list = wh_data.get("events", [])
                        events = ", ".join(events_list) if events_list else "None"
            except Exception:
                # If error (e.g. 404 or 500), assume no webhook or error fetching
                pass

            table_data.append([name, status, webhook_url, enabled, events])

    # 3. Print Table
    headers = ["Instance", "Status", "Webhook URL", "Enabled", "Events"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="github"))

if __name__ == "__main__":
    # Ensure tabulate is installed or handle if not (user might need to install it)
    # pip install tabulate
    try:
        asyncio.run(check_evolution_webhooks())
    except ImportError:
        print("Please install tabulate: pip install tabulate")
