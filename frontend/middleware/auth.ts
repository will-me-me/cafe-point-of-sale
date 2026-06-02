// frontend/middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  // Check if user is authenticated
  if (!authStore.checkAuth()) {
    // Redirect to login if not authenticated
    return navigateTo("/");
  }

  // Role-based access control
  const requiredRole = to.meta.role as "admin" | "cashier" | undefined;

  if (requiredRole) {
    if (requiredRole === "admin" && !authStore.isAdmin) {
      // Redirect cashiers to POS if they try to access admin routes
      return navigateTo("/pos");
    }
    if (requiredRole === "cashier" && !authStore.isCashier) {
      // Redirect admins to dashboard if they try to access cashier routes
      return navigateTo("/pos");
    }
  }
});
