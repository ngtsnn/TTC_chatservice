from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
# importing ObjectId from bson library
from bson.objectid import ObjectId
from db.connection import connect
from .utils import PyObjectId


class MessageSchema(BaseModel):
  id: str = Field(default="")
  msg: str = Field(default="")
  sender: PyObjectId = Field()
  isToxic: bool = Field(default=False)

  # class Config:
  #   schema_extra = {
  #     "example": {
  #       "id": "12345678123456781234567812345678",
  #       "msg": "Hello",
  #       "sender": "62a3c20aa75c379e4b3f5668",
  #       "isToxic": False
  #     }
  #   }

messageModel = connect().get_collection("messages")