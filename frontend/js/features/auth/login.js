// login.js — page-specific script for login.html

import { login } from "../../api/auth.api.js";
import { setAuthenticated } from "../../state/auth.state.js";

const errorEl = document.querySelector("#login-error");



export const handleLogin = async (event) => {
  event.preventDefault();
  errorEl.textContent = "";
  
  const form = event.target;
  const email = form.email.value.trim();
  const password = form.password.value.trim();

  try {
    const data = await login(email, password);
    setAuthenticated(data.user, data.access_token);
    console.log("Done")
    errorEl.textContent = data.message || "Login succeeded.";
    window.location.assign("./index.html"); 
  } catch (err) {
    errorEl.textContent = err.message || "Login failed. Try again.";
    // console.log(err.message)
  }
};