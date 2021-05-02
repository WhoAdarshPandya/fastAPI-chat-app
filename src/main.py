from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .Sockets import ConnectionManager
import json

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return {'msg': 'socket io api is working...'}


manager = ConnectionManager()


async def findIndex(client_id):
    fri = next((index for (index, d) in enumerate(
        manager.friends_online) if d["client_id"] == client_id), None)
    print("found")
    print(fri)
    return fri


@app.websocket("/ws/{client_id}/{name}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, name: str):
    print(manager.sendFriends())
    await manager.connect(websocket, client_id, name)
    try:
        while True:
            await manager.broadcast({"event": "friends", "friends": manager.sendFriends()})
            data = json.loads(await websocket.receive_text())
            # await manager.send_personal_message("adjskl")
            # print(data)
            index = await findIndex(data['id'])
            my_indx = await findIndex(client_id)
            await manager.broadcast({"event": "chat", "order": {'one': index, 'two': my_indx}, "client_id": client_id, "msg": data['msg']})
    except WebSocketDisconnect:
        print("initiate leaving sequence")
        manager.disconnect(websocket, client_id)
