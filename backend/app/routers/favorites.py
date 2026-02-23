from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models, schemas

router = APIRouter(
    prefix='/favorites',
    tags=["Favorites"]
)

@router.post('/{room_id}')
def favorite(room_id:int,
             db:Session = Depends(get_db),
             current_user: schemas.User = Depends(get_current_user)):
    
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    user_id = user.id

    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room Not Found")

    already_favorite = db.query(models.Favorite).filter(models.Favorite.user_id == user_id,
                                                        models.Favorite.room_id == room_id).first()
    
    if already_favorite:
        raise HTTPException(status_code=400, detail="Not Allowed To Favorite Twice")

    new_favorite = models.Favorite(room_id = room_id, user_id = user_id)

    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)

    return new_favorite


@router.get('/', response_model=List[schemas.ShowRoomGeneral])
def show_favorites(area:str|None = None,
                   city:str|None = None,
                   country:str|None = None,
                   max_deposit: int|None = None,
                   max_rent: int|None = None,
                   status: str|None = None,
                   db:Session = Depends(get_db),
                   current_user: schemas.User = Depends(get_current_user)):
    
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    user_id = user.id

    query = db.query(models.Room).join(models.Favorite,
                                       models.Favorite.room_id == models.Room.id).filter(models.Favorite.user_id == user_id)

    if area:
        query.filter(models.Room.area == area)
    if city:
        query.filter(models.Room.city == city)
    if country:
        query.filter(models.Room.country == country)
    if max_deposit:
        query.filter(models.Room.deposit <= max_deposit+100)
    if max_rent:
        query.filter(models.Room.rent <= max_rent+1000)
    if status:
        query.filter(models.Room.status == status)
    
    return query.all()

@router.delete('/{fav_id}')
def delete_user(fav_id:int,
                current_user: schemas.User = Depends(get_current_user),
                db:Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    
    favorite = db.query(models.Favorite).filter(models.Favorite.id == fav_id).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite Not Found")

    if favorite.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not Allowed To Unfavorite")

    db.delete(favorite)
    db.commit()
    return "Favorite Removed"