import { apiRequest } from "../../apiClient.js";


export const getNotifications= async () => {
    return apiRequest("/notifications/", 
        {
            headers: {
            "Content-Type": "application/json"
            }
        }
    )
}

export const deleteNotification = async (notificationId) => {
    return apiRequest(`/notifications/${notificationId}`, 
    {
        headers: {
            "Content-Type": "application/json",
        },    
        method: "DELETE"
    })
}

export const deleteNotifications = async () => {
    return apiRequest("/notifications/", 
    {   
        headers: {
            "Content-Type": "application/json",
            },
        method: "DELETE"
    })
}