// js/api/client.js

import { authState, clearAuth } from "../state/auth.state.js";

const API_BASE_URL = "http://127.0.0.1:5000/api/v1";

let accessToken = null;
let refreshPromise = null;


// ==================================================
// ACCESS TOKEN
// ==================================================

export const setAccessToken = (token) => {
    authState.accessToken = token;
    // localStorage.setItem("token", token)
};

// ==================================================
// MAIN API REQUEST
// ==================================================

export const apiRequest = async (
    path,
    requestOptions = {},
    config = {}
    ) => {

    const {
        retryOn401 = true
    } = config;


    const url = `${API_BASE_URL}${path}`;


    // ----------------------------------------------
    // HEADERS
    // ----------------------------------------------

    const headers = {
        "Content-Type": "application/json",
        ...requestOptions.headers
    };


    // ----------------------------------------------
    // BEARER TOKEN
    // ----------------------------------------------

    if (authState.accessToken) {
        headers["Authorization"] =
            `Bearer ${authState.accessToken}`;
        }


    // ----------------------------------------------
    // SEND REQUEST
    // ----------------------------------------------

    const response = await fetch(url, {

        ...requestOptions,

        headers,

        credentials: "include"

    });


    // ----------------------------------------------
    // ACCESS TOKEN EXPIRED
    // ----------------------------------------------

    if (
        response.status === 401 &&
        retryOn401
    ) {

        const refreshed = await refreshAccessToken();


        if (refreshed) {
            console.log(refreshed)

            return apiRequest(
                path,
                requestOptions,
                {
                    retryOn401: false
                }
            );

        };

        // Refresh failed.
        // The session is no longer valid.

        clearAuth();

        redirectToLogin();

        throw new Error(
            "Your session has expired."
        );
    }


    // ----------------------------------------------
    // PARSE RESPONSE
    // ----------------------------------------------

    const data =
        await parseResponse(response);


    // ----------------------------------------------
    // OTHER ERRORS
    // ----------------------------------------------

    if (!response.ok) {

        const error = new Error(
            data?.message ||
            "The request failed."
        );

        error.status = response.status;

        error.data = data;

        throw error;
    }


    return data;
}


// ==================================================
// REFRESH ACCESS TOKEN
// ==================================================

const refreshAccessToken = async () => {

  if (refreshPromise){
    return refreshPromise
  };

  refreshPromise = actuallyRefreshAccessToken();

  try {
    return await refreshPromise;
  } finally {
    refreshPromise = null;
  }

};
  
  
const actuallyRefreshAccessToken = async () => {

      const response = await fetch(
          `${API_BASE_URL}/auth/refresh`,
          {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
                    },
              credentials: "include"
          }
      );


      if (!response.ok) {
          return false;
      };


      const data = await parseResponse(response);


      if (!data?.data?.access_token) {
          return false;
      };

    // authState.accessToken = data.data.access_token;
      setAccessToken(data.data.access_token);
      return true;
};


// ==================================================
// RESPONSE PARSER
// ==================================================

const parseResponse = async (response) => {

    const contentType =
        response.headers.get("content-type");


    if (
        contentType &&
        contentType.includes("application/json")
    ) {

        return await response.json();
    }

    return null;
}


// ==================================================
// REDIRECT
// ==================================================

const redirectToLogin = () => {

    window.location.href = "./login.html";
};