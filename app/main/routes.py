from flask import Blueprint, render_template, request
from app.models import Post


main = Blueprint("main", __name__)


@main.route("/")
def landing_page():
    return render_template("main/landing_page.html", title="B-Social")


@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(per_page=20, page=page)
    return render_template("main/home.html", posts=posts, title="Home")


@main.route("/about")
def about():
    return render_template("main/about.html", title="About")