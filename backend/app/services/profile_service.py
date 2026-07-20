from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from flask import flash
from app.services.media_service import MediaService

class ProfileService():
    def __init__(self, current_user):
        self.current_user = current_user

    def edit_profile(self, form, current_user):
        if (not form.profile_pic.data 
            and form.bio.data == current_user.profile.bio 
            and form.firstname.data == current_user.profile.firstname 
            and form.lastname.data == current_user.profile.lastname 
            and form.username.data == current_user.username):
            return True
        
        if form.profile_pic.data:
            media_service = MediaService()
            if self.current_user.profile.profile_pic_id != "default":
                media_service.delete_photo(self.current_user.profile.profile_pic_id)

            self.current_user.profile.profile_pic_url, self.current_user.profile.profile_pic_id = media_service.save_photo(form.profile_pic.data, folder_name="profile_pics")

        current_user.profile.bio = form.bio.data
        current_user.profile.firstname = form.firstname.data
        current_user.profile.lastname = form.lastname.data
        current_user.username = form.username.data

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash(f"Error please try again", "error")
            return None

        flash("Profile successfully updated", "success")
        return True
    
    def populate_form(self, form):
        form.bio.data =  self.current_user.profile.bio 
        form.firstname.data = self.current_user.profile.firstname 
        form.lastname.data = self.current_user.profile.lastname
        form.username.data = self.current_user.username
        return form
