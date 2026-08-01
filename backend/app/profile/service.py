from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.user.service import UserService
from app.shared.services.file_service import FileService
from app.shared.response import ServiceResponseBuilder
from app.profile.schema import ProfileResponseSchema


profile_response_schema = ProfileResponseSchema()
service_response_builder = ServiceResponseBuilder()
user_service = UserService()


class ProfileService():
    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}


    def edit_profile(self, user_public_id, data:dict, file):
        print(self.current_user)
        if user_public_id != self.current_user.public_id:
            self.error = service_response_builder.forbidden_error(message="You are not authorized to edit this profile")
            return self.result, self.error
        
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        username = data.get("username")
        bio = data.get("bio")
        print(data.values())

        if (not firstname and not lastname and not username and not bio) and not file:     
            self.error = service_response_builder.bad_request_error(message="Invalid request. Please enter atleast one field")
            return self.result, self.error 
        
        old_profile_pic_id = ""
        file_service = FileService()
        
        if file:
            file_result = file_service.handle_file(file, allowed_extensions=[".jpg", ".img", ".png", ".jpeg"])

            if self.current_user.profile.profile_pic_id != "default":
                old_profile_pic_id = self.current_user.profile.profile_pic_id

            self.current_user.profile.profile_pic_url, self.current_user.profile.profile_pic_id = file_service.save_file(file_result, folder_name="profile_pics")

        self.current_user.profile.bio = bio if bio else self.current_user.profile.bio
        self.current_user.profile.firstname = firstname if firstname else self.current_user.profile.firstname
        self.current_user.profile.lastname = lastname if lastname else self.current_user.profile.lastname
        self.current_user.username = username if username else self.current_user.username

        try:
            db.session.commit()
            file_service.delete_file(old_profile_pic_id) if old_profile_pic_id else None

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at profile_service, edit_profile\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not update profile")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at profile_service, edit_profile\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not update profile")
            return self.result, self.error 
        
        self.result = service_response_builder.result(message="Profile successfully updated", 
                                                      data=profile_response_schema.dump(self.current_user.profile))

        return self.result, self.error

    
    def view_profile(self, user_public_id):
        user = user_service.get_user_object(user_public_id)

        if not user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error 

        self.result = service_response_builder.result(data=profile_response_schema.dump(user.profile))
        return self.result, self.error