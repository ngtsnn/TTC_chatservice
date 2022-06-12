from services.db.messages import MessageService


class MessageController: 
  def __init__(self) -> None:
    self.messageService = MessageService()

  async def getAll(self):
    return await self.messageService.getAll()

  async def createOne(self, message: dict) -> dict:
    return await self.messageService.createOne(message)