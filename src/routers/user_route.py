from fastapi import APIRouter, Depends
from ..database import get_db
from ..hashing import *  # use .. to move up a module
from ..schemas.user_schemas import *
from ..models.user_model import *
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

# create instance of router
router = APIRouter(
    prefix="/user",
    tags=['users'],
)


@router.post('/', response_model=ShowUser)
async def post(user: User, db: Session = Depends(get_db)):
    try:
        db_user = Users()
        db_user.name = user.name
        db_user.password = bcrypt(user.password)
        db_user.email = user.email
        db.add(db_user)
        db.commit()

    except:
        return JSONResponse(status_code=409, content={"message": "User already exists"})

    return user

    # return db.query(Memes).order_by(Memes.id.desc()).limit(100).all()

    # route to get meme by id


@router.get('/{id}', response_model=ShowUserAndMemes)
async def get(id: int, db: Session = Depends(get_db)):

    user = db.query(Users).filter(Users.id == id).first()

    if user != None:
        return user

    return JSONResponse(status_code=404)

"""
# route to post meme
@router.post('/')
async def post(meme: Meme, db: Session = Depends(get_db)):
    memes = Memes()
    memes.name = meme.name
    memes.url = meme.url
    memes.caption = meme.caption
    db.add(memes)
    db.commit()

    return {"id": memes.id}


# route to update
@router.patch('/{id}')
async def patch(id: int, patchmeme: PatchMeme, db: Session = Depends(get_db)):
    try:
        memes = db.query(Memes).filter(Memes.id == id).first()
        memes.url = patchmeme.url
        memes.caption = patchmeme.caption
        db.commit()
    except:
        return JSONResponse(status_code=404)


# route to delete meme
@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(get_db)):
    try:
        db.query(Memes).filter(Memes.id == id).delete()
        db.commit()
    except:
        return JSONResponse(status_code=404)"""
