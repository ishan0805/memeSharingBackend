from pydantic import BaseModel
from .user_schemas import ShowUser
# create pydantic class for meme


class Meme(BaseModel):
    url: str
    caption: str

    class Config:
        orm_mode = True


class ShowMeme(BaseModel):
    id:int
    url: str
    caption: str
    owner: ShowUser
    comment_count:int

    class Config:
        orm_mode = True

    #owner: ShowUser
    # because we are using db we need to set orm = true

    # create pydantic class for updating meme


class PatchMeme(Meme):
    url: str
    caption: str
