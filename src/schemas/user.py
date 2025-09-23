from pydantic import BaseModel, EmailStr
from typing import Optional
from src.models.user_model import User

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    level: str 
    school: str
    tel: str
    address: str
    class_id: Optional[int] = None
    registration_number: Optional[str] = None

    parent_name: Optional[str] = None
    parent_tel: Optional[str] = None
    parent_email: Optional[str] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    level: str
    school: str
    tel: str
    address: str
    class_id: Optional[int] = None
    registration_number: Optional[str] = None

    parent_name: Optional[str] = None
    parent_tel: Optional[str] = None
    parent_email: Optional[str] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str
