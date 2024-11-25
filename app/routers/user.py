from .. import models , utils,schemas
from ..database import get_db
from fastapi import Body, FastAPI,Response,status,HTTPException,Depends , APIRouter
from sqlalchemy.orm import Session


# Users API 

router = APIRouter( # APIROuter will connect all the router files with The main.py
    prefix="/users", #this will prefix /users in all the Post Api URL
    tags=['Users'] #This will group up the Api Docs based on the Tag on http://127.0.0.1:8000/docs
)

@router.post("/",status_code=status.HTTP_201_CREATED , response_model= schemas.UserOut)
async def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):

    # Hash the passowrd
    hashed_password =utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)#acts like Returning in Postgres Sql Query.
    return new_user


@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts WHERE id = %s """,(str(id),))
    # post= cursor.fetchone()
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} not found")
    return user