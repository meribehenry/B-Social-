import { apiRequest } from "../../apiClient.js";


export const getUserSearchResult = async (word) => {
    return apiRequest(`/search/?search=${word}`, 
        {
            headers: {
            "Content-Type": "application/json"
        }
        }
    );
};