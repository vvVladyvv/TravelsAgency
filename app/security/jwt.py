from jose import jwt, JWTError
from fastapi import HTTPException
from datetime import timedelta, datetime
from app.config import get_settings

settings = get_settings()

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
TIME_EXPIRED = settings.TIME_EXPIRED


def create_token(user: dict):
    data = user.copy()
    exp = datetime.utcnow() + timedelta(minutes=TIME_EXPIRED)
    data['exp'] = exp

    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    
        
        
