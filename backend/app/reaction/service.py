from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from concurrent.futures import ThreadPoolExecutor
from app.comment.service import CommentService
from app.reaction.model import PostReaction, CommentReaction
from app.post.service import PostService
from app.user.service import UserService
from app.extensions import db, logger
from app.shared.response import ServiceResponseBuilder
from app.notification.service import NotificationService


service_response_builder = ServiceResponseBuilder()
user_service = UserService()
count_executor = ThreadPoolExecutor(max_workers=5)

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

                app = current_app._get_current_object()
                if reaction_type == "like":
                    count_executor.submit(PostService(self.current_user.public_id).update_count, app, post.public_id)
                else:
                    count_executor.submit(PostService(self.current_user.public_id).update_count, app, post.public_id, type_of_count="dislike")

                self.result = service_response_builder.result(f"Post {reaction_type}d", 201)

            else:
                if post_reaction.reaction_type == reaction_type:
                    self.error = service_response_builder.conflict_error(f"Post already {reaction_type}d")
                    return self.result, self.error
                
                post_reaction.reaction_type = reaction_type
                db.session.commit()

                app = current_app._get_current_object()
                if reaction_type == "like":
                    count_executor.submit(PostService(self.current_user.public_id).update_count, app, post.public_id)
                    count_executor.submit(PostService(self.current_user.public_id).update_count, app, post.public_id, type_of_count="dislike", increment=False)
                else:
                    count_executor.submit(PostService(self.current_user.public_id).update_count, app, post.public_id, type_of_count="dislike")
                    count_executor.submit(PostService(self.current_user.public_id).update_count, app, post.public_id, increment=False)

                self.result = service_response_builder.result(f"Changed to {reaction_type}d", 200)
                return self.result, self.error

            if post_reaction and post.author != self.current_user and post_reaction.reaction_type == "like":
                NotificationService(self.current_user.public_id).create_notification(post_reaction.post.author, 
                                                                                 content=f"{self.current_user.username} liked your post",
                                                                                 notification_type="like")

            return self.result, self.error

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to react to post")
            self.error = service_response_builder.internal_server_error("Could not react to post")  
            return self.result, self.error 

        except Exception:
            db.session.rollback()
            logger.error("Failed to react to post")
            self.error = service_response_builder.internal_server_error("Could not react to post")  
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

            app = current_app._get_current_object()
            if post_reaction.reaction_type == "like":
                count_executor.submit(PostService(self.current_user.public_id).update_count, app, post.public_id, increment=False)
            else:
                count_executor.submit(PostService(self.current_user.public_id).update_count, app, post.public_id, type_of_count="dislike", increment=False)

            self.result = service_response_builder.result("Reaction removed")
            return self.result, self.error
    
        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to remove reaction from post")
            self.error = service_response_builder.internal_server_error("Could not remove reaction from post")  
            return self.result, self.error 

        except Exception:
            db.session.rollback()
            logger.error("Failed to remove reaction from post")
            self.error = service_response_builder.internal_server_error("Could not remove reaction from post")  
            return self.result, self.error

    def get_reacted_posts_public_id_list(self):
        likes = []
        dislikes = []

        for reaction in self.current_user.post_reactions:
            if reaction.reaction_type == "like":
                likes.append(reaction.post.public_id)
            else:
                dislikes.append(reaction.post.public_id)

        data = {
                    "likes": likes,
                    "dislikes": dislikes
                }
        
        self.result = service_response_builder.result(data=data, status_code=200)
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
    
                app = current_app._get_current_object()
                if reaction_type == "like":
                    count_executor.submit(CommentService(self.current_user.public_id).update_count, app, comment.public_id)
                else:
                    count_executor.submit(CommentService(self.current_user.public_id).update_count, app, comment.public_id, type_of_count="dislike")

                self.result = service_response_builder.result(f"Comment {reaction_type}d", 201)

            else:
                if comment_reaction.reaction_type == reaction_type:
                    self.error = service_response_builder.conflict_error(f"Comment already {reaction_type}d")
                    return self.result, self.error
                comment_reaction.reaction_type = reaction_type
                db.session.commit()

                app = current_app._get_current_object()
                if reaction_type == "like":
                    count_executor.submit(CommentService(self.current_user.public_id).update_count, app, comment.public_id)
                    count_executor.submit(CommentService(self.current_user.public_id).update_count, app, comment.public_id, type_of_count="dislike", increment=False)
                else:
                    count_executor.submit(CommentService(self.current_user.public_id).update_count, app, comment.public_id, type_of_count="dislike")
                    count_executor.submit(CommentService(self.current_user.public_id).update_count, app, comment.public_id, increment=False)

                self.result = service_response_builder.result(f"Changed to {reaction_type}d", 200)
                return self.result, self.error

            if comment_reaction and comment.author != self.current_user and comment_reaction.reaction_type == "like":
                NotificationService(self.current_user.public_id).create_notification(comment.author, 
                                                                                 content=f"{self.current_user.username} liked your comment",
                                                                                 notification_type="like")
            return self.result, self.error

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to react to comment")
            self.error = service_response_builder.internal_server_error("Could not to react to comment")  
            return self.result, self.error 

        except Exception:
            db.session.rollback()
            logger.error("Failed to react to comment")
            self.error = service_response_builder.internal_server_error("Could not to react to comment")  
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

            app = current_app._get_current_object()
            if comment_reaction.reaction_type == "like":
                count_executor.submit(CommentService(self.current_user.public_id).update_count, app, comment.public_id, increment=False)
            else:
                count_executor.submit(CommentService(self.current_user.public_id).update_count, app, comment.public_id, type_of_count="dislike", increment=False)

            self.result = service_response_builder.result("Reaction removed")
            return self.result, self.error
        
        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to remove reaction from comment")
            self.error = service_response_builder.internal_server_error("Could not remove reaction from comment")  
            return self.result, self.error 

        except Exception:
            db.session.rollback()
            logger.error("Failed to remove reaction from comment")
            self.error = service_response_builder.internal_server_error("Could not remove reaction from comment")  
            return self.result, self.error 

    def get_reacted_comments_public_id_list(self):
            likes = []
            dislikes = []
    
            for reaction in self.current_user.comment_reactions.all():
                if reaction.reaction_type == "like":
                    likes.append(reaction.comment.public_id)
                else:
                    dislikes.append(reaction.comment.public_id)
    
            data = {
                        "likes": likes,
                        "dislikes": dislikes
                    }
            
            self.result = service_response_builder.result(data=data, status_code=200)
            return self.result, self.error 