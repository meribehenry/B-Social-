from flask import flash

from app.models import Post
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.services.media_service import MediaService

class PostService():
    def __init__(self, current_user):
        self.current_user = current_user
    

    def create_post(self, form):
        if not form.content.data and not form.photo.data:
            flash("Cannot post empty an post")
            return None
        
        post_type,  photo_url, photo_id = "text", "",""

        if form.photo.data:
            media_service = MediaService()
            post_type = "photo"
            photo_url, photo_id = media_service.save_photo(form.photo.data)
            
        post = Post(content=form.content.data, photo_url=photo_url, photo_id=photo_id, post_type=post_type, author=self.current_user)
        

        try:
            db.session.add(post)
            self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts + 1
            db.session.commit()

        except SQLAlchemyError:
            self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts - 1
            db.session.rollback()
            flash(f"Error please try again", "danger")
            return None
        
        flash("You created a new post", "success")
        return True


    def edit_post(self, form, post):
        if form.content.data == post.content and not form.photo.data:
            return True
        
        
        if form.photo.data:
            media_service = MediaService()
            post.post_type = "photo"
            post.photo_url , post.photo_id = media_service.save_photo(form.photo.data, folder_name="post_pics")
            print(f"post.photo_url: {post.photo_url}, post.photo_id: {post.photo_id}, post.post_type: {post.post_type}")
            
            if post.photo_url:
                media_service.delete_photo(post.photo_id)
            
        post.content = form.content.data
        post.edited = True
        print(f"post.photo_url: {post.photo_url}, post.photo_id: {post.photo_id}, post.post_type: {post.post_type}")
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash(f"Error please try again", "danger")
            return None
        
        flash("Post successfully updated", "success")
        return post
    

    def delete_post(self, post):
        photo_id = post.photo_id
        self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts - 1
        media_service = MediaService()

        try:
            db.session.delete(post)
            db.session.commit()
            db.session.expire_all()
            media_service.delete_photo(photo_id) if photo_id else None

        except SQLAlchemyError:
            self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts + 1
            db.session.rollback()
            flash(f"Error please try again", "danger")
            return None
        
        flash("Post successfully deleted", "success")
        return True