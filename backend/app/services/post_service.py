from datetime import datetime, timezone
from app.models.post import Post
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.services.file_service import FileService
from app.utils.sanitise import sanitise
from app.utils.pagination import create_pagination_dict
from app.utils.count_clicks import count_clicks
from app.utils.response import ServiceResponseBuilder
from app.schemas.post import PostResponseSchema
from app.schemas.comment import CommentResponseSchema


service_response_builder = ServiceResponseBuilder()
post_response_schema = PostResponseSchema()
posts_response_schema = PostResponseSchema(many=True)
comments_response_schema = CommentResponseSchema(many=True)


class PostService():
    def __init__(self, user_public_id):
        self.current_user = User.query.filter_by(public_id=user_public_id).first_or_404()
        self.error = {}
        self.result = {}
  

    def create_post(self, data:dict, file):
        content = sanitise(data.get("content"))

        if not content and not file:
            self.error = service_response_builder.bad_request_error(message="Please enter atleast one field (text or media)")
            return self.result, self.error
        
        post_type,  media_url, media_id = "text", "",""

        if file:
            file_service = FileService()
            file_result = file_service.handle_file(file, allowed_extensions={"jpg, img, jpeg, png, mp4"})

            if not file_result:
                self.error = service_response_builder.validation_error(message="Invalid file type. Please enter the correct type: [jpg, img, jpeg, png, mp4]")
                return self.result, self.error

            post_type = file_result.get("type")
            media_url, media_id = file_service.save_file(file_result, folder_name="posts")
            
        post = Post(content=content, media_url=media_url, media_id=media_id, post_type=post_type, author=self.current_user)
        
        try:
            db.session.add(post)
            self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts + 1
            db.session.commit()

        except SQLAlchemyError as e:
            self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts - 1
            db.session.rollback()
            print(f"Sqlalchemy error at post_service, create_post\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not create post")
            return self.result, self.error
        
        except Exception as e:
            self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts - 1
            db.session.rollback()
            print(f"An error at post_service, create_post\n{e}")

            self.error = service_response_builder.internal_server_error(message="Could not create post")
            return self.result, self.error 
        
        self.result = service_response_builder.result(message= "Post created successfully",
                                                      data= post_response_schema.dump(post), 
                                                      status_code=201)

        return self.result, self.error


    def edit_post(self, post_public_id, data:dict, file):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error 

        new_content = sanitise(data.get("content"))

        if (not new_content or new_content == post.content) and not file:
            self.error = service_response_builder.bad_request_error(message="Please enter atleast one field (text or media)")
            return self.result, self.error  

        old_post_media_id = ""    
        file_service = FileService()

        if file:
            file_result = file_service.handle_file(file, allowed_extensions={"jpg, img, jpeg, png, mp4"})

            if not file_result:
                self.error = service_response_builder.validation_error(message="Invalid file type. Please enter the correct type: [jpg, img, jpeg, png, mp4]")
                return self.result, self.error
            
            if post.media_url:
                old_post_media_id = post.media_id 

            post.post_type = file_result.get("type")
            post.media_url , post.media_id = file_service.save_file(file_result, folder_name="posts")
            
        post.content = new_content
        post.edited = True
        post.date_updated = datetime.now(timezone.utc)

        try:
            db.session.commit()
            file_service.delete_file(old_post_media_id) if old_post_media_id else None
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at post_service, edit_post\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not update post")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at post_service, edit_post\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not update post")
            return self.result, self.error 
        
        self.result = service_response_builder.result(message= "Post successfully updated",
                                                      data= post_response_schema.dump(post))

        return self.result, self.error
   

    def delete_post(self, post_public_id):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error 

        media_id = post.media_id
        self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts - 1
        file_service = FileService()

        try:
            db.session.delete(post)
            db.session.commit()
            db.session.expire_all()
            file_service.delete_file(media_id) if media_id else None

        except SQLAlchemyError as e:
            self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts + 1
            db.session.rollback()
            print(f"SQLAlchemy error at post_service, delete_post\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete post")
            return self.result, self.error 
        
        except Exception as e:
            self.current_user.profile.num_of_posts = self.current_user.profile.num_of_posts + 1
            db.session.rollback()
            print(f"An error at post_service, delete_post\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete post")
            return self.result, self.error 
        
        self.result = service_response_builder.result(message= "Post successfully deleted", status_code=200)
        
        return self.result, self.error
    

    def view_post(self, post_public_id, per_page=20, page=1):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error 
        
        comment_pagination = post.comments.query.order_by(Post.date_created.desc()).paginate(per_page=per_page, page=page)

        data = {
            "post": post_response_schema.dump(post),
            "comments":  comments_response_schema.dump(comment_pagination.items),
            "pagination": create_pagination_dict(comment_pagination)
        }

        count_clicks(post, post.author)

        self.result = service_response_builder.result(data=data)
        return self.result, self.error
    
    
    def view_posts(self, per_page=20, page=1):
        post_pagination = Post.query.order_by(Post.date_created.desc()).paginate(per_page=per_page, page=page)

        data = {
            "posts": posts_response_schema.dump(post_pagination.items),
            "pagination": create_pagination_dict(post_pagination)
        }

        self.result = service_response_builder.result(data=data)
        return self.result, self.error