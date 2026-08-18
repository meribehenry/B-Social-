import {handleRegister} from "../features/auth/register.js";

const form = document.querySelector("#register-form");

export const initRegister = async () => {
    form.addEventListener("submit", handleRegister)
};