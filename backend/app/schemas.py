from pydantic import BaseModel
from enum import Enum

class CreateUser(BaseModel):
    name: str
    email:str
    phone:str
    password: str

    class Config:
        orm_mode = True


class UserRole(str, Enum):
    seeker = "seeker"
    owner = "owner"
    both = "both"

class UpdateUser(BaseModel):
    name: str
    email:str
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