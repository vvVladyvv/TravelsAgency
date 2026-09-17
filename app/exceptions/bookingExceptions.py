from fastapi import HTTPException

class UnavailableSeats(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = 503,
            detail = "Not Available Seats"
        )

