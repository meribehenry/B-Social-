import { apiRequest } from "../../apiClient.js";


export const react = async (resource, resourceId, reactionType) => {
    return apiRequest(`/${resource}/${resourceId}/reactions`, {
        headers: {
            "Content-Type": "application/json",
            },
        method: "POST",
        body: JSON.stringify({"reaction_type": reactionType})
    });

};


export const deleteReaction = async (resource, resourceId)  => {
        return apiRequest(`/${resource}/${resourceId}/reactions`, {
        headers: {
            "Content-Type": "application/json",
            },
        method: "DELETE",
    });
};


export const getReactionList = async (resource)  => {
        return apiRequest(`/${resource}/reactions`, 
            {
                headers: {
                    "Content-Type": "application/json",
                }
            }
        );
};