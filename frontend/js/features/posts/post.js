import { createPost, deletePost, getPost, getPosts } from "../../api/post.api.js"


export const handleGetPost = async (postId) => {
    try {

        const response = await getPost(postId);
        if (!response.success) {
            throw (response);
        };
        return response.data;
    } catch (error) {
        throw (error) ;     
    }
};

export const handleGetPosts = async () => {
    try {
        const response = await getPosts();
        if (!response.success) {
        throw new Error(response.message);
        };
        return response.data;
    } catch (error) {
        throw (error);
    }
};


export const handleDeletePost =  async (postId) => {
    let response = deletePost(postId);

    if (!response.ok) {
        throw (response);
    }

    response = response;
    return response;

};

export const handleCreatePost = async (event) => {
    event.preventDefault();
    content = event.target.content.value.trim();
    files = event.target.files.value;

    let response = createPost(content, files);

    if (!response.success) {
        throw (response);
    };

    return response;

};