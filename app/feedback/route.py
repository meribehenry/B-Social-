from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.feedback.form import FeedbackForm
from app.models import Feedback
from app.services.feedback_service import FeedbackService
from app.utils.decorators import verification_required

feedback = Blueprint("feedback", __name__)

@feedback.route("/submit_feedback", methods=["GET", "POST"])
@login_required
@verification_required
def submit_feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback_text = form.text.data    
        feedback_service = FeedbackService(current_user)
        feedback_service.submit_feedback(feedback_text)
        return redirect(url_for("feedback.view_feedbacks"))

    return render_template("feedback/submit_feedback.html", form=form, title="Submit Feedback")


@feedback.route("/delete_feedback/<int:feedback_id>", methods=["POST"])
@login_required
@verification_required
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback.writer_id != current_user:
            abort(403)
    feedback_service = FeedbackService(current_user)
    result = feedback_service.delete_feedback(feedback)

    if result is None:
         return redirect('feedback.view_feedbacks')
    return redirect(url_for("main.home"))

@feedback.route("/view_feedbacks")
def view_feedbacks():
    page = request.args.get("page", 1, type=int)
    feedbacks = Feedback.query.order_by(Feedback.date.desc()).paginate(per_page=20, page=page)
    return render_template("feedback/view_feedbacks.html", feedbacks=feedbacks, title="View Feedbacks")
