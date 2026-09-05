from app.post.models.click import Click
from concurrent.futures import ThreadPoolExecutor
from flask import current_app
from app.extensions import db, logger
from sqlalchemy.exc import SQLAlchemyError


count_executor = ThreadPoolExecutor(max_workers=5)


def record_clicks(post, current_user):
    click = Click.query.filter_by(post_id=post.id, user_id=current_user.id).first()

    if not click:
        if post.author != current_user:
            click = Click(post_id=post.id, viewed=True, user_id=current_user.id)
            click.viewed = True
            try: 
                db.session.add(click)
                db.session.commit()

            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Failed to record click")
                return

            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to record click")
                return

            from app.post.service import PostService
            app = current_app._get_current_object()
            count_executor.submit(PostService(current_user.public_id).update_count, app, post.public_id, type_of_count="clicks")
            return True