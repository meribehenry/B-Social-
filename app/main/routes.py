from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from app.models import Post
from app.utils.decorators import verification_required
from app.utils.reaction_dict import get_user_post_reactions_dict
from app.utils.follower_dict import get_follower_dict


main = Blueprint("main", __name__)


@main.route("/")
def landing_page():
    return render_template("main/landing_page.html", title="B-Social")


@main.route("/home")
@login_required
@verification_required
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(per_page=20, page=page)
    post_reactions_dict = get_user_post_reactions_dict(current_user)
    follower_dict = get_follower_dict(current_user)
    return render_template("main/home.html", posts=posts, title="Home", post_reactions_dict=post_reactions_dict, follower_dict=follower_dict)


@main.route("/about")
def about():
    return render_template("main/about.html", title="About")