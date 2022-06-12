from controllers.messages import MessageController
from dto.message import CreateMessageDTO
from fastapi import APIRouter, Body
from utils.ml import vectorizer, MNB

controller = MessageController()

router = APIRouter()

@router.get("/")
async def get():
  return await controller.getAll()

@router.post("/")
async def createOne(message: CreateMessageDTO = Body()):

  msg = message["msg"]
  transformedMsg = vectorizer.transform([msg])
  predict = MNB.predict(transformedMsg)
  message["isToxic"] = bool(predict[0])
  return await controller.createOne(message.__dict__)