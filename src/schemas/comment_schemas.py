from pydantic import BaseModel
from typing import List, Optional
# create pydantic class for comment


class Comment(BaseModel):

    text:str
    meme_id:int
    user_id: int
    comment_id:Optional[int]=None
    # Example of self referencing model
    reply_comment:'Comment'=None

    class Config:
        orm_mode = True


class ShowComment(BaseModel):
    text:str
    class Config:
        orm_mode = True


