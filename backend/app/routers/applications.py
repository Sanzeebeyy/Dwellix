from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models, schemas


router = APIRouter(
    prefix='/application',
    tags=["Applications"]
)

@router.post('/apply/{room_id}')
def apply(room_id:int,
          request: schemas.CreateApplication,
          db:Session = Depends(get_db),
          current_user: schemas.User = Depends(get_current_user)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    applicant = db.query(models.User).filter(models.User.email == current_user.email).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room Not Found")
    
    if room.status != "available":
        raise HTTPException(status_code=403, detail="Not Allowed To Apply")

    if room.owner_id == applicant.id:
        raise HTTPException(status_code=403, detail="Not Allowed To Apply For Own Room")

    application = db.query(models.Application).filter(
        models.Application.room_id == room.id,
        models.Application.applicant_id == applicant.id
        ).first()
    
    if application :
        raise HTTPException(status_code=400, detail= "Not Allowed To Apply More Than Once")

    new_application = models.Application(room_id = room.id,
                                         applicant_id = applicant.id,
                                         bargain_amount = request.bargain_amount,
                                         status = "pending",
                                         )
    
    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

@router.get('/my', response_model=List[schemas.ShowMyApplication])
def show_my_applications(db:Session = Depends(get_db),
                         current_user: schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    applications = db.query(models.Application).filter(models.Application.applicant_id == user.id).all()

    return applications

@router.get('/see_applications', response_model=List[schemas.ShowGeneralApplications])
def show_applications(room_id:int|None = None,
                      bargain_amount:int|None = None,
                      status:str|None = 'pending',
                      db:Session = Depends(get_db),
                      current_user:schemas.User = Depends(get_current_user)):
    
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if user.role not in ["owner", "both"]:
        raise HTTPException(status_code=403, detail="Not Allowed")
    


    query = db.query(models.Application).join(models.Room).filter(
        models.Room.owner_id == user.id
    )

    if room_id is not None:
        query = query.filter(models.Application.room_id == room_id)

    if bargain_amount is not None:
        query = query.filter(models.Application.bargain_amount <= bargain_amount+1000)
    
    if status is not None:
        query = query.filter(models.Application.status == status)

    applications = query.all()

    return applications


@router.get('/see_applications/{application_id}', response_model=schemas.ShowApplications)
def show_application(application_id:int,
                     db:Session = Depends(get_db),
                     current_user:schemas.User = Depends(get_current_user)):
    
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if user.role not in ["owner", "both"]:
        raise HTTPException(status_code=403, detail="Not Allowed")
    
    query = db.query(models.Application).join(models.Room).filter(
        models.Room.owner_id == user.id, models.Application.id == application_id
    )

    application = query.first()

    return application




