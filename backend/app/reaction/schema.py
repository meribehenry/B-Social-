from app.extensions import ma
from marshmallow import fields, post_load
import bleach


class ReactionSchema(ma.Schema):
    reaction_type = fields.String(required=True)

    @post_load
    def sanitize(self, data, **kwarg):
        if "reaction_type" in data:
            data["reaction_type"] = bleach.clean(data["reaction_type"], tags=[], strip=True).strip()
            return data