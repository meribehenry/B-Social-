from app.models import Comment
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from flask import flash


class CommentService():
    def __init__(self, current_user):
        self.current_user = current_user
    
    def create_comment(self, form, post):
        comment = Comment(content=form.content.data, user_id=self.current_user.id, post=post)
        post.num_of_comments = post.num_of_comments + 1

        try:
            db.session.add(comment)
            db.session.commit()
        except SQLAlchemyError:
            post.num_of_comments = post.num_of_comments - 1
            db.session.rollback()
            flash(f"Error please try again", "danger")
            return None
        
        flash("Comment sent successfully", "success")
        return True
    
    def edit_comment(self, form, comment):
        if form.content.data == comment.content:
            return True
        
        comment.content = form.content.data
        try:
            db.session.add(comment)
        except SQLAlchemyError:
            db.session.rollback()
            flash(f"Error please try again", "danger")
            return None
        
        flash("Comment successfully edited", "success")
        return True
    
    def delete_comment(self, comment):
        post_public_id = comment.post.public_id
        comment.post.num_of_comments = comment.post.num_of_comments - 1
        
        try:
            db.session.delete(comment)
            db.session.commit()
        except SQLAlchemyError:
            comment.post.num_of_comments = comment.post.num_of_comments + 1
            db.session.rollback()
            flash(f"Error please try again", "danger")
            return None
        
        flash("Comment successfully deleted", "success")
        return post_public_id 
        
