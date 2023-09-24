from fastapi import APIRouter
from app.controllers.messages_controller import MessagesController
from app.models.message import Message

router = APIRouter()


@router.post("/messages/whatsapp", tags=["messages"])
async def send_whatsapp_message(request: Message):
    return MessagesController.send_whatsapp_message(request)


@router.post("/messages/sms", tags=["messages"])
async def send_sms_message(request):
    return MessagesController.send_sms_message(request)

@router.get("/messages", tags=["messages"])
async def send_sms_message(to: str, from_: str):
    return MessagesController.get_message_history(to, from_)
