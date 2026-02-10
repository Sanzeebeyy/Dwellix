from pydantic import BaseModel

class CreateUser(BaseModel):
    email:str
    phone:str
    password: str

    class Config:
        orm_mode = True


