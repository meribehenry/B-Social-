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
    reported_case_id = fields.String(required=True)
    reported_case = fields.String(required=True)
    case_type = fields.String(required=True)

    @post_load
    def sanitise(self, data, **kwarg):
        fields_to_sanitise = ["reported_case_id", "reported_case", "case_type"]

        for field in fields_to_sanitise:
            if field in data and data[field] is not None:
                data[field] = bleach.clean(data[field], tags=[], strip=True).strip()
        return data