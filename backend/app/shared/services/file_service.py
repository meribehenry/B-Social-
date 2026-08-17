from app.extensions import logger
from werkzeug.utils import secure_filename
import secrets
import cloudinary.uploader
import os


class FileService():
    
    def handle_file(self, file, allowed_extensions):
        file_types = {
            "video": {".mp4", ".mkv"},
            "audio": {".mp3"},
            "photo": {".img", ".jpg", ".jpeg", ".png", ".svg"},
            "document": {".txt", ".doc"}
        }
        
        extension = os.path.splitext(secure_filename(file.filename))[1]
        if extension not in allowed_extensions:
            return None
        
        for type in file_types:
            if extension in file_types[type]:
                return {"file": file, "type": type, "extension": extension}
            

    def save_file(self, file_result, folder_name="folder"):
        resource_type = {
            "video": "video",
            "image": "image",
            "document": "raw",
            "audio": "raw"
        }
        random_name = secrets.token_hex(16)

        try:
            result = cloudinary.uploader.upload(
                file_result.get("file"),
                public_id = random_name,
                resoucre_type=resource_type.get(file_result.get("type")),
                folder=folder_name 
            )
            logger.info(f"Saved file to storage with public_id ({random_name})")
            return result["secure_url"], random_name
                
        
        except:
            logger.error(f"Could not save file to storage")


    def delete_file(self, public_id):
        try:
            cloudinary.uploader.destroy(public_id, invalidate=True)
            logger.info(f"Deleted file with public_id ({public_id}) from storage")
        except:
            logger.error(f"Could not delete file with public_id ({public_id}) from storage")   
            with open("old_media.txt", "a") as file:
                file.write(f"{public_id}\n")
                logger.info(f"File ({public_id}) added to old_media.txt")
                return False     
        return True

