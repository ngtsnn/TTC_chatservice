from http.client import HTTPException
from fastapi import APIRouter, Response
from . api.index import router as apiRouter

router = APIRouter()


router.include_router(apiRouter, prefix="/api")


@router.get("/")
async def root():
  return {
    "message": "Hello from chat service"
  }