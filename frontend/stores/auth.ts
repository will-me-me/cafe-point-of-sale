// frontend/stores/auth.ts
import { defineStore } from "pinia";
import { ref, computed } from "vue";

interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "cashier";
  avatar?: string;
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: "admin" | "cashier";
}

export const useAuthStore = defineStore("auth", () => {
  // State
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value);
  const isAdmin = computed(() => user.value?.role === "admin");
  const isCashier = computed(() => user.value?.role === "cashier");
  const userName = computed(() => user.value?.name || "");
  const userRole = computed(() => user.value?.role || "");

  // Actions
  const login = async (credentials: LoginCredentials) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Simulate API call - Replace with your actual backend
      const response = await $fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        body: credentials,
      });
      user.value = response.user;
      token.value = response.token;
      localStorage.setItem("auth_token", token.value);
      localStorage.setItem("user", JSON.stringify(response.user));
      return { success: true, user: response.user };
    } catch (err: any) {
      error.value = err.message || "Login failed";
      return { success: false, error: error.value };
    } finally {
      isLoading.value = false;
    }
  };

  const register = async (data: RegisterData) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Simulate API call - Replace with your actual backend
      const response = await $fetch("/auth/register", {
        method: "POST",
        body: data,
      });

      // Mock response for demo
      const newUser = {
        id: Date.now().toString(),
        name: data.name,
        email: data.email,
        role: data.role,
      };

      user.value = newUser;
      token.value = "mock-token-" + Date.now();
      localStorage.setItem("auth_token", token.value);
      localStorage.setItem("user", JSON.stringify(newUser));

      return { success: true, user: newUser };
    } catch (err: any) {
      error.value = err.message || "Registration failed";
      return { success: false, error: error.value };
    } finally {
      isLoading.value = false;
    }
  };

  const logout = async () => {
    isLoading.value = true;

    try {
      // Clear local storage
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user");

      // Clear state
      user.value = null;
      token.value = null;
      error.value = null;

      // Navigate to login
      await navigateTo("/login");
    } catch (err: any) {
      error.value = err.message || "Logout failed";
    } finally {
      isLoading.value = false;
    }
  };

  const checkAuth = () => {
    if (!import.meta.client) return false;
    const storedToken = localStorage.getItem("auth_token");
    const storedUser = localStorage.getItem("user");

    if (storedToken && storedUser) {
      token.value = storedToken;
      user.value = JSON.parse(storedUser);
      return true;
    }
    return false;
  };

  const fetchUser = async () => {
    if (!token.value) return null;

    try {
      const response = await $fetch("/auth/me", {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });
      user.value = response;
      return response;
    } catch (err) {
      logout();
      return null;
    }
  };

  return {
    // State
    user,
    token,
    isLoading,
    error,

    // Getters
    isAuthenticated,
    isAdmin,
    isCashier,
    userName,
    userRole,

    // Actions
    login,
    register,
    logout,
    checkAuth,
    fetchUser,
  };
});
