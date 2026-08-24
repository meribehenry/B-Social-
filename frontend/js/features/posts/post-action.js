import { handleViewComments } from "../comments/comment-action.js";
import { handlePostDislikeReaction, handlePostLikeReaction } from "../reaction/post.reaction.js"


export const handlePostAction = async (event) => {

    const postElement = event.target.closest(".post-article")

    const button = event.target.closest("button")
    
    if (button) {
        const action = button.dataset.action;
    
        if (action === "like") {
            await handlePostLikeReaction(postElement);
        };

        if (action === "dislike") {
            await handlePostDislikeReaction(postElement);
        };

        if (action === "comment") {
            await handleViewComments(postElement)
        }
    }

    
}