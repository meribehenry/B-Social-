from flask import Blueprint, render_template


main = Blueprint("main", __name__)


@main.route("/")
def landing_page():
    return render_template("main/landing_page.html")


@main.route("/home")
def home():
    return render_template("main/home.html")


@main.route("/about")
def about():
    return render_template("main/about.html")