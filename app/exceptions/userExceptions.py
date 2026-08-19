from fastapi import HTTPException


class UserAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = 409,
            detail="User already exist"
        )

class InvalidCredentials(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Invalid Credentials"
        )

class UserNotFound(HTTPException):
     def __init__(self):
            super().__init__(
                status_code=404,
                detail="User Not Found"
            )

class AdminRequired(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Admin permission is required for this action")