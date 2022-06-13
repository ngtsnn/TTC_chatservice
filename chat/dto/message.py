from pydantic import BaseModel, Field
from typing import Union
from models.utils import PyObjectId

def MessageHelper(message) -> dict:
  sender = message["sender"][0]

  return {
    "_id": str(message["_id"]),
    "msg": message["msg"],
    "sender": {
      "_id": str(sender["_id"]),
      "id": sender["id"],
      "name": sender["name"],
      "username": sender["username"]
    },
    "isToxic": message["isToxic"]
  }

class CreateMessageDTO(BaseModel):
  msg: str
  sender: PyObjectId = Field(default=PyObjectId())
  isToxic: bool = Field(default=False)
  def __getitem__(self, item):
    return getattr(self, item)

  def __setitem__(self,item,value):
    #explicitly defined __setitem__
    setattr(self, item, value)

class CreateMessageHeadersDTO(BaseModel):
  auth: str
  def __getitem__(self, item):
    return getattr(self, item)

  def __setitem__(self,item,value):
    #explicitly defined __setitem__
    setattr(self, item, value)

