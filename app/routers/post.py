from typing import List
from fastapi import FastAPI,Response,status,HTTPException,Depends , APIRouter
from .. import models , utils,schemas,oauth2
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session


# POST API 

router = APIRouter(  # APIROuter will connect all the router files with The main.py
    prefix="/posts", #this will prefix /posts in all the Post Api URL
    tags=['Posts']  #This will group up the Api Docs based on the Tag on http://127.0.0.1:8000/docs
)

# , response_model= List[schemas.Post]
@router.get("/", response_model= List[schemas.PostWithVotes])
async def get_posts(db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).all() # .filter(models.Post.owner_id == current_user.id)
    
    
    results =db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()
    # Transform results into the new schema   [{"Post": post, "votes": votes} for post, votes in results]
    return results

@router.post("/",status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
async def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    print(current_user)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#acts like Returning in Postgres Sql Query.
    return new_post

@router.get("/{id}",response_model= schemas.PostWithVotes)
def get_post(id:int, db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * from posts WHERE id = %s """,(str(id),))
    # post= cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    posts =db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()
   
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    return posts

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def post_delete(id:int , db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # For deleting API, Fast Api does not return anything but 204 code response only. Delete api cannot return anything but the status code 204 itself.

    # cursor.execute(""" DELETE from posts WHERE id = %s RETURNING * """,(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit() # to commit to database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} is not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to delete the post")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.Post)
async def post_update(id:int,post:schemas.PostCreate , db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):

    # cursor.execute(""" UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s RETURNING *""", (post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone() 
    # conn.commit()

    posts_query = db.query(models.Post).filter(models.Post.id == id)

    update_post = posts_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} is not found.") 
    
    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to update the post")
    
    posts_query.update(post.dict(),synchronize_session=False) # post.dict() is same as passing Key value of post fields Like {'title':post.title,content:post.content}
  
    db.commit() 

    return posts_query.first()
