from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.post import Post
from app.models.user import User
from app.services.file_service import FileService
from app.utils.sanitise import sanitise
from app.utils.pagination import create_pagination_dict
from app.utils.response import ServiceResponseBuilder
from app.schemas.profile import ProfileResponseSchema
from app.schemas.post import PostResponseSchema


profile_response_schema = ProfileResponseSchema()
posts_response_schema = PostResponseSchema(many=True)
service_response_builder = ServiceResponseBuilder()


class ProfileService():
    def __init__(self, user_public_id):
        self.current_user = User.query.filter_by(public_id=user_public_id).first_or_404()
        self.error = {}
        self.result = {}


    def edit_profile(self, data:dict, file):
        firstname = sanitise(data.get("firstname"))
        lastname = sanitise(data.get("lastname"))
        username = sanitise(data.get("username"))
        bio = sanitise(data.get("bio"))

        if not data.values() or (not file
                                and bio == self.current_user.profile.bio 
                                and firstname == self.current_user.profile.firstname 
                                and lastname == self.current_user.profile.lastname 
                                and username == self.current_user.username
                                ):
            
            self.error = service_response_builder.bad_request_error(message="Invalid request. Please enter atleast one field")
            return self.result, self.error 
        
        old_profile_pic_id = ""
        file_service = FileService()
        
        if file:
            file_result = file_service.handle_file(file, allowed_extensions=["jpg", "img", "png", "jpeg"])

            if self.current_user.profile.profile_pic_id != "default":
                old_profile_pic_id = self.current_user.profile.profile_pic_id

            self.current_user.profile.profile_pic_url, self.current_user.profile.profile_pic_id = file_service.save_file(file_result, folder_name="profile_pics")

        self.current_user.profile.bio = bio
        self.current_user.profile.firstname = firstname
        self.current_user.profile.lastname = lastname
        self.current_user.username = username

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

    
    def view_profile(self, user_public_id, per_page=20, page=1):
        user = User.query.filter_by(public_id=user_public_id).first()

        if not user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error 

        post_pagination = user.posts.query.order_by(Post.date_created.desc()).paginate(per_page=per_page, page=page)

        data = {
            "profile": profile_response_schema.dump(user.profile),
            "posts": posts_response_schema.dump(post_pagination.items),
            "pagination": create_pagination_dict(post_pagination)
        }

        self.result = service_response_builder.result(data=data)
        return self.result, self.error