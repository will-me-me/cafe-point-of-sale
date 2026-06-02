<!-- frontend/pages/register.vue -->
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
        <h1>Create Account</h1>
        <p>Join the Grounds Coffee family</p>
      </div>

      <!-- Form -->
      <v-form @submit.prevent="handleRegister" class="auth-form">
        <div class="input-group">
          <label>Full Name</label>
          <v-text-field
            v-model="form.name"
            :error-messages="errors.name"
            placeholder="John Doe"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-account-outline"
            @input="clearFieldError('name')"
          />
        </div>

        <div class="input-group">
          <label>Email Address</label>
          <v-text-field
            v-model="form.email"
            :error-messages="errors.email"
            placeholder="hello@coffee.com"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-email-outline"
            @input="clearFieldError('email')"
          />
        </div>

        <div class="input-group">
          <label>Role</label>
          <v-select
            v-model="form.role"
            :items="roleOptions"
            item-title="title"
            item-value="value"
            :error-messages="errors.role"
            placeholder="Select your role"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-badge-account"
            @update:model-value="clearFieldError('role')"
          />
        </div>

        <div class="input-group">
          <label>Password</label>
          <v-text-field
            v-model="form.password"
            :error-messages="errors.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Create a password"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-lock-outline"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showPassword = !showPassword"
            @input="clearFieldError('password')"
          />
        </div>

        <div class="input-group">
          <label>Confirm Password</label>
          <v-text-field
            v-model="form.confirmPassword"
            :error-messages="errors.confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            placeholder="Confirm your password"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-lock-check-outline"
            :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showConfirmPassword = !showConfirmPassword"
            @input="clearFieldError('confirmPassword')"
          />
        </div>

        <div class="terms">
          <v-checkbox
            v-model="agreeTerms"
            :error-messages="errors.terms"
            hide-details
            density="compact"
          >
            <template #label>
              <span class="terms-text">
                I agree to the
                <a href="#" class="terms-link">Terms of Service</a>
                and
                <a href="#" class="terms-link">Privacy Policy</a>
              </span>
            </template>
          </v-checkbox>
        </div>

        <v-btn
          type="submit"
          block
          size="large"
          class="auth-btn"
          :loading="authStore.isLoading"
          :disabled="!isFormValid"
        >
          Create Account
          <v-icon end>mdi-arrow-right</v-icon>
        </v-btn>
      </v-form>

      <!-- Footer -->
      <div class="auth-footer">
        <p>
          Already have an account?
          <NuxtLink to="/" class="login-link">Sign in</NuxtLink>
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

    <v-snackbar
      v-model="showSuccess"
      :timeout="3000"
      color="success"
      location="top"
      class="custom-toast"
    >
      <v-icon start>mdi-check-circle</v-icon>
      Account created successfully! Redirecting to login...
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from "vue";
import { useAuthStore } from "~/stores/auth";

definePageMeta({
  layout: "auth",
  middleware: "guest",
});

const authStore = useAuthStore();
const router = useRouter();
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const agreeTerms = ref(false);
const showError = ref(false);
const showSuccess = ref(false);

const form = reactive({
  name: "",
  email: "",
  role: "",
  password: "",
  confirmPassword: "",
});

const errors = reactive({
  name: "",
  email: "",
  role: "",
  password: "",
  confirmPassword: "",
  terms: "",
});

const roleOptions = [
  { title: "👑 Admin", value: "admin" },
  { title: "☕ Cashier", value: "cashier" },
];

// Validation
const validateName = (name: string) => {
  if (!name) return "Full name is required";
  if (name.length < 2) return "Name must be at least 2 characters";
  return "";
};

const validateEmail = (email: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email) return "Email is required";
  if (!emailRegex.test(email)) return "Please enter a valid email address";
  return "";
};

const validateRole = (role: string) => {
  if (!role) return "Please select a role";
  return "";
};

const validatePassword = (password: string) => {
  if (!password) return "Password is required";
  if (password.length < 6) return "Password must be at least 6 characters";
  if (!/(?=.*[A-Z])/.test(password))
    return "Password must contain at least one uppercase letter";
  if (!/(?=.*[0-9])/.test(password))
    return "Password must contain at least one number";
  return "";
};

const validateConfirmPassword = (confirmPassword: string) => {
  if (!confirmPassword) return "Please confirm your password";
  if (confirmPassword !== form.password) return "Passwords do not match";
  return "";
};

const validateTerms = () => {
  if (!agreeTerms.value) return "You must agree to the terms";
  return "";
};

const validateForm = () => {
  errors.name = validateName(form.name);
  errors.email = validateEmail(form.email);
  errors.role = validateRole(form.role);
  errors.password = validatePassword(form.password);
  errors.confirmPassword = validateConfirmPassword(form.confirmPassword);
  errors.terms = validateTerms();

  return (
    !errors.name &&
    !errors.email &&
    !errors.role &&
    !errors.password &&
    !errors.confirmPassword &&
    !errors.terms
  );
};

const isFormValid = computed(() => {
  return (
    form.name &&
    form.email &&
    form.role &&
    form.password &&
    form.confirmPassword &&
    agreeTerms.value &&
    !errors.name &&
    !errors.email &&
    !errors.role &&
    !errors.password &&
    !errors.confirmPassword
  );
});

const clearFieldError = (field: keyof typeof errors) => {
  errors[field] = "";
};

// Handle register
const handleRegister = async () => {
  if (!validateForm()) return;

  const result = await authStore.register({
    name: form.name,
    email: form.email,
    password: form.password,
    confirmPassword: form.confirmPassword,
    role: form.role as "admin" | "cashier",
  });

  if (result.success) {
    showSuccess.value = true;
    setTimeout(() => {
      navigateTo("/login");
    }, 2000);
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
/* Same styles as login page plus additional register-specific styles */
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

.auth-card {
  max-width: 520px;
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

/* Reuse all the same coffee decoration, logo, and form styles from login page */

.terms {
  margin: 8px 0;
}

.terms-text {
  font-size: 13px;
  color: #4b5563;
  font-family: "Inter", sans-serif;
}

.terms-link {
  color: #e07a5f;
  text-decoration: none;
  font-weight: 500;
}

.terms-link:hover {
  text-decoration: underline;
}

.login-link {
  color: #e07a5f;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: color 0.2s;
}

.login-link:hover {
  color: #d66b4a;
  text-decoration: underline;
}

/* Password strength indicator can be added */
</style>
