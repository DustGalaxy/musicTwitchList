
from typing import Optional
import uuid
from pydantic import BaseModel


class UserRead(BaseModel):
    id: uuid.UUID
    username: str 
    
    twitch_user_id: str
    twitch_access_token: str
    twitch_refresh_token: str
    
    image_url: str

    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool    
    
    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    username: str 
    
    twitch_user_id: str
    twitch_access_token: str
    twitch_refresh_token: str
    
    image_url: str
    
    id: uuid.UUID
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserUpdate(BaseModel):
    username: Optional[str]  
    
    twitch_user_id: Optional[str] 
    twitch_access_token: Optional[str] 
    twitch_refresh_token: Optional[str] 
    
    image_url: Optional[str]
    id: uuid.UUID
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None