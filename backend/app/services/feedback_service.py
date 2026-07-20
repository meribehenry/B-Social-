from app.extensions import db
from app.models import Feedback
from flask import flash, abort
from datetime import datetime, timezone

class FeedbackService:
    def __init__(self, current_user):
        self.current_user = current_user

    def submit_feedback(self, feedback_text):
        # Logic to save feedback to the database
        feedback = Feedback(writer_id=self.current_user.id, 
                            text=feedback_text,  
                            writer_username = self.current_user.username, 
                            date=datetime.now(timezone.utc)
                            ) 
                        
        try:
            db.session.add(feedback)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error submitting feedback: {str(e)}", "danger")

        flash("Feedback submitted successfully!", "success")
        return feedback
    
    def delete_feedback(self, feedback):
        # Logic to delete feedback from the database
        
        try:
            db.session.delete(feedback)
            db.session.commit()
            flash("Feedback deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting feedback: {str(e)}", "danger")

        return True