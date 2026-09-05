import { apiRequest } from "../../apiClient.js";


export const getProfile = async (userId) => {
    return apiRequest(`/users/${userId}/profile`, 
        {
            headers: {
            "Content-Type": "application/json"
        }
        }
    );
};


export const editProfile = async (userId, body) => {
    return apiRequest(`/users/${userId}/profile`), 
    {   
        headers: {
            "Content-Type": "application/json",
            },
        method: "PATCH",
        body: body
    };
};
