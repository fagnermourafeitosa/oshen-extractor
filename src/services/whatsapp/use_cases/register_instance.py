import logging
from typing import Dict, Any
from fastapi import HTTPException, BackgroundTasks
from src.services.whatsapp.providers.evolution_api import EvolutionApi
from src.core.config import settings

logger = logging.getLogger(__name__)

class RegisterInstanceUseCase:
    """
    Application use case to orchestrate the registration of a new WhatsApp instance.
    Focuses on the business flow: API Creation -> Webhook Configuration -> Mandatory Callback.
    """
    def __init__(self):
        self.api = EvolutionApi()

    async def execute(
        self, 
        instance_name: str, 
        callback_url: str,
        background_tasks: BackgroundTasks
    ) -> Dict[str, Any]:
        try:
            # 1. Create instance
            instance_data = await self.api.create_instance(instance_name)
            
            # 2. Configure Webhook
            target_url = settings.WEBHOOK_PUBLIC_URL.rstrip("/")
            if not target_url.endswith("/evolution"):
                target_url += "/whatsapp/webhook"
            
            await self.api.set_webhook(instance_name, target_url)
            
            # 3. Success Callback (Background)
            background_tasks.add_task(
                self.api.send_callback, 
                callback_url, 
                {"status": "success", "instance": instance_name, "data": instance_data}
            )
            
            return {
                "status": "success", 
                "message": f"Instance {instance_name} registered successfully", 
                "data": instance_data
            }
        except Exception as e:
            logger.error(f"RegisterInstanceUseCase: Failure for {instance_name}: {e}")
            raise HTTPException(status_code=400, detail=str(e))
