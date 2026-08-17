temaplate = {
    "openapi": "3.0.0",
    "info": {
        "title": "B-Social API",
        "description": """Welcome to B-Social API Documentation.""",
        "version": "1.0.0",
        "contact": {
            "name": "Meribe Henry",
            "email": "meribehenry09@gmail.com"
        }
    },

    "server": [
        {
            "url": "http://127.0.0.1:5000/api/v1",
            "description": "Local Development Server"
            }
    ],

    "components": {
        "schemas": {
            # ------------------------ RESPONSE --------------------------

            # --------- REUSABLE SUCCESS RESPONSE SCHEMA ---------
            "SuccessResponse": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "example": True
                    },
                    "message": {
                        "type": "string",
                        "example": "Operation successful"
                    },
                    "data": {
                        "type": "object",
                        "description": "Optional payload data" 
                    }
                },
                "required": ["success"]     
            },

            # --------- REUSABLE ERROR RESPONSE SCHEMAS ---------
            "ErrorResponse":  {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "example": False
                    },
                    "error": {
                        "type": "string",
                        "example": "Error"
                    },
                    "message": {
                        "type": "string",
                        "example": "An error occured"
                    }
                },
                "required": ["success", "error", "message"]     
            },

            "BadRequestErrorResponse":  {
                            "type": "object",
                            "properties": {
                                "success": {
                                    "type": "boolean",
                                    "example": False
                                },
                                "error": {
                                    "type": "string",
                                    "example": "Bad Request"
                                },
                                "message": {
                                    "type": "string",
                                    "example": "The request you sent is invalid"
                                }
                            },
                            "required": ["success", "error", "message"]     
                        },

            "InternalServerErrorResponse":  {
                            "type": "object",
                            "properties": {
                                "success": {
                                    "type": "boolean",
                                    "example": False
                                },
                                "error": {
                                    "type": "string",
                                    "example": "Internal Server"
                                },
                                "message": {
                                    "type": "string",
                                    "example": "An error occured. Please try again soon"
                                }
                            },
                            "required": ["success", "error", "message"]     
                        },

            # --------- REUSABLE MARSHMALLOW SCHEMA ERROR RESPONSE SCHEMA ---------
            "SchemaErrorResponse": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "example": True
                    },
                    "message": {
                        "type": "string",
                        "example": "Validation failed"
                    },
                    "errors": {
                        "type": "object",
                        "description": "Key-value map of field names to validation error messages",
                        "additionalProperties": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "example": {
                            "field": ["Field must not be empty"]
                        }
                    }
                },
                "required": ["success", "message", "errors"]    
            },

            # --------- REUSABLE AUTH REQUEST SCHEMAS ---------

            # LOGIN REQUEST
            "LoginRequest": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "format": "email",
                        "example": "henry@example.com"
                    },

                    "password": {
                        "type": "string",
                        "format": "password",
                        "example": "password123$"
                    }
                },
                "required": ["email", "password"]
            },

            # REGISTRATION REQUEST
            "RegistrationRequest": {
                "type": "object",
                "properties": {
                    "firstname": {
                        "type": "string",
                        "example": "Johnny"
                    },

                    "lastname": {
                        "type": "string",
                        "example": "Dep"
                    },

                    "email": {
                        "type": "string",
                        "format": "email",
                        "example": "henry@example.com"
                    },

                    "password": {
                        "type": "string",
                        "format": "password",
                        "example": "password123$"
                    },

                    "confirm_password": {
                        "type": "string",
                        "format": "password",
                        "example": "password123$",
                        "description": "Must match the password field"
                    },
                    "gender": {
                        "type": "String",
                        "format": "enum",
                        "example": "female",
                        "description": "Either male or female"
                    }
                },
                "required": ["firstname", "lastname", "email", "password", "confirm_password", "gender"]
            },

            # VERIFY EMAIL REQUEST
            "VerifyEmailRequest": {
                "type": "object",
                "properties": {
                    "otp_code": {
                        "type":"integer",
                        "example": "35690"
                    }
                },
                "required": ["otp_code"]
            },

            # PASSWORD RESET REQUEST
            "RequestPasswordResetRequest": {
                "type": "object",
                "properties": {
                        "email": {
                        "type": "string",
                        "format": "email",
                        "example": "henry@example.com"
                    }
                },
                "required": ["email"]
            },

            # PASSWORD RESET REQUEST
            "PasswordResetRequest": {
                "type": "object",
                "properties": {
                    "password": {
                        "type": "string",
                        "format": "password",
                        "example": "password123$"
                    },

                    "confirm_password": {
                        "type": "string",
                        "format": "password",
                        "example": "password123$",
                        "description": "Must match the password field"
                    }                       
                },

                "required": ["password", "confirm_password"]
            },

            # --------- REUSABLE ADMIN REQUEST SCHEMAS ---------

            # ADMIN CHANGE ROLE REQUEST
            "AdminChangeRoleRequest": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "example": "johnnyDep"
                    },

                    "role": {
                        "type": "string",
                        "format": "enum",
                        "example": "moderator",
                        "description": "Must be either admin, user or moderator"
                    },

                    "password": {
                        "type": "string",
                        "format": "password",
                        "example": "password123"
                    }
                },
                "required": ["username", "role", "password"]
            },

            # ADMIN CHANGE STATUS REQUEST
            "AdminChangeStatusRequest": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "format": "enum",
                        "example": "active",
                        "description": "Must be either active or suspended"
                    },

                    "password": {
                        "type": "string",
                        "format": "password",
                        "example": "password123"
                    }
                },
                "required": ["status", "password"]
            },

            # --------- REUSABLE COMMENT REQUEST SCHEMAS ---------

            # COMMENT REQUEST
            "CommentRequest": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "example": "I really love this post"
                    }
                },
                "required": ["content"]
            },

            # --------- REUSABLE FEEDBACK REQUEST SCHEMAS ---------

            # FEEDBACK REQUEST
            "FeedbackRequest": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "example": "This app is really good"
                    }
                },
                "required": ["content"]
            },

            # --------- REUSABLE MODERATOR REQUEST SCHEMAS ---------

            # MODERATOR CHANGE STATUS REQUEST
            "ModeratorChangeStatusRequest": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "format": "enum",
                        "example": "active",
                        "description": "Must be either active or suspended"
                    },

                    "password": {
                        "type": "string",
                        "format": "password",
                        "example": "password123"
                    }
                },
                "required": ["status", "password"]
            },

            # MODERATOR TAKEDOWN REQUEST
            "ModeratorTakeDownRequest": {
                "type": "object",
                "properties": {
                    "password": {
                        "type": "string",
                        "format": "password",
                        "example": "password123"
                    }        
                }
            },

            # --------- REUSABLE POST REQUEST SCHEMAS ---------

            # POST REQUEST
            "PostRequest": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "example": "My very first post",
                        "description": "Optional only if the files are added"
                    },

                    "files": {
                        "type": "object",
                        "description": "Optional field for image or video files. It only optional if content is added"
                    }
                }
            },    

            # --------- REUSABLE PROFILE REQUEST SCHEMAS ---------
            
            # EDIT PROFILE REQUEST
            "EditProfileRequest": {
                "type": "object",
                "properties": {

                    "firstname": {
                        "type": "string",
                        "example": "Johnny"
                    },

                    "lastname": {
                        "type": "string",
                        "example": "Dep"
                    },

                    "username": {
                        "type": "string",
                        "example": "johnnyDep"
                    },

                    "bio": {
                        "type": "text",
                        "example": "I love music and also a sport person"
                    },
                }
            },

            # --------- REUSABLE REACTION REQUEST SCHEMAS ---------
            
            # REACTION REQUEST
            "ReactionRequest": {
                "type": "object",
                "properties": {
                    "reaction_type": {
                        "type": "string",
                        "format": "enum",
                        "example": "like",
                        "descripion": "Must be either like or dislike "
                    }
                },
                "required": ["reaction_type"]
            },

            # --------- REUSABLE REPORT REQUEST SCHEMAS ---------
            
            # REPORT REQUEST
            "ReportRequest": {
                "type": "object",
                "properties": {
                    "reported_case_id": {
                        "type": "string",
                        "example": "02dbc4da-cacb-4a8e-9b9e-8e8bbdaaa964",
                        "descripion": "The public_id of the case been reported"
                    },

                    "reported_case": {
                        "type": "string",
                        "example": "This post contain abusive content",
                    },

                    "case_type": {
                        "type": "string",
                        "format": "enum",
                        "example": "post",
                        "description": "Must be either post, comment or user."
                    }
                },
                "required": ["reported_case_id", "reported_case", "case_type"]
            },


            # --------- REUSABLE USER RESPONSE SCHEMAS ---------
            "UserResponse": {
                "type": "object",
                "properties": {
                    "public_id": {
                        "type": "string",
                        "example": "02dbc4da-cacb-4a8e-9b9e-8e8bbdaaa964"
                    },

                    "username": {
                        "type": "string",
                        "example": "jonnyDep"
                    },

                    "is_verified": {
                        "type": "boolean",
                        "example": False
                    },

                    "status": {
                        "type": "string",
                        "example": "active"
                    },

                    "role": {
                        "type": "string",
                        "example": "moderator"
                    },

                    "role": {
                        "type": "datetime",
                        "format": "iso",
                        "example": "2026-08-11T13:50:10.902126"
                    },

                    "profile": {
                        "type": "object",
                        "properties": {
                            "firstname": {
                                "type": "string",
                                "example": "Johnny"
                            },
                            "lastname": {
                                "type": "string",
                                "example": "Dep"
                            },
                            "profile_pic_url": {
                                "type": "string",
                                "example": "https://res.cloudinary.com/ddzmfmexsk/image/upload/v1786452336/profile_pics/7f747b7eca92258e196a25fe117f31dc.jpg",
                                "description": "default.jgp is the default profile image you want to use for user with none. It doesn't link to any image you decide it"
                            }
                        }
                    }
                }

            }

        }
    }
}