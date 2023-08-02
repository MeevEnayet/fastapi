import fastapi
from jose import JWTError, jwt
from datetime import datetime, timedelta
import time
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import database, schemas, models
from .database import engine, get_db
from . import schemas
from sqlalchemy.orm import Session
from .config import settings
#secret_key
#algorithm hs256
#expiration time of the token 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        #decode the jwt token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #extract the id
        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        #validate the token_date with the schema
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= f"Could not validate credentials", headers= {"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()

    return user 






