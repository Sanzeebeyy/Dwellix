from fastapi import APIRouter, Response, Depends, status, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session
from typing import List
from ..oauth2 import get_current_user

from sqlalchemy import or_

get_db = database.get_db

router = APIRouter(
    prefix='/chat',
    tags=["Chat"]
)

@router.get('/')
def show_chats(db:Session = Depends(get_db),
               current_user: schemas.User = Depends(get_current_user)):
    
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    user_id = user.id

    chats = db.query(models.Chat).filter(
        or_(
        models.Chat.user1_id == user_id,
        models.Chat.user2_id == user_id
        )
    ).all()

    result = []

    for chat in chats:
        other_user_id = (
            chat.user1_id if user_id == chat.user2_id
            else
            chat.user2_id
        )

        other_user = db.query(models.User).filter(models.User.id == other_user_id).first()

        result.append(
            {
                "chat_id":chat.id,
                "current_user_id":user_id,
                "other_user":{
                    "id":other_user.id,
                    "name":other_user.name,
                    "profile_picture_url":other_user.profile_picture_url,

                }
            }
        )

    return result



@router.get('/{chat_id}/messages', response_model=List[schemas.ShowMessage])
def show_messages(chat_id: int,
                  db: Session = Depends(get_db),
                  current_user: schemas.User = Depends(get_current_user)):
    
    user= db.query(models.User).filter(models.User.email == current_user.email).first()
    user_id = user.id 
    
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()

    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if user_id not in [chat.user1_id, chat.user2_id]:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    messages = db.query(models.Message).filter(models.Message.chat_id == chat_id).all()

    return messages