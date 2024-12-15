from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post , user , auth , vote
from fastapi.middleware.cors import CORSMiddleware




# models.Base.metadata.create_all(bind=engine)   #not needed because alembic will take care of creating the tables using models.py

app = FastAPI()

#Specify your domain
origins = [
    "https://www.google.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)


app.include_router(user.router)

app.include_router(auth.router)

app.include_router(vote.router)

@app.get("/")
def root():
    
    return {"message":"Hello World ... deployed to server"}

