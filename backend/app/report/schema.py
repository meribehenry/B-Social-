from app.extensions import ma
from marshmallow import fields, post_load
import bleach


class ReportResponseSchema(ma.Schema):
    public_id = fields.String()
    type = fields.String()
    case_id = fields.String()
    case = fields.String()
    date = fields.DateTime(format="iso")


class NewReportSchema(ma.Schema):
    case = fields.String(required=True)

    @post_load
    def sanitize(self, data, **kwarg):

        if "case" in data:
            data["case"] = bleach.clean(data["case"], tags=[], strip=True).strip()

        return data