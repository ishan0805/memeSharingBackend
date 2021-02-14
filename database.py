# https://memesharing.herokuapp.com/
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./memes.db"
#SQLALCHEMY_DATABASE_URL = "postgres://mbemzptsbvjclz:8a90c0adb9e34766149c1252eb95a321ce883defb5fac4e40b4cef31480145c9@ec2-100-24-139-146.compute-1.amazonaws.com:5432/d3ol9sdno7gh7r"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
