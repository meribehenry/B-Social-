from flask import Blueprint, render_template, redirect, request, url_for, flash, abort
from app.models import Post, Comment
from app.extensions import db
from .forms import NewPostForm
from flask_login import login_required, current_user
from .utils import save_photo, delete_photo

posts = Blueprint("posts", __name__)


@posts.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    form = NewPostForm()
    post_type = "text"
    photo_url, photo_id = "",""

    if form.validate_on_submit():
        if form.photo.data:
            post_type = "photo"
            photo_url, photo_id = save_photo(form.photo.data)
            
        post = Post(content=form.content.data, photo_url=photo_url, photo_id=photo_id, post_type=post_type, author=current_user)
        current_user.num_of_posts += 1

        try:
            db.session.add(post)
            db.session.add(current_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}. Please try again", "danger")
            return redirect(url_for("posts.new_post"))
        
        flash("You created a new post", "success")
        return redirect(url_for("main.home"))

    return render_template("posts/new_post.html", form=form, title="New Post")


@posts.route("/update/<int:post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = NewPostForm()
    post_type = "text"
    photo_url, photo_id = "",""

    if form.validate_on_submit():
        if form.photo.data:
            if post.photo_url:
                delete_photo(post.photo_id)

            post_type = "photo"
            photo_url, photo_id = save_photo(form.photo.data)
            
        post.content = form.content.data
        post.photo_url = photo_url
        post.photo_id = photo_id
        post.post_type = post_type
        post.edited = True

        try:
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}. Please try again", "danger")
            return redirect(url_for("posts.update_post", post_id=post_id))
        
        flash("Post successfully updated", "success")
        return redirect(url_for("posts.view_post", post_id=post.id))
    
    elif request.method == "GET":
        form.content.data = post.content
    
    return render_template("posts/new_post.html", form=form, title="Update Post", photo_url=post.photo_url if post.photo_url else None)
        

@posts.route("/view/<int:post_id>")
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user:
        post.num_of_clicks = post.num_of_clicks + 1
        db.session.commit()

    page = request.args.get("page", 1, type=int)
    comments = post.comments.order_by(Comment.date_created.desc()).paginate(page=page, per_page=20)
    return render_template("posts/view_post.html", post=post, title="View Post", comments=comments)

@posts.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    photo_id = post.photo_id
    if post.author != current_user:
        abort(403)

    try:
        db.session.delete(post)
        current_user.num_of_posts = current_user.num_of_posts - 1
        db.session.commit()
        db.session.expire_all()
        delete_photo(photo_id) if photo_id else None
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}. Please try again", "danger")
        return redirect(url_for("posts.view_post", post_id=post_id))
    
    flash("Post successfully deleted", "success")
    return redirect(url_for("main.home"))