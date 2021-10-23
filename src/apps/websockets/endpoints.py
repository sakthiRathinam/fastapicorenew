from starlette.responses import JSONResponse
from .models import *
from .schemas import *
from fastapi import WebSocket,APIRouter, Body, Depends, HTTPException, Request, BackgroundTasks, status
from typing import List
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from .service import socket_manager
from .schemas import Send_Data
socket_router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <h1>connectgroup</h1>
        <form action="" onsubmit="connectGroup(event)">
            <input type="text" id="groupname" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket();
            function connectGroup(event) {
                var group = document.getElementById("groupname")
                ws = new WebSocket("ws://192.168.29.98:8001/api/v1/sockets/ws"+"/"+group.value+"/");
                group.value = ''
                connectMessage()
                event.preventDefault()
            }
            function connectMessage(){
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
            
        </script>
    </body>
</html>
"""


@socket_router.get("/")
async def get():
    return HTMLResponse(html)


@socket_router.post("/sendJson")
async def sendJson(data:Send_Data):
    # try:
    print(data.args[0].dict())
    await socket_manager.send_json_message(data.topic, data.args[0].json())
    # await socket_manager.send_personal_message(data.topic, "waefwaef")

    return JSONResponse({"success": "message sended successfully"}, status_code=200)
    # except:
    #     return "Faliure"
@socket_router.websocket('/joinall')
async def join_groups(websocket:WebSocket,groups:List[str]):
    try:
        for group in groups:
            await socket_manager.connect(websocket,group)
        return JSONResponse({"success":"connected to all groups"}, status_code=200)
    except Exception as e:
        return JSONResponse({"error":"something went wrong"},status_code=500)


@socket_router.websocket("/ws/{groupname}/")
async def group_chat(websocket: WebSocket,groupname:str,disconnect:bool=False):
    if disconnect:
        await socket_manager.disconnect(websocket,groupname)
        return JSONResponse({"success":"disconnected successfully"},status_code=200)
    await socket_manager.connect(websocket, groupname)
    try:
        while True:
            data = await websocket.receive_text()
            # data = await websocket.receive_json()
            await socket_manager.send_group_message(websocket,groupname, data)
    except Exception as e:
        await socket_manager.disconnect(websocket,groupname)






