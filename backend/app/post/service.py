from datetime import datetime, timedelta, timezone
from flask import current_app
from app.post.models.post import Post, Media
from app.user.service import UserService
from app.extensions import db, logger
from sqlalchemy.exc import SQLAlchemyError
from app.shared.services.file_service import FileService
from app.shared.pagination import create_pagination_dict
from app.post.utils.record_clicks import record_clicks
from app.shared.response import ServiceResponseBuilder
from app.post.schema import PostResponseSchema
from sqlalchemy import update
from concurrent.futures import ThreadPoolExecutor


file_executor = ThreadPoolExecutor(max_workers=5)
count_executor = ThreadPoolExecutor(max_workers=5)
service_response_builder = ServiceResponseBuilder()
post_response_schema = PostResponseSchema()
posts_response_schema = PostResponseSchema(many=True)
user_service = UserService()


class PostService():

    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}

    def _delete_old_medias_file_from_db(self, old_post_medias:list):
        try:
            for media in old_post_medias:
                db.session.delete(media)
                db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to delete old medias")
            return False
  
    def __delete_old_medias_file_from_storage(self, old_post_medias:list):
        file_service = FileService()   
        if old_post_medias:
            logger.info(f"Deleting old media files from storage in a separate thread(background task)")
            for media in old_post_medias:
                file_service.delete_file(media.file_id)               

    def create_post(self, data:dict, files):
        content = data.get("content")

        if len(files) > 4:
            self.error = service_response_builder.bad_request_error(message="Only four files are supported max")
            return self.result, self.error

        if not content and not files:
            self.error = service_response_builder.bad_request_error(message="Please enter atleast one field (text or media)")
            return self.result, self.error

        post = Post(content=content, author=self.current_user)
        db.session.add(post)

        post_files = []

        if files:
            for file in files.values():
                if not file.filename:
                    return
                file_service = FileService()
                file_result = file_service.handle_file(file, allowed_extensions={".jpg", ".img", ".jpeg", ".png"})

                if not file_result:
                    self.error = service_response_builder.validation_error(message="Invalid file type. Please enter the correct type: [jpg, img, jpeg, png]")
                    return self.result, self.error

                media_type = file_result.get("type")
                storage_result = file_service.save_file(file_result, folder_name="posts")

                if not storage_result:
                    self.error = service_response_builder.internal_server_error(message="Could not create post")
                    return self.result, self.error

                post_files.append({"file_url": storage_result[0], "file_id": storage_result[1], "media_type": media_type})   
    
        try: 
            db.session.flush()  # Flush to get the post ID before committing 
            for file in post_files:
                media = Media(post_id=post.id, file_id=file.get("file_id"), file_url=file.get("file_url"), media_type=file.get("media_type")) 
                db.session.add(media)  
            db.session.commit()
            logger.info("Post created")

            app = current_app._get_current_object()
            count_executor.submit(user_service.update_count, app, self.current_user.public_id, "post")

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Failed to create post")
            self.error = service_response_builder.internal_server_error(message="Could not create post")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create post: {e}")
            self.error = service_response_builder.internal_server_error(message="Could not create post")
            return self.result, self.error 
        
        self.result = service_response_builder.result(message= "Post created successfully",
                                                      data= post_response_schema.dump(post), 
                                                      status_code=201)

        return self.result, self.error


    def edit_post(self, post_public_id, data:dict, files):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error 

        if self.current_user != post.author:
            self.error = service_response_builder.forbidden_error(message="You are not authorized to edit this post")
            return self.result, self.error

        if (post.date_created.replace(tzinfo=timezone.utc) + timedelta(hours=48)) <= (datetime.now(timezone.utc)):
            self.error = service_response_builder.validation_error(message="Cannot edit post after 48 hours")
            return self.result, self.error

        if len(files) > 4:
            self.error = service_response_builder.bad_request_error(message="Only four files are supported")
            return self.result, self.error

        new_content = data.get("content")

        if (not new_content or new_content == post.content) and not files:
            self.error = service_response_builder.bad_request_error(message="Please enter atleast one field (text or media)")
            return self.result, self.error 

        old_post_medias = ""  

        file_service = FileService()

        if files:
            if post.medias:
                old_post_medias = post.medias.all() # Store the old media before deletion

            for file in files.values():
                file_result = file_service.handle_file(file, allowed_extensions={".jpg", ".img", ".jpeg", ".png",})

                if not file_result:
                    self.error = service_response_builder.validation_error(message="Invalid file type. Please enter the correct type: [jpg, img, jpeg, png]")
                    return self.result, self.error

                media_type = file_result.get("type")
                storage_result = file_service.save_file(file_result, folder_name="posts")
                            
                if not storage_result:
                    self.error = service_response_builder.internal_server_error(message="Could not update post")
                    return self.result, self.error
    
                file_url, file_id = storage_result
                media = Media(post_id=post.id, file_id=file_id, file_url=file_url, media_type=media_type)
                db.session.add(media)
            
        post.content = new_content
        post.edited = True
        post.date_updated = datetime.now(timezone.utc)

        try:
            self._delete_old_medias_file_from_db(old_post_medias)  # Delete old media from the database
            db.session.commit()   
            file_executor.submit(self.__delete_old_medias_file_from_storage, old_post_medias)  # Delete old media from storage in a separate thread               

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to edit post")
            self.error = service_response_builder.internal_server_error(message="Could not update post")
            return self.result, self.error
        
        except Exception:
            db.session.rollback()
            logger.error("Failed to edit post")
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


        if self.current_user != post.author and (self.current_user.role != "moderator" and self.current_user.role != "admin"):
            self.error = service_response_builder.forbidden_error(message="You are not authorized to delete this post")
            return self.result, self.error

        old_post_medias = post.medias.all()  # Store the old media before deletion

        try:
            db.session.delete(post)
            db.session.commit()
            logger.info("Post deleted")

            # Background Tasks
            app = current_app._get_current_object()
            count_executor.submit(user_service.update_count, app, self.current_user.public_id, "post", increment=False)
            file_executor.submit(self.__delete_old_medias_file_from_storage, old_post_medias)  # Delete old media from storage in a separate thread

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to delete post")
            self.error = service_response_builder.internal_server_error(message="Could not delete post")
            return self.result, self.error 
        
        except Exception:
            db.session.rollback()
            logger.error("Failed to delete post")
            self.error = service_response_builder.internal_server_error(message="Could not delete post")
            return self.result, self.error 
        
        self.result = service_response_builder.result(message= "Post successfully deleted", status_code=200)
        
        return self.result, self.error
    

    def view_post(self, post_public_id):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error 

        record_clicks(post, self.current_user)  

        self.result = service_response_builder.result(data=post_response_schema.dump(post))
        return self.result, self.error
    
    
    def view_posts(self, per_page=20, page=1, user_public_id=None):
        query = Post.query
        if user_public_id:
            user = user_service.get_user_object(user_public_id)
            if user:
                query = query.filter_by(user_id=user.id)

        post_pagination = query.order_by(Post.date_created.desc()).paginate(per_page=per_page, page=page, error_out=False)
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


    def update_count(self, app, post_public_id, type_of_count="like", increment=True):
        
        with app.app_context():
            post = self.get_post_object(post_public_id)
            if not post: return None
            
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
                logger.info(f"Updated {type_of_count} count for post {post.public_id}")
                return True
            
            except SQLAlchemyError:
                db.session.rollback()
                logger.error(f"Failed to update post {type_of_count} count")
                return False
    
    @staticmethod
    def get_db_model():
        return Post