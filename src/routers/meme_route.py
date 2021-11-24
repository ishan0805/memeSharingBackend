from typing import List
from fastapi import APIRouter, Depends

from src.models.user_model import Users
from ..database import get_db  # use .. to move up a module
from ..schemas.meme_schemas import *
from ..models.meme_model import *
from ..schemas import user_schemas
from .. import token
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
# create instance of router
router = APIRouter(
    prefix="/memes",
    tags=['memes'],
)


@router.get('/', response_model=List[ShowMeme])  # instead of app.get use router.get
async def get(db: Session = Depends(get_db)
,current_user:user_schemas.UserDetails = Depends(token.get_current_user) ):

    return db.query(Memes).order_by(Memes.id.desc()).limit(100).all()


# route to get meme by id
@router.get('/{id}', response_model=ShowMeme)
async def get(id: int, db: Session = Depends(get_db)
,current_user:user_schemas.UserDetails = Depends(token.get_current_user)):

    memes = db.query(Memes).filter(Memes.id == id).first()

    if memes != None:
        return memes

    return JSONResponse(status_code=404,content={"message": "Meme Not Found"})


# route to post meme
@router.post('/')
def post(meme: Meme, db: Session = Depends(get_db),current_user:user_schemas.UserDetails = Depends(token.get_current_user)):
    # hard code change afterward
    memes = Memes(url=meme.url,
                  caption=meme.caption, owner_id=current_user.id)

    
    db.add(memes)
    db.commit()
    return {'success':True}
    #db.refresh(memes)
    # print(memes.dict())


    # route to update
@router.patch('/{id}')
async def patch(id: int, patchmeme: PatchMeme, db: Session = Depends(get_db),current_user:user_schemas.UserDetails = Depends(token.get_current_user)):
   

    try:
        memes = db.query(Memes).filter(Memes.id == id).first()
        if memes is None:
             return JSONResponse(status_code=404,content={'message':'Not Found'})
        if  memes.owner_id != current_user.id:
             return JSONResponse(status_code=404,content={'message':'You Cannot Edit this Meme'})   

        memes.url = patchmeme.url
        memes.caption = patchmeme.caption
        db.commit()
        return {'message':"Successful"}
        
    except:
        return JSONResponse(status_code=404,content={'message':'Not Found'})



# route to delete meme
@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(get_db),current_user:user_schemas.UserDetails= Depends(token.get_current_user)):
    try:
        memes = db.query(Memes).filter(Memes.id == id).first()
        if memes is None:
             return JSONResponse(status_code=404,content={'message':'Not Found'})
        print(current_user)     
        if  memes.owner_id != current_user.id:
             return JSONResponse(status_code=404,content={'message':'You Cannot Delete this Meme'})   

        db.query(Memes).filter(Memes.id == id).delete()
        db.commit()
    except:
        return JSONResponse(status_code=500)
