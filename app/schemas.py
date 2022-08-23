from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    name:str
    age: int
    gender: Optional[str] = None
    height: float = None

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email : EmailStr
    last_modified : datetime

    class Config:
        orm_mode = True

class Post(PostBase):

    id : int
    last_modified : datetime
    user_id : int
    user_information: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    Votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str



class UserLogin(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)