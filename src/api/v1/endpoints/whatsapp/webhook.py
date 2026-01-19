import logging
from fastapi import Request, APIRouter, Depends
from src.services.whatsapp.use_cases.process_webhook import ProcessWebhookUseCase

router = APIRouter()
logger = logging.getLogger(__name__)

class WhatsAppWebhookHandler:
    def __init__(self, use_case: ProcessWebhookUseCase = Depends()):
        self.use_case = use_case

    async def handle_webhook(self, req: Request):
        return await self.use_case.execute(req)

@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    handler: WhatsAppWebhookHandler = Depends()
):
    return await handler.handle_webhook(request)
