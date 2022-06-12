from motor.motor_asyncio import AsyncIOMotorClient

CONNECTION_STRING = "mongodb+srv://trung:123456Trung@cluster0.xvhk9ho.mongodb.net/?retryWrites=true&w=majority"
 
def connect():
  try:
    client = AsyncIOMotorClient(CONNECTION_STRING)
    database = client.test
    print("connect to database successfully")
    return database
  except ():
    print("Fail to connect to database")