from flask import jsonify

class APIResponse():

    @staticmethod
    def success(data=None, message="Success", status_code=200):
        """For any success response, examples 200 OK, 204 etc."""
        body = {"success": True, "message":message}
        if data:
            body["data"] = data
        return jsonify(body), status_code
    
    @staticmethod
    def created(data=None, message="Created"):
        return APIResponse.success(data=data, message=message, status_code=201)
    
    @staticmethod
    def error(error=None, message="An error occurred", status_code=400):
        body = {"success": False, "message":message}
        if error:
            body["error"] = error
        return jsonify(body), status_code
    
    @staticmethod
    def forbidden(error=None, message="You are Unauthorized"):
        return APIResponse.error(error=error, message=message, status_code=403)
    
    @staticmethod
    def not_found(error=None, message="The resource you requested does not exist"):
        return APIResponse.error(error=error, message=message, status_code=404)
    
    @staticmethod
    def vallidation_error(error=None, message="Validation failed. Please check your inputs"):
        return APIResponse.error(error=error, message=message, status_code=422)
    
    @staticmethod
    def internal_server_error(error=None, message="Something went wrong. Please try again"):
        return APIResponse.error(error=error, message=message, status_code=500)
    
    @staticmethod
    def schema_error(errors=None, message="Validation failed. Please check your inputs", status_code=422):
        body = {"success": False, "message":message}
        if errors:
            body["errors"] = errors
        return jsonify(body), status_code

