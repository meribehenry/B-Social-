from app.post.service import PostService
from app.user.service import UserService
from app.profile.model import Profile
from app.shared.pagination import create_pagination_dict
from sqlalchemy import or_, and_
from app.shared.response import ServiceResponseBuilder
from app.search.schema import SearchUserResponseSchema



service_response_builder = ServiceResponseBuilder()
search_user_response_schema = SearchUserResponseSchema(many=True)

User = UserService.get_db_model()
Post = PostService.get_db_model()


class SearchService():
    def __init__(self):
        self.error = {}
        self.result = {}
    
    def global_search(self, data:dict, per_page=20, page=1):
        search_term = data.get("search_term")

        if not search_term :
            self.error = service_response_builder.bad_request_error(message="Please fill out the search field")
            return self.result, self.error
        

        # 1. Clean up and split search terms safely
        search_words = [word.strip() for word in search_term.split() if word.strip()]

        # 2. Start from User so users with 0 posts are NOT filtered out
        # Using outerjoin for both tables ensures everything stays visible
        query = (
            User.query
            .outerjoin(Profile, User.id == Profile.user_id)
            .outerjoin(Post, User.id == Post.user_id)
        )

        # 3. Apply cross-column multi-word filtering safely
        if search_words:
            word_filters = []
            
            for clean_word in search_words:
                word_filters.append(
                    or_(
                        User.username.ilike(f"%{clean_word}%"),
                        Profile.firstname.ilike(f"%{clean_word}%"),
                        Profile.lastname.ilike(f"%{clean_word}%"),
                        Post.content.ilike(f"%{clean_word}%")  # Handles NULL automatically if no posts exist
                    )
                )
    
            # Chain conditions: Word 1 matches something AND Word 2 matches something
            query = query.filter(and_(*word_filters))

        # 4. Finalize with uniqueness, sorting by user creation or ID, and pagination
        # Note: Sorting by Post.date_created can push users with 0 posts to the bottom 
        # because their post date is NULL. Sorting by User.id keeps it consistent.
        result_pagination = (
            query.distinct()
            .order_by(User.id.desc()) 
            .paginate(per_page=per_page, page=page, error_out=False)
        )

        # 5. Serialize using your user schema instead of post schema
        data = {
            "users": search_user_response_schema.dump(result_pagination.items),
            "pagination": create_pagination_dict(result_pagination)
        }

        self.result = service_response_builder.result(data=data)
        return self.result, self.error