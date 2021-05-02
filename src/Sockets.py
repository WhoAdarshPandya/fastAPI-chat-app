from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.friends_online = []

    async def connect(self, websocket: WebSocket, client_id: str, name: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.friends_online.append({"client_id": client_id, "name": name})

    def disconnect(self, websocket: WebSocket, client_id: str):
        self.active_connections.remove(websocket)
        self.friends_online = [
            i for i in self.friends_online if not (i['client_id'] == client_id)]

    # async def send_personal_message(self,websocket: WebSocket):
    async def send_personal_message(self, message: dict, client_id: str):
        # print("cin")
        # print(self.active_connections)
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        # await print(message['client_id'])
        # await print(message['msg'])
        if message['event'] == "friends":
            for connection in self.active_connections:
                await connection.send_text(json.dumps(message))
        if message['event'] == "chat":
            await self.active_connections[message['order']['one']].send_text(json.dumps(message))
            await self.active_connections[message['order']['two']].send_text(json.dumps(message))
        # for connection in self.active_connections:
        # await connection.send_text(json.dumps(message))

    def sendFriends(self):
        return self.friends_online
