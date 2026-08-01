from datetime import datetime, timezone

from app.comment.model import Comment
from app.user.service import UserService
from app.post.service import PostService
from sqlalchemy import update
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.shared.pagination import create_pagination_dict
from app.shared.response import  ServiceResponseBuilder
from app.comment.schema import CommentResponseSchema
from app.notification.service import NotificationService

comments_response_schema = CommentResponseSchema(many=True)
comment_response_schema = CommentResponseSchema()
service_response_builder = ServiceResponseBuilder()
user_service = UserService()


class CommentService():
    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}
    
    def create_comment(self, post_public_id, data:dict):
        post = PostService(self.current_user.public_id).get_post_object(post_public_id)

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error 
        
        content = data.get("content")

        if not content:
            self.error = service_response_builder.bad_request_error(message="Comment field cannot be empty")
            return self.result, self.error 
            
        comment = Comment(content=content, user_id=self.current_user.id, post=post)
        
        try:
            db.session.add(comment)
            db.session.commit()
            PostService(self.current_user.public_id).update_count(comment.post, type_of_count="comment")
            print(f"Comment created successfully and updated comment count for post")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at comment_service, create_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not create comment")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at comment_service, create_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not create comment")
            return self.result, self.error
        
        # Create notification for the comment author
        if comment.post.author != self.current_user:
            NotificationService(self.current_user.public_id).create_notification(
                    comment.post.author,
                    content=f"{self.current_user.username} commented on your post",
                    notification_type="comment"
                )
        self.result = service_response_builder.result(message="Comment created successfully", 
                                                      data= comment_response_schema.dump(comment),
                                                      status_code=201)

        return self.result, self.error
    
    def edit_comment(self, comment_public_id, data:dict):
        comment = Comment.query.filter_by(public_id=comment_public_id).first_or_404()
        if not comment:
            self.error = service_response_builder.not_found_error(message="Comment not found")
            return self.result, self.error 

        if self.current_user != comment.author:
            self.error = service_response_builder.forbidden_error(message="You are not authorized to edit this comment")
            return self.result, self.error
        
        new_content = data.get("content")

        if not new_content or new_content == comment.content:
            self.error = service_response_builder.bad_request_error(message="Comment field cannot be empty or left the same")
            return self.result, self.error 
        
        comment.content = new_content
        comment.date_updated = datetime.now(timezone.utc)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at comment_service, edit_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not update comment")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at comment_service, edit_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not update comment")
            return self.result, self.error
        
        self.result = service_response_builder.result(message="Comment successfully updated", 
                                                      data= comment_response_schema.dump(comment))
        
        return self.result, self.error
        
    
    def delete_comment(self, comment_public_id):
        comment = Comment.query.filter_by(public_id=comment_public_id).first()
        
        if not comment:
            self.error = service_response_builder.not_found_error(message="Comment not found")
            return self.result, self.error 

        if self.current_user != comment.author:
            self.error = service_response_builder.forbidden_error(message="You are not authorized to delete this comment")
            return self.result, self.error
        
        post = comment.post

        try:
            db.session.delete(comment)
            # db.session.expire_all()
            db.session.commit()
            PostService(self.current_user.public_id).update_count(post, type_of_count="comment", increment=False)

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at comment_service, delete_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete comment")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"SQLAlchemy error at comment_service, delete_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete comment")
            return self.result, self.error
        
        self.result = service_response_builder.result(message="Comment successfully deleted")
        return self.result, self.error
    

    def view_comment(self, comment_public_id):
        comment = Comment.query.filter_by(public_id=comment_public_id).first()

        if not comment:
            self.error = service_response_builder.not_found_error(message="Comment not found")
            return self.result, self.error 

        self.result = service_response_builder.result(data=comment_response_schema.dump(comment))
        return self.result, self.error

    
    def view_comments(self, post_public_id, per_page=20, page=1):
        post = PostService(self.current_user.public_id).get_post_object(post_public_id)
        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error
         
        comment_pagination = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_created.desc()).paginate(per_page=per_page, page=page)

        data = {
            "comments": comments_response_schema.dump(comment_pagination.items),
            "pagination": create_pagination_dict(comment_pagination)
        }

        self.result = service_response_builder.result(data=data)
        return self.result, self.error
    
    def get_comment_object(self, comment_public_id, return_bool=False):
        comment = Comment.query.filter_by(public_id=comment_public_id).first()

        if not return_bool:
            return comment
        
        return comment is not None
    

    def update_count(self, comment, type_of_count="like", increment=True):
        
        try:
            if type_of_count == "like":
                db.session.execute(
                    update(Comment)
                    .where(Comment.id==comment.id)
                    .values(num_of_likes=(Comment.num_of_likes + 1) if increment else (Comment.num_of_likes - 1))
                    )
            
            elif type_of_count == "dislike":
                db.session.execute(
                    update(Comment)
                    .where(Comment.id==comment.id)
                    .values(num_of_dislikes=(Comment.num_of_dislikes + 1) if increment else (Comment.num_of_dislikes - 1))
                    )
            else:
                raise Exception ("Invalid type_of_count")
            
            db.session.commit()
            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at comment_service update_count\n{e}")
            return False