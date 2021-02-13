from typing import Optional

from fastapi import FastAPI, Depends
from database import SessionLocal, engine
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Memes
import uvicorn
import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/swagger-ui/', port=8080)

# initilise database


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# create pydantic class for meme
class Meme(BaseModel):
    name: str
    url: str
    description: str

# create pydantic class for updating meme


class PatchMeme(BaseModel):
    url: str
    description: str

# route to get latest 100 memes


@app.get('/memes')
async def get():

    db = SessionLocal()
    return db.query(Memes).order_by(Memes.id.desc()).limit(100).all()


# route to get meme by id
@app.get('/memes/{id}')
async def get(id: int):

    db = SessionLocal()
    memes = db.query(Memes).filter(Memes.id == id).first()

    if memes != None:
        return memes

    return JSONResponse(status_code=404)

# route to post meme


@app.post('/memes')
async def post(meme: Meme, db: Session = Depends(get_db)):
    memes = Memes()
    memes.name = meme.name
    memes.url = meme.url
    memes.description = meme.description
    db.add(memes)
    db.commit()

    return {"id": memes.id}


# route to update
@app.patch('/memes/{id}')
async def patch(id: int, patchmeme: PatchMeme, db: Session = Depends(get_db)):
    try:
        memes = db.query(Memes).filter(Memes.id == id).first()
        memes.url = patchmeme.url
        memes.description = patchmeme.description
        db.commit()
    except:
        return JSONResponse(status_code=404)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
