from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Memes(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    caption = Column(String)
