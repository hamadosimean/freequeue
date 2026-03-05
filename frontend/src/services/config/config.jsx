import { API_URL } from "../../config/environment";
import axios from "axios";

export const Config = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for API calls
Config.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem("freequeuesAccessToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response interceptor for API calls
Config.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("freequeuesRefreshToken");

      if (refreshToken) {
        try {
          // Use a separate axios instance to refresh to avoid interceptor loop
          const response = await axios.post(`${API_URL}auth/jwt/refresh/`, {
            refresh: refreshToken,
          });

          if (response.status === 200) {
            const { access } = response.data;
            localStorage.setItem("freequeuesAccessToken", access);

            // Update header and retry original request
            Config.defaults.headers.common.Authorization = `Bearer ${access}`;
            originalRequest.headers.Authorization = `Bearer ${access}`;
            return Config(originalRequest);
          }
        } catch (refreshError) {
          console.error("Refresh token failed:", refreshError);
          // Only clear and redirect if the refresh itself failed
          localStorage.removeItem("freequeuesAccessToken");
          localStorage.removeItem("freequeuesRefreshToken");
          window.location.href = "/auth/login";
        }
      } else {
        // No refresh token available
        window.location.href = "/auth/login";
      }
    }
    return Promise.reject(error);
  },
);
