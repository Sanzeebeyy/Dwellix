from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models, schemas
import uuid

router = APIRouter(
    prefix='/rooms',
    tags=["Room"]
)

@router.get('/', response_model= List[schemas.ShowRoomGeneral])
def show_rooms_general(area:str | None = None,
                       city:str | None = None,
                       country:str |None = None,
                       max_rent:int | None = None,
                       max_deposit:int | None = None,
                       is_furnished:bool | None = None,
                       room_type:schemas.RoomType |None = None,
                       status: schemas.RoomStatus | None = schemas.RoomStatus.available,
                       db: Session = Depends(get_db)):
    
    query = db.query(models.Room)

    if area:
        query = query.filter(models.Room.area == area)
    
    if city:
        query = query.filter(models.Room.city == city)

    if country:
        query = query.filter(models.Room.country == country)

    if max_rent:
        query = query.filter(models.Room.rent <= max_rent + 1000)
    
    if max_deposit:
        query = query.filter(models.Room.deposit <= max_deposit + 100)

    if is_furnished is not None:
        query = query.filter(models.Room.is_furnished == is_furnished)

    if status:
        query = query.filter(models.Room.status == status)

    if room_type:
        query = query.filter(models.Room.room_type == room_type)
    
    
    rooms = query.all()
    return rooms



@router.get('/{room_id}', response_model=schemas.Room)
def show_room(room_id:int,
               db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room Not Found")

    return room




@router.post('/create-room')
def create_rooms(request: schemas.CreateRoom,
                 db: Session = Depends(get_db),
                 current_user : schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    room_counts = db.query(models.Room).filter(models.Room.owner_id == user.id).count()
    
    if user.role not in ['owner','both']:
        raise HTTPException(status_code=403, detail="Only Owners Can Post Rooms")
    if room_counts >= 10:
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


@router.delete('/delete-room/{room_id}')
def delete_room(room_id:int,
                db:Session = Depends(get_db),
                current_user : schemas.User = Depends(get_current_user)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room Not Found")
    if (room.owner_id != user.id):
        raise HTTPException(status_code=403, detail="Not Allowed To Delete")
    
    db.delete(room)
    db.commit()

    return "Room Deleted Successfully"
    


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


IMGDIR = "static/images/room_images/"

@router.post('/update-room/{room_id}/room-photos')
async def add_room_photos(room_id:int, files: List[UploadFile] = File(...),
                          db: Session = Depends(get_db),
                          current_user : schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    room = db.query(models.Room).filter(models.Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room Not Found")

    if room.owner_id != user.id : 
        raise HTTPException(status_code=403, detail="You Are Not Allowed To Edit This Room")
    
    for file in files:
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()

        with open (f'{IMGDIR}{file.filename}',"wb") as f:
            f.write(contents)

        new_image = models.RoomImage(room_id = room_id, image_url = f"/static/images/room_images/{file.filename}")

        db.add(new_image)
    
    db.commit()

    return {"Images Uploaded Successfully"}
    

    
