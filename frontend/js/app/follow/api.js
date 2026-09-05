import { apiRequest } from "../../apiClient.js";


export const follow = async (followedUserID) => {
    return apiRequest(`/users/${followedUserID}/follow`, {
        headers: {
            "Content-Type": "application/json",
            },
        method: "POST",
    });
};

export const unfollow = async (followedUserID) => {
    return apiRequest(`/users/${followedUserID}/follow`, {
        headers: {
            "Content-Type": "application/json",
            },
        method: "DELETE",
    });
};


export const getFollowingList = async (followedUserID)  => {
        return apiRequest(`/users/${followedUserID}/following/list`,
            {
            headers: {
            "Content-Type": "application/json"
            }
        }
        );
};