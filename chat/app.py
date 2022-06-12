from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from routes.index import router

app = FastAPI()

app.add_middleware(CORSMiddleware)


app.include_router(router=router)

