<!-- frontend/pages/login.vue -->
<template>
  <div class="auth-container">
    <div class="auth-card">
      <!-- Coffee Decorative Elements -->
      <div class="coffee-decoration">
        <div class="coffee-bean bean-1">🫘</div>
        <div class="coffee-bean bean-2">☕</div>
        <div class="coffee-bean bean-3">🫘</div>
      </div>

      <!-- Logo Section -->
      <div class="logo-section">
        <div class="logo-icon">🌱</div>
        <div class="logo-text">GROUNDS</div>
        <div class="logo-badge">COFFEE</div>
      </div>

      <!-- Title -->
      <div class="auth-title">
        <h1>Welcome Back</h1>
        <p>Sign in to continue to your dashboard</p>
      </div>

      <!-- Form -->
      <v-form @submit.prevent="handleLogin" class="auth-form">
        <div class="input-group">
          <label>Email Address</label>
          <v-text-field
            v-model="form.email"
            :error-messages="errors.email"
            placeholder="admin@coffee.com"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-email-outline"
            @input="clearFieldError('email')"
          />
        </div>

        <div class="input-group">
          <label>Password</label>
          <v-text-field
            v-model="form.password"
            :error-messages="errors.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Enter your password"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-lock-outline"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showPassword = !showPassword"
            @input="clearFieldError('password')"
          />
        </div>

        <div class="form-options">
          <v-checkbox
            v-model="rememberMe"
            label="Remember me"
            hide-details
            density="compact"
          />
          <a href="#" class="forgot-link">Forgot password?</a>
        </div>

        <v-btn
          type="submit"
          block
          size="large"
          class="auth-btn"
          :loading="authStore.isLoading"
          :disabled="!isFormValid"
        >
          Sign In
          <v-icon end>mdi-arrow-right</v-icon>
        </v-btn>

        <div class="demo-credentials">
          <p class="demo-title">Demo Credentials</p>
          <div class="demo-cards">
            <div class="demo-card" @click="fillAdminCredentials">
              <div class="demo-role admin">Admin</div>
              <div class="demo-details">
                <span>admin@coffee.com</span>
                <span>•••••••••</span>
              </div>
            </div>
            <div class="demo-card" @click="fillCashierCredentials">
              <div class="demo-role cashier">Cashier</div>
              <div class="demo-details">
                <span>cashier@coffee.com</span>
                <span>•••••••••</span>
              </div>
            </div>
          </div>
        </div>
      </v-form>

      <!-- Footer -->
      <div class="auth-footer">
        <p>
          Don't have an account?
          <NuxtLink to="/register" class="register-link"
            >Create account</NuxtLink
          >
        </p>
      </div>
    </div>

    <!-- Toast Notifications -->
    <v-snackbar
      v-model="showError"
      :timeout="3000"
      color="error"
      location="top"
      class="custom-toast"
    >
      <v-icon start>mdi-alert-circle</v-icon>
      {{ authStore.error }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, watch } from "vue";
import { useAuthStore } from "~/stores/auth";

definePageMeta({
  layout: "auth",
  middleware: "guest",
});

const authStore = useAuthStore();
const router = useRouter();
const showPassword = ref(false);
const rememberMe = ref(false);
const showError = ref(false);

const form = reactive({
  email: "",
  password: "",
});

const errors = reactive({
  email: "",
  password: "",
});

// Validation
const validateEmail = (email: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email) return "Email is required";
  if (!emailRegex.test(email)) return "Please enter a valid email address";
  return "";
};

const validatePassword = (password: string) => {
  if (!password) return "Password is required";
  if (password.length < 6) return "Password must be at least 6 characters";
  return "";
};

const validateForm = () => {
  errors.email = validateEmail(form.email);
  errors.password = validatePassword(form.password);
  return !errors.email && !errors.password;
};

const isFormValid = computed(() => {
  return form.email && form.password && !errors.email && !errors.password;
});

const clearFieldError = (field: keyof typeof errors) => {
  errors[field] = "";
};

// Fill demo credentials
const fillAdminCredentials = () => {
  form.email = "admin@coffee.com";
  form.password = "password123";
  validateForm();
};

const fillCashierCredentials = () => {
  form.email = "cashier@coffee.com";
  form.password = "password123";
  validateForm();
};

// Handle login
const handleLogin = async () => {
  if (!validateForm()) return;

  const result = await authStore.login({
    email: form.email,
    password: form.password,
  });

  if (result.success) {
    // Redirect based on role
    if (authStore.isAdmin) {
      await navigateTo("/admin/dashboard");
    } else {
      await navigateTo("/pos");
    }
  } else {
    showError.value = true;
  }
};

// Check if already logged in
onMounted(() => {
  if (authStore.checkAuth()) {
    if (authStore.isAdmin) {
      navigateTo("/admin/dashboard");
    } else {
      navigateTo("/pos");
    }
  }
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap");

.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #1b4332 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

.auth-container::before {
  content: "";
  position: absolute;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.05) 1px,
    transparent 1px
  );
  background-size: 40px 40px;
  animation: shift 20s linear infinite;
}

@keyframes shift {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(40px, 40px);
  }
}

.auth-card {
  max-width: 480px;
  width: 100%;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border-radius: 40px;
  padding: 48px 40px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  position: relative;
  z-index: 1;
  transition: transform 0.3s ease;
}

.auth-card:hover {
  transform: translateY(-5px);
}

/* Coffee Decoration */
.coffee-decoration {
  position: absolute;
  top: 20px;
  right: 20px;
  left: 20px;
  pointer-events: none;
}

.coffee-bean {
  position: absolute;
  font-size: 24px;
  opacity: 0.15;
  animation: float 3s ease-in-out infinite;
}

.bean-1 {
  top: -10px;
  right: 0;
  animation-delay: 0s;
}
.bean-2 {
  bottom: -10px;
  left: 0;
  animation-delay: 1s;
}
.bean-3 {
  top: 50%;
  right: -20px;
  animation-delay: 2s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Logo Section */
.logo-section {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 8px;
  margin-bottom: 32px;
  position: relative;
}

.logo-icon {
  font-size: 36px;
  animation: rotate 4s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.logo-text {
  font-family: "Playfair Display", serif;
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.logo-badge {
  background: linear-gradient(135deg, #e07a5f, #d66b4a);
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  color: white;
  letter-spacing: 1px;
}

/* Auth Title */
.auth-title {
  text-align: center;
  margin-bottom: 32px;
}

.auth-title h1 {
  font-family: "Playfair Display", serif;
  font-size: 32px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 8px;
}

.auth-title p {
  font-family: "Inter", sans-serif;
  font-size: 14px;
  color: #6b7280;
}

/* Form Styles */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group label {
  font-family: "Inter", sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
  display: block;
  letter-spacing: 0.3px;
}

:deep(.v-field) {
  border-radius: 16px !important;
  transition: all 0.3s ease;
}

:deep(.v-field:hover) {
  box-shadow: 0 4px 12px rgba(27, 67, 50, 0.1);
}

:deep(.v-field--focused) {
  border-color: #2d6a4f !important;
  box-shadow: 0 0 0 3px rgba(45, 106, 79, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 4px 0;
}

:deep(.v-checkbox) {
  font-size: 13px;
}

.forgot-link {
  font-size: 13px;
  color: #e07a5f;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: #d66b4a;
  text-decoration: underline;
}

.auth-btn {
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%) !important;
  color: white !important;
  font-family: "Inter", sans-serif;
  font-weight: 700;
  font-size: 16px;
  text-transform: none;
  border-radius: 40px !important;
  padding: 12px !important;
  margin-top: 8px;
  transition: all 0.3s ease;
}

.auth-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(27, 67, 50, 0.3);
}

/* Demo Credentials */
.demo-credentials {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.demo-title {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
  text-align: center;
}

.demo-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.demo-card {
  background: #f9fafb;
  border-radius: 16px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
}

.demo-card:hover {
  background: #f3f4f6;
  transform: translateY(-2px);
  border-color: #2d6a4f;
}

.demo-role {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 8px;
  display: inline-block;
  margin-bottom: 8px;
}

.demo-role.admin {
  background: #e07a5f20;
  color: #e07a5f;
}

.demo-role.cashier {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.demo-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.demo-details span {
  font-size: 11px;
  color: #6b7280;
  font-family: monospace;
}

/* Footer */
.auth-footer {
  margin-top: 32px;
  text-align: center;
}

.auth-footer p {
  font-family: "Inter", sans-serif;
  font-size: 14px;
  color: #6b7280;
}

.register-link {
  color: #e07a5f;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: color 0.2s;
}

.register-link:hover {
  color: #d66b4a;
  text-decoration: underline;
}

/* Toast */
.custom-toast :deep(.v-snackbar__content) {
  font-family: "Inter", sans-serif;
  font-weight: 500;
  border-radius: 12px;
}

/* Responsive */
@media (max-width: 640px) {
  .auth-card {
    padding: 32px 24px;
  }

  .auth-title h1 {
    font-size: 28px;
  }

  .demo-cards {
    grid-template-columns: 1fr;
  }
}
</style>
