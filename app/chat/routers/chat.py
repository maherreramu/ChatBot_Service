from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from chat.models import messages
from chat.utils.chat_exit import chat_exit
from chat.utils.chat_completion import gpt_chat_completion as completion
import secrets

router = APIRouter()

connected_clients = {}
client_chats = {}
greeting = "¡Bienvenido! ¿En qué puedo ayudarte hoy?"

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    #client_id = websocket.headers.get("Sec-WebSocket-Protocol")
    #print(client_id)
    #if client_id is None:
        #client_ip = websocket.client.host
    client_id = websocket.headers["Sec-WebSocket-Key"] #= generate_client_id(client_ip)
    print(client_id)
        #websocket.headers["Sec-WebSocket-Protocol"] = client_id
    connected_clients[client_id] = websocket
    client_chats[client_id] = messages.messages.copy()

    await send_response_to_client(client_id, greeting)

    try:
        while True:
            data = await websocket.receive_json()
            message = data["message"]
            print(message)
            
            await handle_message(client_id, message)
    except WebSocketDisconnect:
        del connected_clients[client_id]
        del client_chats[client_id]

async def handle_message(client_id: str, message: str):
    client_chats[client_id].append({"role": "user", "content": message})
    response = await completion(message)
    await send_response_to_client(client_id, response)

async def send_response_to_client(client_id: str, response: str):
    if client_id in connected_clients:
        websocket = connected_clients[client_id]
        client_chats[client_id].append({"role": "assistant", "content": response})
        if response == messages.goodbye:
                await chat_exit(client_chats[client_id])
                del connected_clients[client_id]
                del client_chats[client_id]
                await websocket.close()
        await websocket.send_text(response)

def generate_client_id(ip) -> str:
    token = secrets.token_urlsafe(16)
    return f"{ip}-{token}"
