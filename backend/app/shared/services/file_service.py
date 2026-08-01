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
        
        extension = os.path.splitext(file.filename)[1]
        print(extension)
        if extension not in allowed_extensions:
            return None
        
        for type in file_types:
            if extension in file_types[type]:
                return {"file": file, "type": type, "extension": extension}
            

    def save_file(self, file_result, folder_name="folder"):
        random_name = secrets.token_hex(16)

        result = cloudinary.uploader.upload(
            file_result.get("file"),
            public_id = random_name,
            resoucre_type=file_result.get("type"),
            folder=folder_name #os.path.join(folder_name, file_result.get("type"))
        )

        return result["secure_url"], random_name


    def delete_file(self, public_id):
        cloudinary.uploader.destroy(public_id, invalidate=True)
        return True

