from fastapi import UploadFile, HTTPException
from pathlib import Path
import shutil
from app.exceptions.imageExceptions import fileTooLarge, fileFormatNotSupported


def save_image(image: UploadFile, user_id: int):
    upload_path = Path("uploads")
   
    if image != None: 
        max_size = 5 * 1024 * 1024
        size = await image.read()
        if len(size) > max_size:
            raise fileTooLarge()

        #Extract suffix of file and restrict 3 types of suffix
        extension = Path(image.filename).suffix.lower()
        if extension not in [".jpg", ".png", ".jpeg"]:
            raise fileFormatNotSupported()

        #Generate file name
        image_uid = f"{uuid.uuid4()}{extension}"
        #Generate path of the file
        file_path = upload_path / image_uid

        #Reset cursor inside image bytes
        await image.seek(0)

        #Open file as buffer with "write" and "bytes" permissions, for modify it, then copy content in image inside our buffer object
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        return image_uid
    else:
        return None
