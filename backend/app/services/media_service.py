import secrets
import cloudinary.uploader


class MediaService():
    def save_photo(self, photo, folder_name="folder"):
        random_name = secrets.token_hex(16)

        result = cloudinary.uploader.upload(
        photo,
        public_id = random_name,
        resoucre_type="image",
        folder=folder_name
    )

        return result["secure_url"], random_name


    def delete_photo(self, public_id):
        cloudinary.uploader.destroy(public_id, invalidate=True)
        return True

