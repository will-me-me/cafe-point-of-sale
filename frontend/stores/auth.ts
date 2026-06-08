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
interface UsersinDb {
  id: string;
  name: string;
  email: string;
  status?: "active" | "inactive";
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

interface ActivityLog {
  id?: string;
  user_id: string;
  user_name: string;
  user_email?: string;
  action: string;
  message: string;
  created_at: string;
}

export const useAuthStore = defineStore("auth", () => {
  // State
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const activityLogs = ref<ActivityLog[]>([]);
  const AllDbUsers = ref<UsersinDb[]>([]);

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
      const { user: loggedInUser, access_token: authToken } = response;
      user.value = loggedInUser;

      token.value = authToken;
      localStorage.setItem("auth_token", authToken);
      localStorage.setItem("user", JSON.stringify(loggedInUser));
      console.log("token after login:", token.value);
      console.log(
        "localStorage token after login:",
        localStorage.getItem("auth_token")
      );
      return { success: true, user: loggedInUser };
    } catch (err: any) {
      error.value = err.message || "Login failed";
      return { success: false, error: error.value };
    } finally {
      isLoading.value = false;
    }
  };

  const getAllUsers = async () => {
    if (!token.value) return [];
    try {
      const response = await $fetch("http://127.0.0.1:8000/auth/users", {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });
      AllDbUsers.value = response;
      console.log("Fetched users:", response);
      console.log("alldbusers.value:", AllDbUsers.value);
      return response;
    } catch (err) {
      error.value = err.message || "Failed to fetch users";
      return [];
    }
  };

  const deleteUser = async (userId: string) => {
    if (!token.value) return { success: false, error: "Not authenticated" };
    try {
      const response = await $fetch(
        `http://127.0.0.1:8000/auth/users/${userId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        }
      );
      // Remove the deleted user from the local state
      AllDbUsers.value = AllDbUsers.value.filter((user) => user.id !== userId);
      console.log("Deleted user:", response);
      return { success: true };
    } catch (err) {
      error.value = err.message || "Failed to delete user";
      return { success: false, error: error.value };
    }
  };

  const UserStatus = async (userId: string, status: "active" | "inactive") => {
    if (!token.value) return { success: false, error: "Not authenticated" };
    try {
      const response = await $fetch(
        `http://127.0.0.1:8000/auth/users/${userId}/status?status=${status}`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        }
      );
      // Update the user's status in the local state
      const userIndex = AllDbUsers.value.findIndex(
        (user) => user.id === userId
      );
      if (userIndex !== -1) {
        AllDbUsers.value[userIndex].status = status;
      }
      console.log("Updated user status:", response);
      return { success: true };
    } catch (err) {
      error.value = err.message || "Failed to update user status";
      return { success: false, error: error.value };
    }
  };

  const getActivityLogs = async () => {
    console.log("Fetching activity logs with token:", token.value);
    if (!token.value) return [];

    try {
      const response = await $fetch(
        "http://127.0.0.1:8000/auth/activity-logs",
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        }
      );
      activityLogs.value = response;
      console.log("Fetched activity logs:", response);
      return response;
    } catch (err) {
      error.value = err.message || "Failed to fetch activity logs";
      return [];
    }
  };

  const register = async (data: RegisterData) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Simulate API call - Replace with your actual backend
      const response = await $fetch("http://127.0.0.1:8000/auth/register", {
        method: "POST",
        body: data,
      });

      // don't mock response, use actual response from backend
      const { user: registeredUser, access_token: authToken } = response;
      user.value = registeredUser;

      token.value = authToken;
      localStorage.setItem("auth_token", authToken);
      localStorage.setItem("user", JSON.stringify(registeredUser));
      return { success: true, user: registeredUser };
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
      await navigateTo("/");
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
    activityLogs,
    AllDbUsers,

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
    getActivityLogs,
    getAllUsers,
    deleteUser,
    UserStatus,
  };
});
