from fastapi import APIRouter, Response, Depends, status, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/user',
    tags=["User"]
)

@router.post('/register')
def register_user(request:schemas.CreateUser, db:Session = Depends(get_db)):
    pass