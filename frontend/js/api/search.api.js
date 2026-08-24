import { apiRequest } from "./client.js";


export const getUserSearchResult = async (word, parameters={userId: ""}) => {
    return apiRequest(`/search/?search=${word}&user_public_id=${parameters.userId}`);
};