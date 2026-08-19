from passlib.context import CryptContext

security = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed_password(password):
    return security.hash(password)

def verify_password(password, hash_password):
    return security.verify(password, hash_password)