import {
  createContext,
  useContext,
  useCallback,
  useMemo,
  useEffect,
  useState,
} from "react";
import { userApi } from "@/services/api/userService";
import { authApi } from "@/services/api/authService";
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchUserInfo = useCallback(async () => {
    try {
      const response = await userApi.userProfile();
      if (response.data) {
        setUser(response.data);
      }
    } catch (error) {
      console.error("Failed to fetch user info:", error);
    }
  }, []);

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const token = localStorage.getItem("freequeuesAccessToken");
        if (token) {
          await fetchUserInfo();
        }
      } catch (error) {
        console.error("Failed to check login status:", error);
      } finally {
        setIsLoading(false);
      }
    };
    checkLoginStatus();
  }, [fetchUserInfo]);

  const login = useCallback(
    async (tokens) => {
      try {
        if (tokens.access) {
          localStorage.setItem("freequeuesAccessToken", tokens.access);
          await fetchUserInfo();
        }
        if (tokens.refresh) {
          localStorage.setItem("freequeuesRefreshToken", tokens.refresh);
        }
      } catch (error) {
        console.error("Login error:", error);
      }
    },
    [fetchUserInfo],
  );

  const logout = useCallback(async () => {
    try {
      const accessToken = localStorage.getItem("freequeuesAccessToken");
      const refreshToken = localStorage.getItem("freequeuesRefreshToken");
      if (refreshToken) {
        const response = await authApi.logout({ refresh: refreshToken });
        if (response.status === 200) {
          localStorage.removeItem("freequeuesRefreshToken");
        }
      }
      if (accessToken) {
        localStorage.removeItem("freequeuesAccessToken");
      }

      setUser(null);
    } catch (error) {
      console.error("Logout error:", error);
    }
  }, []);

  const value = useMemo(
    () => ({ user, login, logout, isLoading }),
    [user, login, logout, isLoading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
