import { apiRequest } from "./client.js";


export const getNotifications= async () => {
    return apiRequest("/notifications/")
}

export const deleteNotification = async (notificationId) => {
    return apiRequest(`/notifications/${notificationId}`, {method: "DELETE"})
}

export const deleteNotifications = async () => {
    return apiRequest("/notifications/", {method: "DELETE"})
}