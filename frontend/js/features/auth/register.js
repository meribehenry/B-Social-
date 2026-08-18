// register.js — page-specific script for register.html

import { register } from "../../api/auth.api.js";
import { setUser} from "../../state/auth.state.js";

const errorEl = document.querySelector("#register-error");


export const handleRegister = async (event) => {
  event.preventDefault();
  errorEl.textContent = "";

  const form = event.target;
  const firstname = form.firstname.value.trim();
  const lastname = form.lastname.value.trim();
  const email = form.email.value.trim();
  const password = form.password.value;
  const confirm_password = form.confirm_password.value;
  const gender = form.gender.value;
  console.log(email, password, confirm_password, firstname, lastname, gender);

  try {
    const data = await register(email, password, confirm_password, firstname, lastname, gender);
    setUser(data.user);
    // window.location.href = "../index.html"; // dummy target — adjust to your routing
    window.location.assign("./index.html")
  } catch (err) {
    errorEl.textContent = err.message || "Registration failed. Try again.";
  }
};