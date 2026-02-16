from pydantic import BaseModel
from enum import Enum
from typing import List

#---------------Users Schemas-----------------#

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
    id: int
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




#---------------Rooms Schemas-----------------#


class RoomType(str, Enum):
    single = "single"
    shared = "shared"
    flat = "flat"

class RoomStatus(str, Enum):
    available = "available"
    occupied = "occupied"
    hidden = "hidden"


class RoomImages(BaseModel):
    id:int
    image_url : str

    class Config:
        orm_mode = True


class Room(BaseModel):
    id:int
    title: str
    description: str
    area: str
    city: str
    country: str
    rent: int
    deposit: int
    is_furnished: bool
    min_stay_months: int

    room_type: RoomType
    status: RoomStatus
    owner: ShowPublicUser

    images:List[RoomImages]

    class Config:
        orm_mode = True



class CreateRoom(BaseModel):
    title: str
    description: str
    area: str
    city: str
    country: str
    rent: int
    deposit: int
    is_furnished: bool
    min_stay_months: int

    room_type: RoomType
    status: RoomStatus

    class Config:
        orm_mode = True

class UpdateRoom(BaseModel):
    title: str
    description: str
    area: str
    city: str
    country: str
    rent: int
    deposit: int
    is_furnished: bool
    min_stay_months: int

    room_type: RoomType
    status: RoomStatus

    class Config:
        orm_mode = True

class ShowRoomGeneral(BaseModel):
    id:int
    title: str
    area: str
    city: str
    country: str
    rent: int

    class Config:
        orm_mode = True


#---------------Applications Schemas-----------------#

class ApplicationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class CreateApplication(BaseModel):
    bargain_amount: int
    status: ApplicationStatus

    class Config:
        orm_mode = True

class ShowMyApplication(BaseModel):
    id:int
    room_id:int
    bargain_amount: int
    status: ApplicationStatus
    room: Room

    class Config:
        orm_mode = True

class ShowApplications(BaseModel):
    id:int
    room_id:int
    applicant_id: int
    status: ApplicationStatus
    bargain_amount:int
    applicant: ShowPublicUser

    class Config:
        orm_mode = True