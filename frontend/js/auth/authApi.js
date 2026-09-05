import { apiRequest } from "../apiClient.js";


export const login = async (email, password) => {
  return apiRequest("/auth/login", {
    headers: {
            "Content-Type": "application/json",
            },
    method: "POST",
    body: JSON.stringify({ email, password }),
  },
  {
    retryOn401: false
  }
  );

};

export const register= async (email, password, confirm_password, firstname, lastname, gender) => {
  return apiRequest("/auth/register", {
    headers: {
            "Content-Type": "application/json",
            },
    method: "POST",
    body: JSON.stringify({ email, password, confirm_password, firstname, lastname, gender }),
  },
  {
    retryOn401: false
  }
  );

}

export const verifyEmail = async (otp_code, userId) => {
  return apiRequest(`/auth/users/${userId}/email`, {
    headers: {
            "Content-Type": "application/json",
            },
    method: "PATCH",
    body: JSON.stringify({ otp_code }),
  },
  {
    retryOn401: false
  }
  );

};

export const resendOtp = async (userId) => {
  return apiRequest(`/auth/otp/users/${userId}`, {
    headers: {
            "Content-Type": "application/json",
            },
    method: "POST",
  },
  {
    retryOn401: false
  }
  );

};


export const logout = async () => {
    return apiRequest(`/auth/logout`, {
    headers: {
            "Content-Type": "application/json",
            },
    method: "POST",
  },
  {
    retryOn401: false
  }
  );

}

export const resetRequest = async (email) => {
    return apiRequest(`/auth/reset/request`, {
    headers: {
            "Content-Type": "application/json",
            },
    method: "POST",
    body: JSON.stringify({ email })
  },
  {
    retryOn401: false
  }
  );

}

export const resetPassword = async (token, password, confirm_password) => {
    return apiRequest(`/auth/reset/password/${token}`, {
    headers: {
            "Content-Type": "application/json",
            },
    method: "PATCH",
    body: JSON.stringify({ password, confirm_password })
  },
  {
    retryOn401: false
  }
  );

}