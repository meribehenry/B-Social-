import { apiRequest } from "../../apiClient.js";


export const getPosts = async (parameters={}) => {
    return apiRequest(`/posts/?user_public_id=${parameters?.userId}&sort=${parameters?.sortBy}`,
        {
            headers: {
            "Content-Type": "application/json"
        }
        }
    )
}

export const getPost = async (postId) => {
    return apiRequest(`/posts/${postId}`,
        {
            headers: {
            "Content-Type": "application/json"
        }
        }
    )
}

export const deletePost = async (postId) => {
    return apiRequest(`/posts/${postId}`, 
        {   headers: {
            "Content-Type": "application/json",
            },
            method: "DELETE"})
}

export const createPost = async (formData) => {
    // Remove empty file fields
    for (let [key, value] of formData.entries()) {
    if (value instanceof File && value.size === 0) {
        formData.delete(key)
    }
    }
    return apiRequest("/posts",
        {
            method: "POST",
            body: formData
        }
    )
}

export const editPost = async (formData, postId) => {
    // Remove empty file fields
    for (let [key, value] of formData.entries()) {
    if (value instanceof File && value.size === 0) {
        formData.delete(key)
    }
    }
    return apiRequest(`/posts/${postId}`,
        {
            method: "PATCH",
            body: formData
        }
    )
}