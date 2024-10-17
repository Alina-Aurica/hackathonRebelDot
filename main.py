from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class TwoUserChatController:
    def __init__(self):
        self.connected_clients: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        if len(self.connected_clients) >= 2:
            await websocket.send_text("Room is full. Only two users can interact.")
            await websocket.close()
        else:
            await websocket.accept()  # Accept the WebSocket connection
            self.connected_clients.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.connected_clients.remove(websocket)

    async def broadcast(self, message: str, sender: WebSocket):
        """Send message to the other connected client (not the sender)."""
        for client in self.connected_clients:
            if client != sender:
                await client.send_text(message)

# Instantiate the controller
chat_controller = TwoUserChatController()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await chat_controller.connect(websocket)
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_text()
            # Broadcast the received message to the other client
            await chat_controller.broadcast(data, websocket)
    except WebSocketDisconnect:
        chat_controller.disconnect(websocket)
