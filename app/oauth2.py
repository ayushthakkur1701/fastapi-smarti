from jose import JWTError,jwt
from datetime import datetime , timedelta
from . import schemas , database , models

from fastapi import Depends, status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#secretKey
#Algorithim
#Expiration Time

SECRET_KEY = settings.secret_key
ALGORITHIM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
  to_encode =   data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp":expire})
  encoded_jwt = jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHIM)
  return encoded_jwt


def verify_access_token(token:str,credentials_expecption):
  try:
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHIM])
    id :str = payload.get("user_id")

    if id is None:
        raise credentials_expecption
    token_data = schemas.TokenData(id=id)
  except JWTError:
    raise credentials_expecption
  
  return token_data
  
def get_current_user(token:str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"www-Authenticate":"Bearer"})
  
  token = verify_access_token(token,credentials_exception)

  user = db.query(models.User).filter(models.User.id == token.id).first()

  return user
