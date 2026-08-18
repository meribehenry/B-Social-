import { handleLogin } from "../features/auth/login.js";

const form = document.querySelector("#login-form");

export const initLogin = async  () => {
  form.addEventListener("submit", handleLogin);
};
