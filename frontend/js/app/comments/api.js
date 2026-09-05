import { apiRequest } from "../../apiClient.js";


export const getComments = async (postId) => {
    return apiRequest(`/posts/${postId}/comments`, 
        {
            headers: {
            "Content-Type": "application/json"
        }
        }
    )
}

export const getComment = async (commentId) => {
    return apiRequest(`/comments/${commentId}`, 
        {
            headers: {
            "Content-Type": "application/json"
        }
        }
    )
}

export const deleteComment = async (commentId) => {
    return apiRequest(`/comments/${commentId}`, 
        { 
            headers: {
            "Content-Type": "application/json",
            },
            method: "DELETE"
        })
}

export const createComment = async (postId, content) => {
    return apiRequest(`/posts/${postId}/comments`,
        {   
            headers: {
            "Content-Type": "application/json",
            },
            method: "POST",
            body: JSON.stringify({content: content})
        }
    )
}

export const editComment = async (commentId, content) => {
    return apiRequest(`/comments/${commentId}`,
        {   
            headers: {
            "Content-Type": "application/json",
            },
            method: "PATCH",
            body: JSON.stringify({content: content})
        }
    )
}