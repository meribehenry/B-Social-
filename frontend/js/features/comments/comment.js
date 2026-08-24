import { getComments, getComment, createComment, deleteComment, editComment } from "../../api/comment.api.js";


export const handleGetComments = async (postId) => {
    try {

        const response = await getComments(postId);
        if (!response.success) {
            throw (response);
        };
        console.log(response.data.comments)
        return response.data.comments;
        
    } catch (error) {
        throw (error) ;     
    }
};

export const handleGetComment = async (commentId) => {
    try {
        const response = await getComment();
        if (!response.success) {
        throw new Error(response.message);
        };
        return response.data;
    } catch (error) {
        throw (error);
    }
};


export const handleDeleteComment =  async (commentId) => {
    let response = deleteComment(postId);

    if (!response.success) {
        throw (response);
    }

    response = response;
    return response;

};

export const handleCreateComment= async (event) => {
    event.preventDefault();
    content = event.target.content.value.trim();

    let response = createComment(content);

    if (!response.success) {
        throw (response);
    };

    return response;

};