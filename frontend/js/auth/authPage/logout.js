import { logout } from "../authApi.js"
import { clearAuth } from "../authState.js"

export const handleLogout = async(event) => {
    event.preventDefault()

    try {
        const response = logout()

        if (!response.success) {
            console.log(response.message)
        }

    } catch {
        console.log(response.message)
    }

    clearAuth()
    window.location.href = "/"
}

export const logoutEventListener = () => {
    const body = document.querySelector("body");
    body.addEventListener("click", handleLogout);
}

logoutEventListener()