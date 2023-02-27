from typing import List
from fastapi import APIRouter, Depends

from src.models.user_model import Users
from ..database import get_db  # use .. to move up a module
from ..schemas.comment_schemas import *
from ..models.comments_model import *
from ..schemas import user_schemas
from .. import token
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
# create instance of router
router = APIRouter(
    prefix="/comment",
    tags=['comments'],
)


# route to get comments of a user and blog
@router.get('/{user_id}/{meme_id}')
async def get(user_id: int,meme_id:int, db: Session = Depends(get_db)):

    comment = db.query(Comments).filter(Comments.meme_id==meme_id,Comments.user_id==user_id).order_by(Comments.id.desc()).limit(100).all()

    if comment != None:

        return comment

    return JSONResponse(status_code=404,content={"message": "Comment Not Found"})


@router.post('/')
def post(comment:Comment , db: Session = Depends(get_db),
         current_user: user_schemas.UserDetails = Depends(token.get_current_user)):
    # hard code change afterward
    parent_id=comment.comment_id
    print(parent_id)

    parent=db.query(Comments).get(parent_id)
    print(parent)
    ob = Comments(text=comment.text,
                  user_id=current_user.id, meme_id=comment.meme_id,comment_id=parent_id)

    db.add(ob)
    db.commit()
    if parent:
        parent.reply_comment=ob

    db.commit()
    return {'success': True,}
    # db.refresh(ob)
    # print(memes.dict())

@router.patch('/')
def patch(comment:Comment , db: Session = Depends(get_db),
         current_user: user_schemas.UserDetails = Depends(token.get_current_user)):
    
    try:
        ob = db.query(Comments).filter(Comments.meme_id==comment.meme_id).first()
        if ob is None:
             return JSONResponse(status_code=404,content={'message':'Not Found'})
        if  ob.user_id != current_user.id:
             return JSONResponse(status_code=404,content={'message':'You Cannot Delete this Comment'})   

        ob.text = comment.text
       
        db.commit()
        return {'message':"Successful"}
        
    except:
        return JSONResponse(status_code=404,content={'message':'Not Found'})


# route to delete comment
@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(get_db),current_user:user_schemas.UserDetails= Depends(token.get_current_user)):
    try:
        ob = db.query(Comments).filter(Comments.id == id).first()
        if ob is None:
             return JSONResponse(status_code=404,content={'message':'Not Found'})
        print(current_user)     
        if ob.user_id != current_user.id:
             return JSONResponse(status_code=404,content={'message':'You Cannot Delete this Meme'})   

        db.query(Comments).filter(Comments.id == id).delete()
        db.commit()
        return {'message': "Successful"}
    except Exception as ex:
        return JSONResponse(content={'message':str(ex)},status_code=500)