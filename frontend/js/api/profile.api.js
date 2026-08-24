import { apiRequest } from "./client.js";


export const getProfile = async (userId) => {
    return apiRequest(`/users/${userId}/profile`);
};


export const editProfile = async (userId, body) => {
    return apiRequest(`/users/${userId}/profile`), 
    {
        method: "PATCH",
        body: body
    };
};


