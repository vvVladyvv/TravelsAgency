from fastapi import UploadFile, HTTPException
from pathlib import Path
import shutil
from uuid import uuid4
from app.exceptions.imageExceptions import fileTooLarge, fileFormatNotSupported


async def save_image(new_image: UploadFile, older_image: str = None):
    # Delete the older image file if exists
    if older_image:
        older_image_path = Path("uploads") / older_image
        if older_image_path.exists():
            older_image_path.unlink()  
    
    upload_path = Path("uploads")
    max_size = 5 * 1024 * 1024
    size = await new_image.read()
    if len(size) > max_size:
        raise fileTooLarge()

    #Extract suffix of file and restrict 3 types of suffix
    extension = Path(new_image.filename).suffix.lower()
    if extension not in [".jpg", ".png", ".jpeg"]:
        raise fileFormatNotSupported()

    #Generate file name
    image_uid = f"{uuid4()}{extension}"
    #Generate path of the file
    file_path = upload_path / image_uid

    #Reset cursor inside image bytes
    await new_image.seek(0)

    #Open file as buffer with "write" and "bytes" permissions, for modify it, then copy content in image inside our buffer object
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(new_image.file, buffer)
        
    return image_uid
