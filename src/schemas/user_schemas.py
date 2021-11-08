from pydantic import BaseModel

from typing import List, Optional


class User(BaseModel):
    email: str
    name:Optional [str]=None
    password: str


class Meme(BaseModel):
    url: str
    caption: str

    class Config:
        orm_mode = True


class ShowUserAndMemes(BaseModel):
    class Config:
        orm_mode = True
    email: str
    name: Optional [str]=None
    memes: List[Meme] = []


class ShowUser(BaseModel):
    class Config:
        orm_mode = True
    email: str
    name: Optional [str]

class UserDetails(BaseModel):
    id:int
    email: str
    name:Optional [str]=None
    password: str

