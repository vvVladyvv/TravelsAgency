from fastapi import HTTPException

class TravelAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = 409,
            detail = "Travel already exist"
        )

class TravelNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Travel not found"
        )

