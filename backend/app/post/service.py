from datetime import datetime, timezone
from app.post.models.post import Post
from app.user.service import UserService
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.shared.services.file_service import FileService
from app.shared.pagination import create_pagination_dict
from app.post.utils.count_clicks import count_clicks
from app.shared.response import ServiceResponseBuilder
from app.post.schema import PostResponseSchema
from sqlalchemy import update


service_response_builder = ServiceResponseBuilder()
post_response_schema = PostResponseSchema()
posts_response_schema = PostResponseSchema(many=True)
user_service = UserService()


class PostService():
    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}
  

    def create_post(self, data:dict, file):
        content = data.get("content")

        if not content and not file:
            self.error = service_response_builder.bad_request_error(message="Please enter atleast one field (text or media)")
            return self.result, self.error
        
        post_type,  media_url, media_id = "text", "",""

        if file:
            file_service = FileService()
            file_result = file_service.handle_file(file, allowed_extensions={".jpg", ".img", ".jpeg", ".png", ".mp4"})

            if not file_result:
                self.error = service_response_builder.validation_error(message="Invalid file type. Please enter the correct type: [jpg, img, jpeg, png, mp4]")
                return self.result, self.error

            post_type = file_result.get("type")
            media_url, media_id = file_service.save_file(file_result, folder_name="posts")
            
        post = Post(content=content, media_url=media_url, media_id=media_id, type=post_type, author=self.current_user)
        
        try:
            db.session.add(post)
            db.session.commit()
            user_service.update_count(self.current_user, "post")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at post_service, create_post\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not create post")
            return self.result, self.error
        
        except Exception as e:
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

        if self.current_user != post.author:
            self.error = service_response_builder.forbidden_error(message="You are not authorized to edit this post")
            return self.result, self.error

        new_content = data.get("content")

        if (not new_content or new_content == post.content) and not file:
            self.error = service_response_builder.bad_request_error(message="Please enter atleast one field (text or media)")
            return self.result, self.error  

        old_post_media_id = ""    
        file_service = FileService()

        if file:
            file_result = file_service.handle_file(file, allowed_extensions={".jpg", ".img", ".jpeg", ".png", ".mp4"})

            if not file_result:
                self.error = service_response_builder.validation_error(message="Invalid file type. Please enter the correct type: [jpg, img, jpeg, png, mp4]")
                return self.result, self.error
            
            if post.media_url:
                old_post_media_id = post.media_id 

            post.type = file_result.get("type")
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

        if self.current_user != post.author:
            self.error = service_response_builder.forbidden_error(message="You are not authorized to delete this post")
            return self.result, self.error

        media_id = post.media_id
        file_service = FileService()

        try:
            db.session.delete(post)
            db.session.commit()
            user_service.update_count(self.current_user, "post", increment=False)
            file_service.delete_file(media_id) if media_id else None

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at post_service, delete_post\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete post")
            return self.result, self.error 
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at post_service, delete_post\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete post")
            return self.result, self.error 
        
        self.result = service_response_builder.result(message= "Post successfully deleted", status_code=200)
        
        return self.result, self.error
    

    def view_post(self, post_public_id):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error 
        
        count_clicks(post, post.author)

        self.result = service_response_builder.result(data=post_response_schema.dump(post))
        return self.result, self.error
    
    
    def view_posts(self, per_page=20, page=1):
        post_pagination = Post.query.order_by(Post.date_created.desc()).paginate(per_page=per_page, page=page)

        data = {
            "posts": posts_response_schema.dump(post_pagination.items),
            "pagination": create_pagination_dict(post_pagination)
        }

        self.result = service_response_builder.result(data=data)
        return self.result, self.error
    

    def get_post_object(self, post_public_id, return_bool=False):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not return_bool:
            return post
        
        return post is not None
    
    def update_count(self, post, type_of_count="like", increment=True):
        
        try:
            if type_of_count == "like":
                db.session.execute(
                    update(Post)
                    .where(Post.id==post.id)
                    .values(num_of_likes=(Post.num_of_likes + 1) if increment else (Post.num_of_likes - 1))
                    )
            
            elif type_of_count == "dislike":
                db.session.execute(
                    update(Post)
                    .where(Post.id==post.id)
                    .values(num_of_dislikes=(Post.num_of_dislikes + 1) if increment else (Post.num_of_dislikes - 1))
                    )
                
            elif type_of_count == "comment":
                db.session.execute(
                    update(Post)
                    .where(Post.id==post.id)
                    .values(num_of_comments=(Post.num_of_comments + 1) if increment else (Post.num_of_comments - 1))
                    )
                
            elif type_of_count == "clicks":
                db.session.execute(
                    update(Post)
                    .where(Post.id==post.id)
                    .values(num_of_clicks=(Post.num_of_clicks + 1) if increment else (Post.num_of_clicks - 1))
                    )
            else:
                raise Exception ("Invalid type_of_count")
            
            db.session.commit()
            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at post_service update_count\n{e}")
            return False