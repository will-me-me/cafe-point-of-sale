// frontend/middleware/guest.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  // Redirect to dashboard if already logged in
  if (authStore.checkAuth()) {
    if (authStore.isAdmin) {
      return navigateTo("/pos");
    } else {
      return navigateTo("/pos");
    }
  }
});
