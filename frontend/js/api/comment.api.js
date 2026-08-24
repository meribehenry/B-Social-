import { apiRequest } from "./client.js";


export const getComments = async (postId) => {
    return apiRequest(`/posts/${postId}/comments`)
}

export const getComment = async (commentId) => {
    return apiRequest(`/comments/${commentId}`)
}

export const deleteComment = async (commentId) => {
    return apiRequest(`/comments/${commentId}`, {method: "DELETE"})
}

export const createComment = async (content) => {
    return apiRequest("/comments",
        {
            method: "POST",
            body: JSON.stringify(content)
        }
    )
}

export const editComment = async (commentId, content) => {
    return apiRequest(`/comments/${commentId}`,
        {
            method: "PATCH",
            body: JSON.stringify(content)
        }
    )
}