import { apiRequest } from "./client.js";


export const getPosts = async () => {
    return apiRequest("/posts/")
}

export const getPost = async (postId) => {
    return apiRequest(`/posts/${postId}`)
}

export const deletePost = async (postId) => {
    return apiRequest(`/posts/${postId}`, {method: "DELETE"})
}

export const createPost = async (content, files) => {
    return apiRequest("/posts",
        {
            method: "POST",
            body: content
        }
    )
}

export const editPost = async (postId, content, file) => {
    return apiRequest(`/posts/${postId}`,
        {
            method: "PATCH",
            body: content
        }
    )
}