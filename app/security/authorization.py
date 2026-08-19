from fastapi.security import HTTPBearer
from fastapi import Depends
from app.security.jwt import verify_token
from app.exceptions.userExceptions import AdminRequired


oauth2_scheme = HTTPBearer()

def get_current_user(credentials = Depends(oauth2_scheme)):
   return verify_token(credentials.credentials)

def get_admin(credentials = Depends(oauth2_scheme)):
      token = verify_token(credentials.credentials)
      if token["role"] == "admin":
           return token
      return None
      