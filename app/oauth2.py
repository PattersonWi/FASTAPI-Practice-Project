from jose import JWTError, jwt 
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session  # this will allow you to declare the type of the db parameters and have better type checks and completion in your functions.
from . config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")


#Create a random secret key that will be used to sign the JWT tokens.
SECRET_KEY = settings.secret_key

#The algorithm used to sign the JWT token
ALGORITHM = settings.algorithm

#Variable for the expiration of the token
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict, ):

    to_enconde = data.copy()

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enconde.update({"exp":expire})

    encoded_jwt = jwt.encode(to_enconde, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id =id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f"Could not validate credentials", headers= {"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user