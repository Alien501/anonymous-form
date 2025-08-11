import axios from "axios";

export const API_URL = import.meta.env.VITE_BASE_URL;

// CSRF token management
let csrfToken: string | null = null;

export const getCSRFToken = async (): Promise<string | null> => {
  try {
    if (csrfToken) {
      console.log("Using cached CSRF token");
      return csrfToken;
    }

    console.log("Fetching CSRF token from server...");
    const response = await axios.get(`${API_URL}/csrf-token/`, {
      withCredentials: true,
    });

    csrfToken = response.data.csrf_token;
    console.log("CSRF token fetched successfully");
    return csrfToken;
  } catch (error) {
    console.error("Failed to fetch CSRF token:", error);
    return null;
  }
};

export const clearCSRFToken = () => {
  console.log("Clearing CSRF token");
  csrfToken = null;
};

export const setCSRFToken = (token: string) => {
  console.log("Setting CSRF token");
  csrfToken = token;
};

export const getStoredCSRFToken = (): string | null => {
  return csrfToken;
};

function getCookie(name: string) {
  let cookieValue: string | null = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

// Add CSRF token to requests
api.interceptors.request.use(async (config) => {
  // Try to get CSRF token from cookie first
  let token = getCookie("csrftoken");

  // If no token in cookie, fetch it from the server
  if (!token) {
    console.log("No CSRF token in cookie, fetching from server...");
    token = await getCSRFToken();
  } else {
    console.log("Using CSRF token from cookie");
  }

  if (token && config.method !== "get") {
    config.headers["X-CSRFToken"] = token;
    console.log("CSRF token added to request headers");
  }

  config.withCredentials = true;
  return config;
});

api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (error.response && error.response.status === 403) {
      // CSRF token might be invalid, try to refresh it
      console.log("CSRF token might be invalid, refreshing...");
      clearCSRFToken();
      const newToken = await getCSRFToken();
      if (newToken) {
        // Retry the original request with new token
        const originalRequest = error.config;
        originalRequest.headers["X-CSRFToken"] = newToken;
        console.log("Retrying request with new CSRF token");
        return api(originalRequest);
      }
    }

    if (error.response && error.response.status === 401) {
      console.log("Authentication error");
    }

    return Promise.reject(error);
  },
);

export default api;
