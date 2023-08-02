from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    #automatically sends the error and the validations 

class PostCreate(PostBase):
    pass

class User(BaseModel):
    id : int
    email : EmailStr
    created_at: datetime

    class Config:
        orm_mode= True

class Post(PostBase):
    id : int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int 
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]


class VoteCreate(BaseModel):
    user_id : int
    post_id : int

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)