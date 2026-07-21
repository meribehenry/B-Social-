from app.extensions import ma
from marshmallow import fields


class ReportResponseSchema(ma.Schema):
    public_id = fields.UUID()
    type = fields.String()
    case_id = fields.String()
    category = fields.String()
    date = fields.DateTime(format="iso")