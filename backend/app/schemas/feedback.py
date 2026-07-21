from app.extensions import ma
from marshmallow import fields, validate
from app.schemas.user import UserResponseSchema


class NewFeedbackSchema(ma.Schema):
    content = fields.String(load_default=None,
                validate=validate.Length(max=2000, error="Post content cannot exceed 2000 words"))



class FeedbackResponseSchema(ma.Schema):
    public_id = fields.UUID()
    content = fields.String()
    date_created = fields.DateTime(format="iso")
    user = fields.Nested(UserResponseSchema, only=("public_id", "username", "profile"))
    