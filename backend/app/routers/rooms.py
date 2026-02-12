from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models, schemas

router = APIRouter(
    prefix='/room',
    tags=["Room"]
)

@router.get('/', response_model= List[schemas.ShowRoomGeneral])
def show_rooms_general(db: Session = Depends(get_db)):
    rooms = db.query(models.Room).all()
    return rooms


@router.get('/{room_id}', response_model=schemas.Room)
def show_room(room_id:int,
               db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    return room




@router.post('/create-room')
def create_rooms(request: schemas.CreateRoom,
                 db: Session = Depends(get_db),
                 current_user : schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    room_counts = db.query(models.Room).filter(models.Room.owner_id == user.id).count()
    
    if user.role not in ['owner','both']:
        raise HTTPException(status_code=403, detail="Only Owners Can Post Rooms")
    if room_counts > 10:
        raise HTTPException(status_code=403, detail="Not Allowed To Post More Than 10 Rooms")

    new_room = models.Room(owner_id = user.id,
                           title = request.title,
                           description = request.description,
                           area = request.area,
                           city = request.city,
                           country = request.country,
                           rent = request.rent,
                           deposit = request.deposit,
                           room_type = request.room_type,
                           is_furnished = request.is_furnished,
                           min_stay_months = request.min_stay_months,
                           status = 'available')
    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room


@router.put('/update-room/{room_id}')
def update_rooms(room_id:int,
                 request: schemas.UpdateRoom,
                 db: Session = Depends(get_db),
                 current_user : schemas.User = Depends(get_current_user)):
    
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    
    if not room:
        raise HTTPException(status_code=404 , detail="Room Not Found")

    if room.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You Are Not Allowed To Edit This Room")
    
    for key, value in request.dict(exclude_unset=True).items():
        setattr(room, key, value)
    
    db.commit()
    db.refresh(room)

    return room

