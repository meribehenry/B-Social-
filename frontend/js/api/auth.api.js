// auth.api.js
// "What auth endpoints exist?" — nothing about tokens/headers lives here,
// that's client.js's job.

import { apiRequest } from "./client.js";

// TODO: adjust paths + payload/response shape to match your real Flask routes

export const login = async (email, password) => {
  return apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  },
  {
    retryOn401: false
  }
  );

}

export const register= async (email, password, confirm_password, firstname, lastname, gender) => {
  return apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password, confirm_password, firstname, lastname, gender }),
  },
  {
    retryOn401: false
  }
  );

}

export function logout() {
  return apiRequest("/auth/logout", { method: "POST" });
}