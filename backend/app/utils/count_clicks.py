from app.models.click import Click
from app.extensions import db

def count_clicks(post, current_user):
    click = Click.query.filter_by(post_id=post.id, user_id=current_user.id).first()
    if not click:
        if post.author != current_user:
            click = Click(post_id=post.id, viewed=True, user_id=current_user.id)
            click.viewed = True
            post.num_of_clicks = post.num_of_clicks + 1
            db.session.add(click)
            db.session.commit()