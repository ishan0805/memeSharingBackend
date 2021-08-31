from pydantic import BaseModel

from typing import List


class User(BaseModel):
    email: str
    name: str
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
    name: str
    memes: List[Meme] = []


class ShowUser(BaseModel):
    class Config:
        orm_mode = True
    email: str
    name: str
