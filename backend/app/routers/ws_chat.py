from fastapi import APIRouter, Depends, status, WebSocket, WebSocketDisconnect
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..ws_manager import ConnectionManager
from ..token import get_current_user_ws

get_db = database.get_db

router = APIRouter(
    tags=["WebSocket"],
    prefix='ws'
)

manager = ConnectionManager()

@router.websocket('/{chat_id}')
async def websocket_chat(
    websocket: WebSocket,
    chat_id:int,
    db:Session = Depends(get_db)
):
    user = await get_current_user_ws(websocket, db)

    if not user:
        return
    
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()

    if not chat:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    if user.id not in [chat.user1_id, chat.user2_id]:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    await manager.connect(chat_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            message = data["message"]

            new_message = models.Message( chat_id = chat_id, sender_id = user.id , message_text = message)

            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            await manager.broadcast(chat_id,{
                "sender_id": user.id,
                "message_text":message,
                "message_id":new_message.id
            })

    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)