from app.models import Clicks
from app.extensions import db
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

def count_clicks(post, current_user):
    click = Clicks.query.filter_by(post_id=post.id, user_id=current_user.id).first()
    if not click:
        if post.author != current_user:
            click = Clicks(post_id=post.id, viewed=True, user_id=current_user.id, username=current_user.username)
            click.viewed = True
            post.num_of_clicks = post.num_of_clicks + 1
            db.session.add(click)
            db.session.commit()