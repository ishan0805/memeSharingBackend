
from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text= Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    meme_id = Column(Integer, ForeignKey("memes.id"))
    comment_id=Column(Integer, ForeignKey("comments.id"),default=None)
    reply_comment=relationship("Comments")


