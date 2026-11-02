from fastapi import HTTPException

class fileTooLarge(HTTPException):
    def __init__(self):
        super().__init__(status_code=413, detail="File too large")

class fileFormatNotSupported(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Format supported is (.jpg, .jpeg, .png)")