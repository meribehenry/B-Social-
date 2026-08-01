from app.extensions import ma
from marshmallow import fields,  post_load
import bleach


class ModeratorTakeDownSchema(ma.Schema):
    password = fields.String(required=True)
    
    @post_load
    def sanitize(self, data, **kwarg):
        if "password" in data:
            data["password" ] = bleach.clean(data["password" ], tags=[], strip=True).strip()
            return data

class ModeratorChangeStatusSchema(ma.Schema):
    password = fields.String(required=True)
    status = fields.String(required=True)
    
    @post_load
    def sanitize(self, data, **kwarg):
        
        fields_to_sanitise = ["password", "status"]

        for field in fields_to_sanitise:
            if field in data:
                data[field] = bleach.clean(data[field], tags=[], strip=True).strip()
        return data