from typing import Optional

from fastapi import FastAPI, Depends, File
from src.database import SessionLocal, engine, get_db, Base
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.routers import authentication_route, meme_route, user_route ,authentication_route
import uvicorn
from src.models.meme_model import Memes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/swagger-ui/', port=8000)

app.include_router(authentication_route.router)
app.include_router(meme_route.router)
app.include_router(user_route.router)
# for Cors control
# enable support for ors
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
