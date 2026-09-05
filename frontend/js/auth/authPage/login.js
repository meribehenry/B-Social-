import { login } from "../authApi.js";
import { setAuthenticated } from "../authState.js";

const authApp = document.querySelector("#auth-app")

export const renderLoginPage = () => {
    const title = document.querySelector("#title")
    const body= document.querySelector("body")

    title.textContent = "Login"
    body.dataset.page = "login";

    const html = `
    <form id="login-form" action="" method="POST">
        <p id="login-error"></p>

        <label for="email">Email</label>
        <input id="email" type="email" name="email">

        <label for="password">Password</label>
        <input id="password" type="password" name="password">

        <button type="submit" data-action="login">Login</button>

    </form>
    `
    authApp.innerHTML = "";
    authApp.innerHTML = html;

    loginEventListener()

};


export  const handleLogin = async (event) => {
  event.preventDefault();
  
  const form = event.target;
  const email = form.email.value.trim();
  const password = form.password.value.trim();

  try {
    const response = await login(email, password);

    if (!response.success) {
        console.log(response.message)
    }
    
    setAuthenticated(response.data.user, response.data.access_token);
    window.location.assign("/app"); 
  } catch (error) {
    console.log(error.message)

  }
};


export const loginEventListener = async  () => {
    const form = document.querySelector("#login-form");
    form.addEventListener("submit", handleLogin);
};