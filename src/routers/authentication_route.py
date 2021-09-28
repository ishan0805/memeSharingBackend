from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse
from .. schemas import login_schemas
from .. models import user_model
from .. import database ,hashing
from sqlalchemy.orm import Session
router =APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request:login_schemas.Login,db:Session =Depends(database.get_db)):
    user =db.query(user_model.Users).filter(user_model.Users.email == request.username).first()
    if not user:
         return JSONResponse(status_code=404, content={"message": "User Not Found"})

    if not hashing.verify_password(request.password,user.password):
         return JSONResponse(status_code=404, content={"message": "Incorrect Password"})

    return user     