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
def register_user(request:schemas.CreateUser, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already registered")
    
    hashed_password = hashing.Hash.bcrypt(request.password)


    try:
        valid = validate_email(request.email)
        email = valid.email
        new_user = models.User(email = email, phone = request.phone, password_hash = hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email not valid")

    return new_user
    