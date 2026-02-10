from fastapi import APIRouter, Response, Depends, status, HTTPException
from .. import schemas, models, database, hashing
from sqlalchemy.orm import Session
from ..database import get_db
from email_validator import validate_email, EmailNotValidError

router = APIRouter(
    prefix='/user',
    tags=["User"]
)

@router.post('/register')
def register_user(request:schemas.CreateUser,
                  db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already registered")
    
    hashed_password = hashing.Hash.bcrypt(request.password)


    try:
        valid = validate_email(request.email)
        email = valid.email
        new_user = models.User(email = email, name = request.name,  phone = request.phone, password_hash = hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email not valid")

    return new_user

@router.put('/update/{id}')
def update_user(id:int,
                request:schemas.UpdateUser,
                db:Session = Depends(get_db)):
        db.query(models.User).filter(models.User.id == id).update(request.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        
        return {"Profile Updated"}


@router.put('/update/password/{id}')
def update_password(id:int,
                    request:schemas.UpdatePassword,
                    db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    real_password = user.password_hash
    
    if not (hashing.Hash.verify_password(request.old_password, real_password)):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Old Password didn't match") 
    
    new_hashed_password = hashing.Hash.bcrypt(request.new_password)

    user.password_hash = new_hashed_password

    db.commit()

    return {"Password Updated Successfully"}


