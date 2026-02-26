# from fastapi import WebSocket
# from typing import Dict, List

# class ConnectionManager:
#     def __init__(self):
#         self.active_connection: Dict[int, List[WebSocket]] = {} # type definition

#     async def connect(self, chat_id:int, websocket: WebSocket):
#         await websocket.accept()
#         if chat_id not in self.active_connection:
#             self.active_connection[chat_id] = []
#         self.active_connection[chat_id].append(websocket)

#     def disconnect(self, chat_id:int, websocket:WebSocket):
#         self.active_connection[chat_id].remove(websocket)
#         if not self.active_connection[chat_id]:
#             del self.active_connection[chat_id]

#     async def broadcast(self, chat_id:int, message:dict):
#         for connection in self.active_connection.get(chat_id,[]):
#             await connection.send_json(message)