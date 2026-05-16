import { useState, useEffect, useCallback } from "react";
import { apiClient } from "../lib/api";

interface User {
  id: string;
  wallet_address: string;
  name?: string;
  role: "admin" | "user";
}

interface UseAuthReturn {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  login: (walletAddress: string, signature: string, message: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

/**
 * Hook para gerenciar autenticação com Arc wallet
 */
export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check if user is already logged in (from localStorage)
  useEffect(() => {
    const storedToken = localStorage.getItem("orvion_token");
    const storedUser = localStorage.getItem("orvion_user");

    if (storedToken && storedUser) {
      try {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
        apiClient.setToken(storedToken);
      } catch (err) {
        localStorage.removeItem("orvion_token");
        localStorage.removeItem("orvion_user");
      }
    }
  }, []);

  const login = useCallback(
    async (walletAddress: string, signature: string, message: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await apiClient.walletLogin(
          walletAddress,
          signature,
          message
        );

        const newToken = response.token;
        const userData: User = {
          id: response.user?.id || walletAddress,
          wallet_address: walletAddress,
          name: response.user?.name,
          role: response.user?.role || "user",
        };

        setToken(newToken);
        setUser(userData);
        apiClient.setToken(newToken);

        // Persist to localStorage
        localStorage.setItem("orvion_token", newToken);
        localStorage.setItem("orvion_user", JSON.stringify(userData));
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "Login failed";
        setError(errorMessage);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const logout = useCallback(() => {
    setUser(null);
    setToken(null);
    setError(null);
    apiClient.clearToken();
    localStorage.removeItem("orvion_token");
    localStorage.removeItem("orvion_user");
  }, []);

  return {
    user,
    token,
    isLoading,
    error,
    login,
    logout,
    isAuthenticated: !!token && !!user,
  };
}
