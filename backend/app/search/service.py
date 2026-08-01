from app.post.models.post import Post
from app.user.model import User
from app.profile.model import Profile
from app.shared.pagination import create_pagination_dict
from sqlalchemy import or_, and_
from app.shared.response import ServiceResponseBuilder
from app.search.schema import SearchResponseSchema



service_response_builder = ServiceResponseBuilder()
search_response_schema = SearchResponseSchema(many=True)


class SearchService():
    def __init__(self):
        self.error = {}
        self.result = {}
    
    def global_search(self, data:dict, per_page=20, page=1):
        search_term = data.get("search_term")

        if not search_term :
            self.error = service_response_builder.bad_request_error(message="Please fill out the search field")
            return self.result, self.error
        

        # 1. Clean up and split the search term into individual words
        # Example: "  John   Doe  " becomes ["John", "Doe"]
        words = [word.strip() for word in search_term.split() if word.strip()]

        # 2. Build the base query with your required database table joins
        query = (
        Post.query
        .join(User, Post.user_id == User.id)
        .join(Profile, User.id == Profile.user_id)
        )

        # 3. Apply the conditions conditionally based on what the user typed
        if words:
            word_filters = []

            for word in words:
                # Every individual word must match AT LEAST one of these columns
                word_filters.append(
                    or_(
                        Post.content.ilike(f"%{word}%"),
                        User.username.ilike(f"%{word}%"),
                        Profile.firstname.ilike(f"%{word}%"),
                        Profile.lastname.ilike(f"%{word}%")
                    )
                )

            # Use and_() to chain them: Word 1 must match something AND Word 2 must match something
            query = query.filter(and_(*word_filters))

        # 4. Finalize with sorting and pagination
        result_pagination = (
        query
        .order_by(Post.date_created.desc())
        .paginate(per_page=per_page, page=page, error_out=False)
                )


        data = {
            "posts": search_response_schema.dump(result_pagination.items),
            "pagination": create_pagination_dict(result_pagination)
        }

        self.result = service_response_builder.result(data=data)
        return self.result, self.error