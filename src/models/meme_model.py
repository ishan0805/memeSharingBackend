from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.orm import relationship

from .. database import Base


class Memes(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    caption = Column(String)
    comment_count=Column(Integer,default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates='memes')
    comments = relationship("Comments",)
