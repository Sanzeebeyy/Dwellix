from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    seeker = "seeker"
    owner = "owner"
    both = "both"


class User(BaseModel):
    name:str
    email: str
    password: str
    phone: str
    bio:str | None = None
    gender: str | None = None
    role: UserRole
    profile_picture_url: str|None = None
    
    class Config:
        orm_mode = True




class ShowPublicUser(BaseModel):
    name: str
    bio: str | None = None
    gender: str | None = None
    role: UserRole
    profile_picture_url: str| None = None

    class Config:
        orm_mode = True

class ShowUser(ShowPublicUser):

    phone: str
    email: str

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    name: str
    email:str
    phone:str
    password: str

    class Config:
        orm_mode = True



class UpdateUser(BaseModel):
    name: str
    phone:str
    bio: str|None = None
    gender: str | None = None
    role : UserRole
    profile_picture_url: str|None = None

    class Config:
        orm_mode = True

class UpdatePassword(BaseModel):
    old_password: str
    new_password: str

    class Config:
        orm_mode = True

class DeleteUser(BaseModel):
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_types: str

    class Config():
        orm_mode = True 


class TokenData(BaseModel):
    email: str
    
    class Config():
        orm_mode = True 