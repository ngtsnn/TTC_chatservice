from http.client import UNAUTHORIZED
from controllers.messages import MessageController
from dto.message import CreateMessageDTO
from fastapi import APIRouter, Body, HTTPException, Header
from typing import Union
from utils.ml import vectorizer, MNB, preprocess
from jose import JWTError, jwt
from models.utils import PyObjectId

controller = MessageController()

router = APIRouter()

@router.get("/")
async def get():
  data = await controller.getAll()
  return {
    "status": 200,
    "message": "Ok",
    "data": data
  }

@router.post("/")
async def createOne(body: CreateMessageDTO = Body(), auth: Union[str, None] = Header(default=None)):
  print(auth)
  try: 
    user = jwt.decode(auth, "secret")
    body["sender"] = PyObjectId(user.get("id"))
    msg = body["msg"]
    msg = preprocess(msg)
    transformedMsg = vectorizer.transform([msg])
    predict = MNB.predict(transformedMsg)
    body["isToxic"] = bool(predict[0])
    print(body["isToxic"])
    data = await controller.createOne(body.__dict__)
    return {
      "status": 200,
      "message": "Ok",
      "data": data
    }
  except:
    raise HTTPException(UNAUTHORIZED, "unauthorize")