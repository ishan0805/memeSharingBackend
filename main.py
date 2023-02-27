from typing import Optional
from fastapi import FastAPI
from src.database import engine, Base
from src.routers import meme_route, user_route, authentication_route,comment_router
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/swagger-ui/', port=8000)

app.include_router(authentication_route.router)
app.include_router(meme_route.router)
app.include_router(user_route.router)
app.include_router(comment_router.router)
# for Cors control
# enable support for ors
origins = [
    "*", '40023', '34469'
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
