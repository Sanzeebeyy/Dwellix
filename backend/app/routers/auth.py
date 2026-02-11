from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import token, models
from ..database import get_db
from ..hashing import Hash

router = APIRouter(
    prefix='/login',
    tags=['/login']
)

@router.post('/')
def login_user(request:OAuth2PasswordRequestForm = Depends(),
               db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    
    if not Hash.verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong Password")
    
    access_token = token.create_access_token(data = {"sub":user.email})

    return{"access_token":access_token,
           "token_type":"bearer", "user":
           {"id":user.id,
            "email":user.email,
            "name":user.name}}