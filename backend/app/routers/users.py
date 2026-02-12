from fastapi import APIRouter, Response, Depends, status, HTTPException

from fastapi import File, UploadFile
import uuid

from .. import schemas, models, database, hashing
from sqlalchemy.orm import Session
from ..database import get_db
from email_validator import validate_email, EmailNotValidError
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/user',
    tags=["User"]
)




@router.post('/register')
def register_user(request:schemas.CreateUser,
                  db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email Already Registered")
    
    hashed_password = hashing.Hash.bcrypt(request.password)


    try:
        valid = validate_email(request.email)
        email = valid.email
        new_user = models.User(email = email, name = request.name,  phone = request.phone, password_hash = hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email Not Valid")

    return new_user




@router.get('/', response_model=schemas.ShowUser)
def show_self(db:Session = Depends(get_db),
              current_user: schemas.User = Depends(get_current_user)):
        user = db.query(models.User).filter(models.User.email == current_user.email).first()

        return user





@router.get('/{user_id}', response_model= schemas.ShowPublicUser)
def show_user(user_id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found") 

    return user





@router.put('/update')
def update_user(request:schemas.UpdateUser,
                current_user:schemas.User = Depends(get_current_user),
                db:Session = Depends(get_db)):
        

        db.query(models.User).filter(models.User.email == current_user.email).update(request.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        
        user = db.query(models.User).filter(models.User.email == current_user.email).first()

        return {"details":"Profile Updated","update":{
            "name":user.name,
            "email":user.email,
            "gender":user.gender,
            "bio":user.bio,
            "role":user.role,
            "profile_picture":user.profile_picture_url
        }}


IMGDIR = 'static/images/profile_images/'

@router.put('/update/profile-photo')
async def update_profile_picture(file: UploadFile = File(...),
                                 db:Session = Depends(get_db),
                                 current_user: schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if not user:
         raise HTTPException(status_code=404 , detail="User Not Found")

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    with open(f"{IMGDIR}{file.filename}","wb") as f:
         f.write(contents)

    user.profile_picture_url = f"static/images/profile_images/{file.filename}"
    db.commit()
    return file.filename



@router.put('/update/password')
def update_password(request:schemas.UpdatePassword,
                    current_user: schemas.User = Depends(get_current_user),
                    db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    
    real_password = user.password_hash
    
    if not (hashing.Hash.verify_password(request.old_password, real_password)):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Old Password Didn't Match") 
    
    new_hashed_password = hashing.Hash.bcrypt(request.new_password)

    user.password_hash = new_hashed_password

    db.commit()

    return {"Password Updated Successfully"}





@router.delete('/delete-user')
def delete_user(request:schemas.DeleteUser,
                current_user: schemas.User = Depends(get_current_user),
                db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    
    real_password = user.password_hash
    if not hashing.Hash.verify_password(request.password, real_password):
        raise HTTPException(status_code=401, detail="Incorrect Password")
    
    db.delete(user)
    db.commit()
    return "Account Deleted"
    