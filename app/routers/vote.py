from typing import List
from fastapi import FastAPI,Response,status,HTTPException,Depends , APIRouter
from .. import models , utils,schemas,oauth2
from ..database import get_db

from sqlalchemy.orm import Session


# POST API 

router = APIRouter(  # APIROuter will connect all the router files with The main.py
    prefix="/vote", #this will prefix /posts in all the Post Api URL
    tags=['Votes']  #This will group up the Api Docs based on the Tag on http://127.0.0.1:8000/docs
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post does not exist with ID {vote.post_id}")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    

    if (vote.dir == 1):
       if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on post {vote.post_id}")
       new_vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
       db.add(new_vote)
       db.commit()
       return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote did not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted vote"}

