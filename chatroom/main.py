from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

# Store connected WebSocket clients
clients: List[WebSocket] = []

# WebSocket endpoint for connecting to the chatroom
@app.websocket("/chat/{username}")
async def connect_to_chat(username: str, websocket: WebSocket):
    await websocket.accept()
    clients.append((username, websocket))  # Store username along with websocket
    
    # Notify all clients about the new user joining, except the user who just joined
    for client_username, client_websocket in clients:
        if client_username != username:
            await client_websocket.send_text(f"{username} joined the chatroom")

    try:
        while True:
            # Receive message from the client
            message = await websocket.receive_text()
            # Broadcast the received message to all clients
            for client_username, client_websocket in clients:
                await client_websocket.send_text(f"{username}: {message}")
    finally:
        # Remove the client from the list when the connection is closed
        clients.remove((username, websocket))
        # Notify all clients about the user leaving
        for client_username, client_websocket in clients:
            await client_websocket.send_text(f"{username} left the chatroom")
