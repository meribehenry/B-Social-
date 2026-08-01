from app.extensions import ma
from marshmallow import fields, validate


class NewFeedbackSchema(ma.Schema):
    content = fields.String(validate=validate.Length(max=500, error="Feedback content cannot exceed 500 words"))



class FeedbackResponseSchema(ma.Schema):
    public_id = fields.UUID()
    content = fields.String()
    date_created = fields.DateTime(format="iso")
    writer = fields.Nested("UserResponseSchema", only=("public_id", "username", "profile"))
    