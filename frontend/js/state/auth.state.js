// auth.state.js
// The frontend's current belief about who is logged in.
// accessToken lives in memory only — never localStorage, never a normal cookie.
// The refresh token is a separate HttpOnly cookie the browser manages; JS never touches it.


export const authState = {
    user: null,
    accessToken: null,
    isAuthenticated: false,
    initialised: false
};


export const setUser = (user) =>  {
    authState.user =  user || {};
};

export const setAuthenticated = (user, accessToken) =>  {
    authState.user =  user;
    authState.accessToken =  accessToken;
    authState.isAuthenticated = true
};

export const clearAuth = () =>  {
    authState.user =  null;
    authState.accessToken =  null;
    authState.isAuthenticated = false;
};