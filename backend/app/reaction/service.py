from sqlalchemy.exc import SQLAlchemyError
from app.comment.service import CommentService
from app.reaction.model import PostReaction, CommentReaction
from app.post.service import PostService
from app.user.service import UserService
from app.extensions import db
from app.shared.response import ServiceResponseBuilder
from app.notification.service import NotificationService


service_response_builder = ServiceResponseBuilder()
user_service = UserService()

class BaseReactionService():
    model = None

    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}
    

class PostReactionService(BaseReactionService):
    model = PostReaction  

    def toggle_reaction(self, post_public_id, reaction_type):
        if reaction_type not in ("like", "dislike"):
            self.error = service_response_builder.bad_request_error("Invalid reaction type")
            return  self.result, self.error

        post = PostService(self.current_user.public_id).get_post_object(post_public_id)
        if not post:
            self.error = service_response_builder.not_found_error("Post not found")
            return self.result, self.error

        post_reaction = self.model.query.filter_by(post_id=post.id, user_id=self.current_user.id).first()

        try:
            if post_reaction is None:
                post_reaction = self.model(reaction_type=reaction_type, post_id=post.id, user_id=self.current_user.id)
                db.session.add(post_reaction)
                db.session.commit()

                if reaction_type == "like":
                    PostService(self.current_user.public_id).update_count(post)
                else:
                    PostService(self.current_user.public_id).update_count(post, type_of_count="dislike")

                self.result = service_response_builder.result(f"{reaction_type}d", 201)
                return self.result, self.error

            else:
                post_reaction.reaction_type = reaction_type
                db.session.commit()

                if reaction_type == "like":
                    PostService(self.current_user.public_id).update_count(post)
                    PostService(self.current_user.public_id).update_count(post, type_of_count="dislike", increment=False)
                else:
                    PostService(self.current_user.public_id).update_count(post, type_of_count="dislike")
                    PostService(self.current_user.public_id).update_count(post, increment=False)

                self.result = service_response_builder.result(f"Changed to {reaction_type}d", 200)

            if post_reaction and post.author != self.current_user and post_reaction.reaction_type == "like":
                NotificationService(self.current_user.public_id).create_notification(post_reaction.post.author, 
                                                                                 content=f"{self.current_user.username} liked your post",
                                                                                 notification_type="like")

            return self.result, self.error

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at reaction_service under post_reaction_service toggle_reaction\n{e}")
            self.error = service_response_builder.internal_server_error("Something went wrong")  
            return self.result, self.error 

        except Exception as e:
            db.session.rollback()
            print(f"An error at reaction_service under post_reaction_service toggle_reaction\n{e}")
            self.error = service_response_builder.internal_server_error("Something went wrong")  
            return self.result, self.error 
    

    def remove_reaction(self, post_public_id):
        
        post = PostService(self.current_user.public_id).get_post_object(post_public_id)
        if not post:
            self.error = service_response_builder.not_found_error("Post not found")
            return self.result, self.error
        
        post_reaction = self.model.query.filter_by(post_id=post.id, user_id=self.current_user.id).first()
        if not post_reaction:
            self.error = service_response_builder.not_found_error("No reaction found")
            return self.result, self.error 
        
        try:
            db.session.delete(post_reaction) 
            db.session.commit()
            
            if post_reaction.reaction_type == "like":
                PostService(self.current_user.public_id).update_count(post, increment=False)
            else:
                PostService(self.current_user.public_id).update_count(post, type_of_count="dislike", increment=False)

            self.result = service_response_builder.result("Reaction removed")
            return self.result, self.error
    
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at reaction_service under post_reaction_service remove_reaction\n{e}")
            self.error = service_response_builder.internal_server_error("Something went wrong")  
            return self.result, self.error 

        except Exception as e:
            db.session.rollback()
            print(f"An error at reaction_service under post_reaction_service remove_reaction\n{e}")
            self.error = service_response_builder.internal_server_error("Something went wrong")  
            return self.result, self.error


class CommentReactionService(BaseReactionService):
    model = CommentReaction

    def toggle_reaction(self, comment_public_id, reaction_type):
        if reaction_type not in ("like", "dislike"):
            self.error = service_response_builder.bad_request_error("Invalid reaction type")
            return  self.result, self.error

        comment = CommentService(self.current_user.public_id).get_comment_object(comment_public_id)
        if not comment: 
            self.error = service_response_builder.not_found_error("Comment not found")
            return self.result, self.error

        comment_reaction = self.model.query.filter_by(comment_id=comment.id, user_id=self.current_user.id).first()

        try:
            if comment_reaction is None:
                comment_reaction = self.model(reaction_type=reaction_type, post_id=comment.post.id, comment_id=comment.id, user_id=self.current_user.id)
                db.session.add(comment_reaction)
                db.session.commit()

                if reaction_type == "like":
                    CommentService(self.current_user.public_id).update_count(comment)
                else:
                    CommentService(self.current_user.public_id).update_count(comment, type_of_count="dislike")

                self.result = service_response_builder.result(f"{reaction_type}d", 201)
                return self.result, self.error

            else:
                comment_reaction.reaction_type = reaction_type
                db.session.commit()

                if reaction_type == "like":
                    CommentService(self.current_user.public_id).update_count(comment)
                    CommentService(self.current_user.public_id).update_count(comment, type_of_count="dislike", increment=False)
                else:
                    CommentService(self.current_user.public_id).update_count(comment, type_of_count="dislike")
                    CommentService(self.current_user.public_id).update_count(comment, increment=False)

                self.result = service_response_builder.result(f"Changed to {reaction_type}d", 200)

            if comment_reaction and comment.author != self.current_user and comment_reaction.reaction_type == "like":
                NotificationService(self.current_user.public_id).create_notification(comment.author, 
                                                                                 content=f"{self.current_user.username} liked your comment",
                                                                                 notification_type="like")
            return self.result, self.error

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at reaction_service under comment_reaction_service toggle_reaction\n{e}")
            self.error = service_response_builder.internal_server_error("Something went wrong")  
            return self.result, self.error 

        except Exception as e:
            db.session.rollback()
            print(f"An error at reaction_service under commentreaction_service toggle_reaction\n{e}")
            self.error = service_response_builder.internal_server_error("Something went wrong")  
            return self.result, self.error 
    

    def remove_reaction(self, comment_public_id):
        comment = CommentService(self.current_user.public_id).get_comment_object(comment_public_id)

        if not comment: 
            self.error = service_response_builder.not_found_error("Comment not found")
            return self.result, self.error

        comment_reaction = self.model.query.filter_by(comment_id=comment.id, user_id=self.current_user.id).first()
        if not comment_reaction:
            self.error = service_response_builder.not_found_error("No reaction found")
            return self.result, self.error 

        try:    
            db.session.delete(comment_reaction)
            db.session.commit()

            if comment_reaction.reaction_type == "like":
                CommentService(self.current_user.public_id).update_count(comment, increment=False)
            else:
                CommentService(self.current_user.public_id).update_count(comment, type_of_count="dislike", increment=False)

            self.result = service_response_builder.result("Reaction removed")
            return self.result, self.error
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at reaction_service under comment_reaction_service remove_reaction\n{e}")
            self.error = service_response_builder.internal_server_error("Something went wrong")  
            return self.result, self.error 

        except Exception as e:
            db.session.rollback()
            print(f"An error at reaction_service under commentreaction_service remove_reaction\n{e}")
            self.error = service_response_builder.internal_server_error("Something went wrong")  
            return self.result, self.error 