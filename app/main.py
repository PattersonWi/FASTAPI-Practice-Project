from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, votes
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

#No longer needed since using alembic
# it tells sqlalchemy to run the create staments
# so that it generated all of the tables when we
# first start it
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
#CORS: Cross Origin Resources Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# grabs the router object from the post, auth and user files
# that essentialy is going to import all of the specific routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "This is the root folder"}
