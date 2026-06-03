<!-- frontend/pages/register.vue -->
<template>
  <div class="auth-container">
    <!-- Animated Background -->
    <div class="animated-bg">
      <div class="coffee-particles"></div>
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <div class="auth-card">
      <!-- Floating Coffee Beans Decoration -->
      <div class="floating-beans">
        <div class="floating-bean bean-1">🫘</div>
        <div class="floating-bean bean-2">☕</div>
        <div class="floating-bean bean-3">🫘</div>
        <div class="floating-bean bean-4">✨</div>
      </div>

      <!-- Premium Logo Section -->
      <div class="logo-section">
        <div class="logo-ring">
          <div class="logo-icon">🌱</div>
        </div>
        <div class="logo-text-wrapper">
          <div class="logo-text">GROUNDS</div>
          <div class="logo-badge">PREMIUM COFFEE</div>
        </div>
      </div>

      <!-- Welcome Section -->
      <div class="welcome-section">
        <h1 class="welcome-title">
          <span class="gradient-text">Create Account</span>
        </h1>
        <p class="welcome-subtitle">
          Join the Grounds Coffee family and start your journey
        </p>
      </div>

      <!-- Social Sign Up Options -->
      <!-- <div class="social-options">
        <button class="social-btn google">
          <svg width="20" height="20" viewBox="0 0 24 24">
            <path
              fill="currentColor"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="currentColor"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="currentColor"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="currentColor"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Sign up with Google
        </button>
        <button class="social-btn apple">
          <svg width="20" height="20" viewBox="0 0 24 24">
            <path
              fill="currentColor"
              d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17.36 3 13.5 4.7 10.45c.85-1.52 2.36-2.48 4-2.5 1.26-.01 2.44.85 3.21.85.77 0 2.21-1.05 3.73-.89.63.03 2.41.25 3.55 1.93-.09.06-2.12 1.23-2.1 3.68.03 2.92 2.56 3.89 2.59 3.91-.02.05-.4 1.37-1.32 2.72zM15 4.5c.66-.8 1.1-1.91.98-3-.94.04-2.07.63-2.74 1.42-.6.7-1.13 1.82-.99 2.89 1.05.08 2.12-.53 2.75-1.31z"
            />
          </svg>
          Sign up with Apple
        </button>
      </div> -->

      <div class="divider">
        <span class="divider-line"></span>
        <span class="divider-text">sign up with email</span>
        <span class="divider-line"></span>
      </div>

      <!-- Form -->
      <v-form @submit.prevent="handleRegister" class="auth-form">
        <div class="input-group">
          <label class="input-label">
            <v-icon class="label-icon" size="18">mdi-account-outline</v-icon>
            Full Name
          </label>
          <v-text-field
            v-model="form.name"
            :error-messages="errors.name"
            placeholder="John Doe"
            variant="outlined"
            density="comfortable"
            class="custom-input"
            @input="clearFieldError('name')"
          >
            <template v-slot:append-inner v-if="form.name && !errors.name">
              <v-icon color="#2D6A4F" size="18">mdi-check-circle</v-icon>
            </template>
          </v-text-field>
        </div>

        <div class="input-group">
          <label class="input-label">
            <v-icon class="label-icon" size="18">mdi-email-outline</v-icon>
            Email Address
          </label>
          <v-text-field
            v-model="form.email"
            :error-messages="errors.email"
            placeholder="hello@coffee.com"
            variant="outlined"
            density="comfortable"
            class="custom-input"
            @input="clearFieldError('email')"
          >
            <template v-slot:append-inner v-if="form.email && !errors.email">
              <v-icon color="#2D6A4F" size="18">mdi-check-circle</v-icon>
            </template>
          </v-text-field>
        </div>

        <div class="input-group">
          <label class="input-label">
            <v-icon class="label-icon" size="18">mdi-badge-account</v-icon>
            Role
          </label>
          <v-select
            v-model="form.role"
            :items="roleOptions"
            item-title="title"
            item-value="value"
            :error-messages="errors.role"
            placeholder="Select your role"
            variant="outlined"
            density="comfortable"
            class="custom-select"
            @update:model-value="clearFieldError('role')"
          >
            <template #item="{ props, item }">
              <v-list-item v-bind="props">
                <template #prepend>
                  <span class="role-icon">{{ item.raw.icon }}</span>
                </template>
              </v-list-item>
            </template>
          </v-select>
        </div>

        <div class="input-group">
          <label class="input-label">
            <v-icon class="label-icon" size="18">mdi-lock-outline</v-icon>
            Password
          </label>
          <v-text-field
            v-model="form.password"
            :error-messages="errors.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Create a strong password"
            variant="outlined"
            density="comfortable"
            class="custom-input"
            @input="clearFieldError('password')"
          >
            <template v-slot:append-inner>
              <v-icon
                @click="showPassword = !showPassword"
                class="cursor-pointer"
                :color="showPassword ? '#2D6A4F' : '#999'"
                size="18"
              >
                {{ showPassword ? "mdi-eye-off" : "mdi-eye" }}
              </v-icon>
            </template>
          </v-text-field>

          <!-- Password Strength Indicator -->
          <div v-if="form.password" class="password-strength">
            <div class="strength-bars">
              <div
                class="strength-bar"
                :class="{ active: passwordStrength.level >= 1 }"
                :style="{ background: passwordStrength.color }"
              ></div>
              <div
                class="strength-bar"
                :class="{ active: passwordStrength.level >= 2 }"
                :style="{ background: passwordStrength.color }"
              ></div>
              <div
                class="strength-bar"
                :class="{ active: passwordStrength.level >= 3 }"
                :style="{ background: passwordStrength.color }"
              ></div>
              <div
                class="strength-bar"
                :class="{ active: passwordStrength.level >= 4 }"
                :style="{ background: passwordStrength.color }"
              ></div>
            </div>
            <span
              class="strength-text"
              :style="{ color: passwordStrength.color }"
            >
              {{ passwordStrength.text }}
            </span>
          </div>
        </div>

        <div class="input-group">
          <label class="input-label">
            <v-icon class="label-icon" size="18">mdi-lock-check-outline</v-icon>
            Confirm Password
          </label>
          <v-text-field
            v-model="form.confirmPassword"
            :error-messages="errors.confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            placeholder="Confirm your password"
            variant="outlined"
            density="comfortable"
            class="custom-input"
            @input="clearFieldError('confirmPassword')"
          >
            <template v-slot:append-inner>
              <v-icon
                @click="showConfirmPassword = !showConfirmPassword"
                class="cursor-pointer"
                size="18"
                :color="showConfirmPassword ? '#2D6A4F' : '#999'"
              >
                {{ showConfirmPassword ? "mdi-eye-off" : "mdi-eye" }}
              </v-icon>
            </template>
          </v-text-field>
        </div>

        <div class="terms">
          <v-checkbox
            v-model="agreeTerms"
            :error-messages="errors.terms"
            hide-details
            density="compact"
            color="#2D6A4F"
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
          <span class="btn-text">Create Account</span>
          <v-icon class="btn-icon" end>mdi-arrow-right</v-icon>
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
      :timeout="4000"
      location="top"
      class="custom-toast error-toast"
    >
      <div class="toast-content">
        <v-icon class="toast-icon">mdi-alert-circle</v-icon>
        <div class="toast-text">
          <div class="toast-title">Registration Failed</div>
          <div class="toast-message">{{ authStore.error }}</div>
        </div>
      </div>
    </v-snackbar>

    <v-snackbar
      v-model="showSuccess"
      :timeout="3000"
      location="top"
      class="custom-toast success-toast"
    >
      <div class="toast-content">
        <v-icon class="toast-icon">mdi-check-circle</v-icon>
        <div class="toast-text">
          <div class="toast-title">Welcome to Grounds Coffee!</div>
          <div class="toast-message">
            Account created successfully. Redirecting...
          </div>
        </div>
      </div>
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
  { title: "Admin", value: "admin", icon: "👑" },
  { title: "Cashier", value: "cashier", icon: "☕" },
];

// Password strength calculator
const passwordStrength = computed(() => {
  const password = form.password;
  if (!password) return { level: 0, text: "", color: "" };

  let strength = 0;
  if (password.length >= 6) strength++;
  if (password.length >= 8) strength++;
  if (/(?=.*[A-Z])/.test(password)) strength++;
  if (/(?=.*[0-9])/.test(password)) strength++;

  const strengths = {
    1: { text: "Weak", color: "#E07A5F" },
    2: { text: "Fair", color: "#F4A261" },
    3: { text: "Good", color: "#E9C46A" },
    4: { text: "Strong", color: "#2D6A4F" },
  };

  return (
    strengths[strength as keyof typeof strengths] || {
      level: strength,
      text: "",
      color: "",
    }
  );
});

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
      navigateTo("/pos");
    }, 2000);
  } else {
    showError.value = true;
  }
};

// Check if already logged in
onMounted(() => {
  if (authStore.checkAuth()) {
    navigateTo("/pos");
  }
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap");

/* Container & Background */
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 20px;
}

.animated-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: #e07a5f;
  top: -200px;
  right: -200px;
  animation-delay: 0s;
}

.orb-2 {
  width: 600px;
  height: 600px;
  background: #f4a261;
  bottom: -250px;
  left: -250px;
  animation-delay: 5s;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: #e9c46a;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes float {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.coffee-particles {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(
    circle at 10% 20%,
    rgba(255, 255, 255, 0.1) 1px,
    transparent 1px
  );
  background-size: 50px 50px;
  animation: particleShift 30s linear infinite;
}

@keyframes particleShift {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(50px, 50px);
  }
}

/* Auth Card */
.auth-card {
  max-width: 580px;
  width: 100%;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 48px;
  padding: 56px 48px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  position: relative;
  z-index: 1;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Floating Beans */
.floating-beans {
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  pointer-events: none;
}

.floating-bean {
  position: absolute;
  font-size: 24px;
  opacity: 0.15;
  animation: floatBean 4s ease-in-out infinite;
}

.bean-1 {
  top: -30px;
  right: 20px;
  animation-delay: 0s;
}
.bean-2 {
  bottom: -30px;
  left: 20px;
  animation-delay: 1s;
}
.bean-3 {
  top: 50%;
  right: -30px;
  animation-delay: 2s;
}
.bean-4 {
  bottom: 20%;
  left: -30px;
  animation-delay: 3s;
}

@keyframes floatBean {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-15px) rotate(10deg);
  }
}

/* Logo Section */
.logo-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 40px;
}

.logo-ring {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #1b4332, #2d6a4f);
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(45, 106, 79, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(45, 106, 79, 0);
  }
}

.logo-icon {
  font-size: 32px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.logo-text-wrapper {
  text-align: left;
}

.logo-text {
  font-family: "Playfair Display", serif;
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, #1b4332, #2d6a4f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.logo-badge {
  font-size: 10px;
  font-weight: 600;
  color: #e07a5f;
  letter-spacing: 2px;
  margin-top: 4px;
}

/* Welcome Section */
.welcome-section {
  text-align: center;
  margin-bottom: 32px;
}

.welcome-title {
  font-family: "Playfair Display", serif;
  font-size: 36px;
  font-weight: 800;
  margin-bottom: 8px;
}

.gradient-text {
  background: linear-gradient(135deg, #1b4332, #2d6a4f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.welcome-subtitle {
  font-size: 14px;
  color: #6b7280;
}

/* Social Options */
.social-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 24px;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.social-btn.google {
  color: #ea4335;
}

.social-btn.apple {
  color: #000;
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
}

.divider-text {
  font-size: 12px;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Form Styles */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.label-icon {
  color: #2d6a4f;
}

:deep(.custom-input .v-field),
:deep(.custom-select .v-field) {
  border-radius: 20px !important;
  transition: all 0.3s ease;
}

:deep(.custom-input .v-field:hover),
:deep(.custom-select .v-field:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(27, 67, 50, 0.1);
}

:deep(.custom-input .v-field--focused),
:deep(.custom-select .v-field--focused) {
  border-color: #2d6a4f !important;
  box-shadow: 0 0 0 4px rgba(45, 106, 79, 0.1);
}

/* Password Strength */
.password-strength {
  margin-top: 8px;
}

.strength-bars {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: #e5e7eb;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.strength-bar.active {
  background: #2d6a4f;
}

.strength-text {
  font-size: 11px;
  font-weight: 500;
}

/* Terms */
.terms {
  margin: 8px 0;
}

.terms-text {
  font-size: 13px;
  color: #4b5563;
  margin-left: 8px;
}

.terms-link {
  color: #e07a5f;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.terms-link:hover {
  color: #d66b4a;
  text-decoration: underline;
}

/* Auth Button */
.auth-btn {
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%) !important;
  color: white !important;
  font-weight: 700;
  font-size: 16px;
  text-transform: none;
  border-radius: 40px !important;
  padding: 12px !important;
  margin-top: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.auth-btn::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s ease;
}

.auth-btn:hover::before {
  left: 100%;
}

.auth-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(27, 67, 50, 0.3);
}

.btn-text {
  letter-spacing: 0.5px;
}

.btn-icon {
  transition: transform 0.3s ease;
}

.auth-btn:hover .btn-icon {
  transform: translateX(4px);
}

/* Footer */
.auth-footer {
  margin-top: 32px;
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid #f3f4f6;
}

.auth-footer p {
  font-size: 14px;
  color: #6b7280;
}

.login-link {
  color: #e07a5f;
  text-decoration: none;
  font-weight: 600;
  margin-left: 8px;
  transition: color 0.2s;
}

.login-link:hover {
  color: #d66b4a;
  text-decoration: underline;
}

/* Toast */
.custom-toast :deep(.v-snackbar__content) {
  padding: 0 !important;
  background: transparent !important;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  min-width: 320px;
}

.toast-icon {
  font-size: 28px;
}

.toast-text {
  flex: 1;
}

.toast-title {
  font-weight: 700;
  margin-bottom: 4px;
}

.toast-message {
  font-size: 13px;
  color: #6b7280;
}

.error-toast .toast-icon {
  color: #e07a5f;
}

.success-toast .toast-icon {
  color: #2d6a4f;
}

.cursor-pointer {
  cursor: pointer;
}

/* Responsive */
@media (max-width: 640px) {
  .auth-card {
    padding: 32px 24px;
  }

  .welcome-title {
    font-size: 28px;
  }

  .social-options {
    grid-template-columns: 1fr;
  }

  .logo-text {
    font-size: 22px;
  }

  .logo-ring {
    width: 48px;
    height: 48px;
  }

  .logo-icon {
    font-size: 24px;
  }
}
</style>
