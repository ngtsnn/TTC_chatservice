from fastapi import APIRouter
from .messages.index import router as messagesRoutes

router = APIRouter()
router.include_router(messagesRoutes, prefix="/messages")



