from app.models import Follower
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError

class FollowerService():
    def __init__(self, current_user):
        self.current_user = current_user
    
    def follow_user(self, followed_user):
        follower = Follower.query.filter_by(followed_user_id=followed_user.id, follower_id=self.current_user.id).first()
        if follower:
            return follower
        
        follower = Follower(follower_id=self.current_user.id, followed_user=followed_user) 

        try:
            db.session.add(follower)
            followed_user.profile.num_of_followers = followed_user.profile.num_of_followers + 1
            db.session.commit()
        except SQLAlchemyError:
            followed_user.profile.num_of_followers = followed_user.profile.num_of_followers - 1
            db.session.rollback()
            return None
        
        return follower
    
    def unfollow_user(self, followed_user):
        follower = Follower.query.filter_by(followed_user_id=followed_user.id, follower_id=self.current_user.id).first()
        followed_user.profile.num_of_followers = followed_user.profile.num_of_followers - 1

        try:
            db.session.delete(follower)
            db.session.commit()
        except SQLAlchemyError:
            followed_user.profile.num_of_followers = followed_user.profile.num_of_followers + 1
            db.session.rollback()
            return None
        
        return None