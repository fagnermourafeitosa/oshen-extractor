import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, HttpUrl
from src.services.whatsapp.use_cases.register_instance import RegisterInstanceUseCase

router = APIRouter()
logger = logging.getLogger(__name__)

class RegistrationRequest(BaseModel):
    instanceName: str
    callbackUrl: HttpUrl

class WhatsAppRegistrationHandler:
    def __init__(self, use_case: RegisterInstanceUseCase = Depends()):
        self.use_case = use_case

    async def register_instance(self, request: RegistrationRequest, background_tasks: BackgroundTasks):
        return await self.use_case.execute(
            instance_name=request.instanceName,
            callback_url=str(request.callbackUrl),
            background_tasks=background_tasks
        )

@router.post("/register")
async def register_whatsapp_instance(
    request: RegistrationRequest, 
    background_tasks: BackgroundTasks,
    handler: WhatsAppRegistrationHandler = Depends()
):
    return await handler.register_instance(request, background_tasks)
