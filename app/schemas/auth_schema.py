from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    role: Optional[int] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    name: Optional[str] = None
    role: Optional[int] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    role: Optional[int] = None
    name: Optional[str] = None

class SendPassword(BaseModel):
    email: EmailStr

    
class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = "Bearer"
    name: Optional[str] = None
    role: Optional[int] = None

class TokenData(BaseModel):
    id: Optional[int] = None