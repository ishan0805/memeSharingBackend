from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse
from .. schemas import login_schemas
from .. models import user_model
from .. import database ,hashing,token
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


router =APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session =Depends(database.get_db)):
    user =db.query(user_model.Users).filter(user_model.Users.email == request.username).first()
    if not user:
         return JSONResponse(status_code=404, content={"message": "User Not Found"})

    if not hashing.verify_password(request.password,user.password):
         return JSONResponse(status_code=404, content={"message": "Incorrect Password"})
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}    

    