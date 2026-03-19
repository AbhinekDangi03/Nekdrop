from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uuid

app = FastAPI()

rooms = {} 

from fastapi.responses import FileResponse
import os

@app.get("/")
async def get():
    return FileResponse("index.html")
async def get():
    return HTMLResponse("<h1>Thanks for using NekDrop - Abhinek.</h1>")

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(websocket)
    
    try:
        while True:
            # We receive data from one device...
            data = await websocket.receive_bytes()
            # ...and blast it out to the other device in the same room.
            for client in rooms[room_id]:
                if client != websocket:
                    await client.send_bytes(data)
    except WebSocketDisconnect:
        rooms[room_id].remove(websocket)
