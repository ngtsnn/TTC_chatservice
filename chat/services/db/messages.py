from bson import ObjectId
from bson.json_util import default,RELAXED_JSON_OPTIONS

from models.messages import MessageSchema, messageModel
from dto.message import MessageHelper


class MessageService:
  def __init__(self):
    self.model = messageModel
  
  async def getAll(self):
    data = []
    async for message in self.model.aggregate([
      {
        "$lookup": {
          "from": "users",
          "localField": "sender",
          "foreignField": "_id",
          "as": "sender"
        }
      }
    ]):
      data.append(MessageHelper(message))
    return data

  async def createOne(self, message: dict):
    inserted = await self.model.insert_one(message)
    # data = await self.model.find_one({"_id": inserted.inserted_id})
    data = []
    async for message in self.model.aggregate([
      {
        "$match": { "_id": inserted.inserted_id }
      },
      {
        "$lookup": {
          "from": "users",
          "localField": "sender",
          "foreignField": "_id",
          "as": "sender"
        }
      }
    ]):
      
      data.append(MessageHelper(message))
    # data["_id"] = str(data["_id"])
    # data["sender"] = str(data["sender"])
    return data[0]