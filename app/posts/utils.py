import secrets
import cloudinary.uploader

def save_photo(photo):
    random_name = secrets.token_hex(16)

    result = cloudinary.uploader.upload(
        photo,
        public_id = random_name,
        resoucre_type="image",
        folder="Posts"
    )

    return result["secure_url"], random_name


def delete_photo(public_id):
    cloudinary.uploader.destroy(public_id, invalidate=True)