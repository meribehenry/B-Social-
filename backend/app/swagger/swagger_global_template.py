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
                        },

            "RateLimitErrorResponse":  {
                                        "type": "object",
                                        "properties": {
                                            "success": {
                                                "type": "boolean",
                                                "example": False
                                            },
                                            "error": {
                                                "type": "string",
                                                "example": "Too many requests"
                                            },
                                            "message": {
                                                "type": "string",
                                                "example": "Too many requests try again in 60 seconds"
                                            }
                                        },
                                            
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
                    }

                #     "files": {
                #         "type": "object",
                #         "description": "Optional field for image or video files. It only optional if content is added"
                #     }
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
            "UserResponseSchema": {
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
                        "example": True
                    },

                    "status": {
                        "type": "string",
                        "example": "active"
                    },

                    "role": {
                        "type": "string",
                        "example": "moderator"
                    },

                    "date_joined": {
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
                            },
                        }
                    }
                }

            },
            "PostResponseSchema": {
                "type": "object",
                "properties": {
                    "public_id": {
                        "type": "string",
                        "example": "02dbc4da-cacb-4a8e-9b9e-9e8bbdaaa964"
                    },
                    "content": {
                        "type": "string",
                        "example": "My very first post"
                    },
                    "date_created": {
                        "type": "datetime",
                        "format": "iso",
                        "example": "2026-08-11T13:50:10.902126"
                    },
                    "date_updated": {
                        "type": "datetime",
                        "format": "iso",
                        "example": "2026-09-11T13:50:10.902126"
                    },
                    "edited": {
                        "type": "boolean",
                        "example": True
                    },
                    "num_of_likes": {
                        "type": "integer",
                        "example": 10
                    },
                    "num_of_dislikes": {
                        "type": "integer",
                        "example": 0
                    },
                    "num_of_comments": {
                        "type": "integer",
                        "example": 3
                    },
                    "num_of_clicks": {
                        "type": "integer",
                        "example": 14
                    },
                    "medias": {
                        "type": "array",
                        "example": [
                            {
                                "file_url": "https://res.cloudinary.com/ddzmfmexsk/image/upload/v1786452336/profile_pics/7f747b7eca92258e196a25fe117f31dc.jpg",
                                "file_type": "photo"
                            },
                            {
                                "file_url": "https://res.cloudinary.com/ddzmfmexsk/image/upload/v1786452336/profile_pics/7f747b7eca92258e196a25fe117f31dc.jpg",
                                "file_type": "video"
                            }
                        ]
                    },
                    "author": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "example": "MeribeHenry"
                            },
                            "public_id": {
                                "type": "string",
                                "example": "02dbc4da-cacb-4a8e-9b9e-9e8bbdaaa965"
                            },
                            "profile": {
                                "type": "object",
                                "properties": {
                                    "firstname": {
                                        "type": "string",
                                        "example": "Meribe"
                                    },
                                    "lastname": {
                                        "type": "string",
                                        "example": "Henry"
                                    },
                                    "profile_pic_url": {
                                        "type": "string",
                                        "example": "https://res.cloudinary.com/ddzmfmexsk/image/upload/v1786452336/profile_pics/7f747b7eca92258e196a25fe117f31dc.jpg",
                                        "description": "default.jgp is the default profile image you want to use for user with none. It doesn't link to any image you decide it"
                                    },

                                }
                            }
                        }
                    }
                }
            },
            "CommentResponseSchema": {
                "type": "object",
                "properties": {
                    "public_id": {
                        "type": "string",
                        "example": "02dbc4da-cacb-4a8e-9b9e-9e8bbdaaa964"
                    },
                    "content": {
                        "type": "string",
                        "example": "I really love this post"
                    },
                    "date_created": {
                        "type": "datetime",
                        "format": "iso",
                        "example": "2026-08-11T14:50:10.905626"
                    },
                    "date_updated": {
                        "type": "datetime",
                        "format": "iso",
                        "example": "2026-09-11T14:51:16.608126"
                    },
                    "edited": {
                        "type": "boolean",
                        "example": True
                    },
                    "num_of_likes": {
                        "type": "integer",
                        "example": 10
                    },
                    "num_of_dislikes": {
                        "type": "integer",
                        "example": 0
                    },
                    "author": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "example": "johnnyDep"
                            },
                            "public_id": {
                                "type": "string",
                                "example": "02dbc4da-cacb-4a8e-9b9e-9e8bbdaaa965"
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
                                    },
                                }
                            }
                        }
                    }
                }
            },
            "ProfileResponseSchema": {
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
                    },
                    "bio": {
                        "type": "string",
                        "example": "Software Developer at B-Code"
                    },
                    "user": {
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
                                "example": True
                            },
        
                            "status": {
                                "type": "string",
                                "example": "active"
                            },
        
                            "role": {
                                "type": "string",
                                "example": "moderator"
                            },
        
                            "date_joined": {
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
                                    },
                                    "bio": {
                                        "type": "string",
                                        "example": "A software developer, I build scalable and reliable systems for company"
                                    },
                                }
                            }
                        }
                    }
                }
            },
            "FeedbackResponseSchema": {
                "type": "object",
                "properties": {
                    "public_id": {
                        "type": "string",
                        "example": "02dbc4da-cacb-4a8e-9b9e-9e8bbdaaa964"
                    },
                    "content": {
                        "type": "string",
                        "example": "I really like the concept of the app but it wasn't completed 😌"
                    },
                    "date_created": {
                        "type": "datetime",
                        "format": "iso",
                        "example": "2026-08-11T14:50:10.905626"
                    },
                    "writer": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "example": "MiaBella"
                            },
                            "public_id": {
                                "type": "string",
                                "example": "02dbc4da-cacb-4a8e-9b9e-9e8bbdaaa965"
                            },
                            "profile": {
                                "type": "object",
                                "properties": {
                                    "firstname": {
                                        "type": "string",
                                        "example": "Mia"
                                    },
                                    "lastname": {
                                        "type": "string",
                                        "example": "Bella"
                                    },
                                    "profile_pic_url": {
                                        "type": "string",
                                        "example": "https://res.cloudinary.com/ddzmfmexsk/image/upload/v1786452336/profile_pics/7f747b7eca92258e196a25fe117f31dc.jpg",
                                        "description": "default.jgp is the default profile image you want to use for user with none. It doesn't link to any image you decide it"
                                    },
                                }
                            }
                        }
                    }
                }
            },
            "ReportResponseSchema": {
                "type": "object",
                "properties": {
                    "public_id": {
                        "type": "string",
                        "example": "02dbc4da-cacb-4a8e-9b9e-9e8bbdaaa964"
                    },
                    "case_type": {
                        "type": "string",
                        "example": "post"
                    },
                    "date": {
                        "type": "datetime",
                        "format": "iso",
                        "example": "2026-08-11T14:50:10.905626"
                    },
                    "reported_case": {
                        "type": "string",
                        "example": "This post contains abusive content"
                    },
                    "reported_case_id": {
                        "type": "string",
                        "example": "02ddf4da-cacb-4a8e-9b9e-9e8bbdaaa504"
                    }
                }
            },
            "SearchResponseSchema": {
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
                    "status": {
                        "type": "string",
                        "example": "active"
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
                            },
                        }
                    },
                    "posts": {
                        "type": "array",
                        "example": [
                            {
                                "author": {
                                    "profile": {
                                        "firstname": "Meribe",
                                        "lastname": "Henry",
                                        "profile_pic_url": "https://res.cloudinary.com/ddzmfmexs/image/upload/v1786452336/profile_pics/7f747b7eca92258e196a25fe117f31dc.jpg"
                                    },
                                    "public_id": "65621469-6257-42bc-a7e0-4c45be8cd662",
                                    "username": "MeribeHenry"
                                },
                                "content": "Me self don tire 2",
                                "date_created": "2026-08-10T07:30:21.280164",
                                "date_updated": "2026-08-10T07:32:90.190172",
                                "edited": False,
                                "medias": [
                                    {
                                        "file_url": "",
                                        "media_type": ""
                                    }
                                ],
                                "num_of_clicks": 0,
                                "num_of_comments": 0,
                                "num_of_dislikes": 0,
                                "num_of_likes": 1,
                                "public_id": "f32da7c6-8dbc-4e3e-a084-d5f9f36c8dee"
                            }
                        ]
                    }
                }
            },
            "NotificationResponseSchema": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "example": "MiaBella followed you"
                    },
                    "date_created": {
                        "type": "datetime",
                        "format": "iso",
                        "example": "2026-08-11T14:50:10.905626"
                    },
                    "type": {
                        "type": "string",
                        "example": "like",
                        "description": "This can either be (like), (follow) or (info)"
                    },
                    "recipient": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "example": "MeribeHenry"
                            },
                            "public_id": {
                                "type": "string",
                                "example": "02dbc4da-cacb-4a8e-9b9e-9e8bbdaaa965"
                            }
                        }
                    },     
                    "actor": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "example": "MiaBella"
                            },
                            "public_id": {
                                "type": "string",
                                "example": "02dbc4da-cacb-4a8e-9b9e-9e8bbdaaa965"
                            },
                            "profile": {
                                "type": "object",
                                "properties": {
                                    "firstname": {
                                        "type": "string",
                                        "example": "Mia"
                                    },
                                    "lastname": {
                                        "type": "string",
                                        "example": "Bella"
                                    },
                                    "profile_pic_url": {
                                        "type": "string",
                                        "example": "https://res.cloudinary.com/ddzmfmexsk/image/upload/v1786452336/profile_pics/7f747b7eca92258e196a25fe117f31dc.jpg",
                                        "description": "default.jgp is the default profile image you want to use for user with none. It doesn't link to any image you decide it"
                                    },
                                }
                            }
                        }
                    }
                }
            },
            "NotificationStreamResponseSchema": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "example": "MiaBella liked your post"
                    },
                    "date_created": {
                        "type": "datetime",
                        "format": "iso",
                        "example": "2026-08-11T14:50:10.905626"
                    },
                    "type": {
                        "type": "string",
                        "example": "like",
                        "description": "This can either be (like), (follow) or (info)"
                    }
                }
            },
            "PaginationSchema": {
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "example": 10,
                        "description": "This represent the current page"
                    },
                    "per_page": {
                        "type": "integer",
                        "example": 20,
                        "description": "This represent the number of items page"
                    },
                    "total": {
                        "type": "integer",
                        "example": 15,
                        "description": "This represent the number total number of items across all pages"
                    },
                    "pages": {
                        "type": "integer",
                        "example": 15,
                        "description": "This represent the number total number of pages"
                    },
                    "has_next": {
                        "type": "boolean",
                        "example": True,
                        "description": "True if it not the last page"
                    },
                    "has_prev": {
                        "type": "boolean",
                        "example": True,
                        "description": "True if it not the first page"
                    },
                    "next_page": {
                        "type": "integer",
                        "example": 3,
                        "description": "The next page number, or None if this is the last page."        
                    },
                    "prev_page": {
                        "type": "integer",
                        "example": 2,
                        "description": "The previous page number, or None if this is the first page."        
                    }
                }
            }
        }
    }
}