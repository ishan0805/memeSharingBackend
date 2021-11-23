from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.orm import relationship

from .. database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    memes = relationship("Memes", back_populates="owner")
