import { getReactionList } from "../../api/reaction.api.js";

export const handleGetCommentReactionsList = async () => {
    if (localStorage.getItem("cachedCommentsState")) {
        return null;
    }
    try {
        const response = await getReactionList("comments");

        if (!response.success) {
            return null;
        }

        // postsState.likedCommentIds = response.data.liked;
        // postsState.dislikedCommentIds = response.data.diskliked;

        const cachedCommentState = {
            likedCommentIds: response.data.liked,
            dislikedCommentIds: response.data.disliked,
            commentsCount: 0
        };

        localStorage.setItem("cachedCommentsState", JSON.stringify(cachedCommentState));

    } catch {
        return null
    };
};