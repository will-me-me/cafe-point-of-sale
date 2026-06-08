<!-- frontend/pages/admin/users.vue -->
<template>
  <div class="users-container">
    <!-- Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">User Management</div>
        <h1 class="page-title">Manage Users</h1>
        <p class="page-subtitle">Manage staff accounts and permissions</p>
      </div>
      <v-btn class="add-user-btn" color="#2D6A4F" @click="openAddUserDialog">
        <v-icon start>mdi-plus</v-icon>
        Add New User
      </v-btn>
    </div>

    <!-- Stats Cards -->
    <v-row class="stats-row" gutter="24">
      <v-col cols="12" md="3" sm="6">
        <v-card class="stat-card" elevation="0">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-value">{{ users.length }}</div>
              <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-icon-wrapper" style="background: #2d6a4f20">
              <v-icon color="#2D6A4F" size="28">mdi-account-group</v-icon>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="3" sm="6">
        <v-card class="stat-card" elevation="0">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-value">{{ adminCount }}</div>
              <div class="stat-label">Administrators</div>
            </div>
            <div class="stat-icon-wrapper" style="background: #e07a5f20">
              <v-icon color="#E07A5F" size="28">mdi-crown</v-icon>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="3" sm="6">
        <v-card class="stat-card" elevation="0">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-value">{{ cashierCount }}</div>
              <div class="stat-label">Cashiers</div>
            </div>
            <div class="stat-icon-wrapper" style="background: #f4a26120">
              <v-icon color="#F4A261" size="28">mdi-coffee</v-icon>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="3" sm="6">
        <v-card class="stat-card" elevation="0">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-value">{{ activeUsers }}</div>
              <div class="stat-label">Active Now</div>
            </div>
            <div class="stat-icon-wrapper" style="background: #2d6a4f20">
              <v-icon color="#2D6A4F" size="28">mdi-account-check</v-icon>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Filters and Search -->
    <v-card class="filters-card" elevation="0">
      <v-row align="center" no-gutters>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="searchQuery"
            placeholder="Search by name or email..."
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-magnify"
            hide-details
            class="search-field"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="selectedRole"
            :items="roleFilters"
            item-title="title"
            item-value="value"
            placeholder="Filter by role"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-filter"
            hide-details
            class="filter-select"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="selectedStatus"
            :items="statusFilters"
            item-title="title"
            item-value="value"
            placeholder="Filter by status"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-filter"
            hide-details
            class="filter-select"
          />
        </v-col>
        <v-col cols="12" md="2" class="text-right">
          <v-btn variant="text" @click="clearFilters" class="clear-btn">
            Clear All
          </v-btn>
        </v-col>
      </v-row>
    </v-card>

    <!-- Users Table -->
    <v-card class="users-table-card" elevation="0">
      <v-data-table
        :headers="headers"
        :items="filteredUsers"
        :loading="loading"
        :search="searchQuery"
        :items-per-page="itemsPerPage"
        class="users-table"
        hover
      >
        <!-- User Avatar Template -->
        <template v-slot:item.avatar="{ item }">
          <div class="user-avatar-wrapper">
            <v-avatar
              :color="getAvatarColor(item.role)"
              size="40"
              class="user-avatar"
            >
              <span class="avatar-text">{{ getInitials(item.name) }}</span>
            </v-avatar>
            <div
              v-if="item.status === 'active'"
              class="status-dot active"
            ></div>
            <div v-else class="status-dot inactive"></div>
          </div>
        </template>

        <!-- User Info Template -->
        <template v-slot:item.name="{ item }">
          <div>
            <div class="user-name">{{ item.name }}</div>
            <div class="user-email">{{ item.email }}</div>
          </div>
        </template>

        <!-- Role Badge Template -->
        <template v-slot:item.role="{ item }">
          <v-chip
            :color="item.role === 'admin' ? '#E07A5F' : '#2D6A4F'"
            size="small"
            class="role-chip"
          >
            <v-icon start size="14">
              {{ item.role === "admin" ? "mdi-crown" : "mdi-coffee" }}
            </v-icon>
            {{ item.role === "admin" ? "Admin" : "Cashier" }}
          </v-chip>
        </template>

        <!-- Status Template -->
        <template v-slot:item.status="{ item }">
          <v-chip
            :color="item.status === 'active' ? '#2D6A4F' : '#9CA3AF'"
            size="small"
            class="status-chip"
          >
            <v-icon start size="12">
              {{
                item.status === "active"
                  ? "mdi-check-circle"
                  : "mdi-clock-outline"
              }}
            </v-icon>
            {{ item.status === "active" ? "Active" : "Inactive" }}
          </v-chip>
        </template>

        <!-- Last Active Template -->
        <template v-slot:item.lastActive="{ item }">
          <div class="last-active">
            <v-icon size="14" class="mr-1">mdi-calendar</v-icon>
            {{ formatDate(item.lastActive) }}
          </div>
        </template>

        <!-- Actions Template -->
        <template v-slot:item.actions="{ item }">
          <div class="action-buttons">
            <v-btn
              icon
              size="small"
              variant="text"
              color="#2D6A4F"
              @click="editUser(item)"
              class="action-btn"
            >
              <v-icon size="18">mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              size="small"
              variant="text"
              color="#E07A5F"
              @click="toggleUserStatus(item)"
              class="action-btn"
            >
              <v-icon size="18">{{
                item.status === "active"
                  ? "mdi-pause-circle"
                  : "mdi-play-circle"
              }}</v-icon>
            </v-btn>
            <v-btn
              icon
              size="small"
              variant="text"
              color="#EF4444"
              @click="confirmDelete(item)"
              class="action-btn"
            >
              <v-icon size="18">mdi-delete</v-icon>
            </v-btn>
          </div>
        </template>

        <!-- No Data Template -->
        <template v-slot:no-data>
          <div class="empty-state">
            <v-icon size="64" color="#E5E7EB">mdi-account-group</v-icon>
            <p class="empty-title">No users found</p>
            <p class="empty-subtitle">
              Try adjusting your search or filter criteria
            </p>
            <v-btn color="#2D6A4F" variant="text" @click="clearFilters">
              Clear Filters
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Add/Edit User Dialog -->
    <v-dialog
      v-model="userDialog"
      max-width="600"
      transition="dialog-transition"
    >
      <v-card class="user-dialog">
        <v-card-title class="dialog-title">
          <div class="title-content">
            <v-icon size="28" color="#2D6A4F" class="mr-3">
              {{ editingUser ? "mdi-account-edit" : "mdi-account-plus" }}
            </v-icon>
            <span>{{ editingUser ? "Edit User" : "Add New User" }}</span>
          </div>
          <v-btn icon variant="text" @click="userDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="dialog-content">
          <v-form ref="formRef" v-model="isFormValid">
            <!-- Avatar Section -->
            <div class="avatar-upload-section">
              <div class="avatar-preview" @click="triggerFileInput">
                <v-avatar
                  size="80"
                  :color="getAvatarColor(form.role)"
                  class="upload-avatar"
                >
                  <v-img v-if="imagePreview" :src="imagePreview" />
                  <span v-else class="avatar-upload-text">
                    {{ getInitials(form.name || "U") }}
                  </span>
                </v-avatar>
                <div class="upload-overlay">
                  <v-icon size="20">mdi-camera</v-icon>
                </div>
              </div>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                hidden
                @change="handleImageUpload"
              />
              <div class="avatar-info">
                <p class="avatar-label">Profile Picture</p>
                <p class="avatar-hint">Click to upload (JPG, PNG, max 2MB)</p>
              </div>
            </div>

            <v-row class="mt-4">
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.name"
                  label="Full Name"
                  placeholder="John Doe"
                  variant="outlined"
                  :rules="[rules.required]"
                  prepend-inner-icon="mdi-account"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.email"
                  label="Email Address"
                  placeholder="john@coffee.com"
                  variant="outlined"
                  :rules="[rules.required, rules.email]"
                  prepend-inner-icon="mdi-email"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="form.role"
                  label="Role"
                  :items="roleOptions"
                  item-title="title"
                  item-value="value"
                  variant="outlined"
                  :rules="[rules.required]"
                  prepend-inner-icon="mdi-badge-account"
                >
                  <template v-slot:item="{ item, props }">
                    <v-list-item v-bind="props">
                      <template v-slot:prepend>
                        <v-icon
                          :color="
                            item.value === 'admin' ? '#E07A5F' : '#2D6A4F'
                          "
                        >
                          {{
                            item.value === "admin" ? "mdi-crown" : "mdi-coffee"
                          }}
                        </v-icon>
                      </template>
                    </v-list-item>
                  </template>
                </v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="form.status"
                  label="Status"
                  :items="statusOptions"
                  item-title="title"
                  item-value="value"
                  variant="outlined"
                  :rules="[rules.required]"
                  prepend-inner-icon="mdi-account-check"
                />
              </v-col>
            </v-row>

            <v-row v-if="!editingUser">
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.password"
                  label="Password"
                  type="password"
                  placeholder="Create password"
                  variant="outlined"
                  :rules="[rules.required, rules.password]"
                  prepend-inner-icon="mdi-lock"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.confirmPassword"
                  label="Confirm Password"
                  type="password"
                  placeholder="Confirm password"
                  variant="outlined"
                  :rules="[rules.required, rules.confirmPassword]"
                  prepend-inner-icon="mdi-lock-check"
                />
              </v-col>
            </v-row>

            <v-row v-else>
              <v-col cols="12">
                <v-text-field
                  v-model="form.password"
                  label="New Password (Optional)"
                  type="password"
                  placeholder="Leave blank to keep current"
                  variant="outlined"
                  prepend-inner-icon="mdi-lock-reset"
                  hint="Only fill if you want to change password"
                />
              </v-col>
            </v-row>

            <v-divider class="my-4" />

            <div class="permissions-section">
              <div class="section-title">
                <v-icon size="20">mdi-shield-account</v-icon>
                <span>Permissions</span>
              </div>
              <v-row>
                <v-col cols="12" md="6">
                  <v-checkbox
                    v-model="form.permissions.viewOrders"
                    label="View Orders"
                    color="#2D6A4F"
                    hide-details
                  />
                  <v-checkbox
                    v-model="form.permissions.createOrders"
                    label="Create Orders"
                    color="#2D6A4F"
                    hide-details
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-checkbox
                    v-model="form.permissions.manageProducts"
                    label="Manage Products"
                    color="#2D6A4F"
                    hide-details
                    :disabled="form.role !== 'admin'"
                  />
                  <v-checkbox
                    v-model="form.permissions.viewReports"
                    label="View Reports"
                    color="#2D6A4F"
                    hide-details
                  />
                </v-col>
              </v-row>
            </div>
          </v-form>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="outlined" @click="userDialog = false">Cancel</v-btn>
          <v-btn
            color="#2D6A4F"
            :disabled="!isFormValid"
            @click="saveUser"
            class="save-btn"
          >
            <v-icon start>{{
              editingUser ? "mdi-content-save" : "mdi-check"
            }}</v-icon>
            {{ editingUser ? "Update User" : "Create User" }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card class="delete-dialog">
        <div class="delete-icon-wrapper">
          <v-icon size="64" color="#E07A5F">mdi-alert-circle</v-icon>
        </div>
        <h3 class="delete-title">Delete User?</h3>
        <p class="delete-message">
          Are you sure you want to delete
          <strong>{{ userToDelete?.name }}</strong
          >? This action cannot be undone.
        </p>
        <div class="delete-actions">
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn
            color="#E07A5F"
            @click="confirmDeleteUser"
            class="delete-confirm-btn"
          >
            Delete User
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :timeout="3000"
      :color="snackbar.color"
      location="top"
      class="custom-snackbar"
    >
      <v-icon start>{{ snackbar.icon }}</v-icon>
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" icon="mdi-close" @click="snackbar.show = false" />
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "~/stores/auth";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const authStore = useAuthStore();
const loading = ref(false);
const userDialog = ref(false);
const deleteDialog = ref(false);
const editingUser = ref(null);
const userToDelete = ref(null);
const isFormValid = ref(false);
const formRef = ref(null);
const fileInput = ref(null);
const imagePreview = ref("");
const searchQuery = ref("");
const selectedRole = ref("");
const selectedStatus = ref("");
const itemsPerPage = ref(10);

// Form data
const form = ref({
  name: "",
  email: "",
  role: "cashier",
  status: "active",
  password: "",
  confirmPassword: "",
  avatar: null,
  permissions: {
    viewOrders: true,
    createOrders: true,
    manageProducts: false,
    viewReports: false,
  },
});
const users = computed(() => authStore.AllDbUsers || []);

// Table headers
const headers = [
  { title: "", key: "avatar", sortable: false, width: 80 },
  { title: "User", key: "name", sortable: true },
  { title: "Role", key: "role", sortable: true },
  { title: "Status", key: "status", sortable: true },
  { title: "Last Active", key: "lastActive", sortable: true },
  { title: "Actions", key: "actions", sortable: false, align: "center" },
];

// Filter options
const roleFilters = [
  { title: "All Roles", value: "" },
  { title: "Admin", value: "admin" },
  { title: "Cashier", value: "cashier" },
];

const statusFilters = [
  { title: "All Status", value: "" },
  { title: "Active", value: "active" },
  { title: "Inactive", value: "inactive" },
];

const roleOptions = [
  { title: "👑 Administrator", value: "admin" },
  { title: "☕ Cashier", value: "cashier" },
];

const statusOptions = [
  { title: "Active", value: "active" },
  { title: "Inactive", value: "inactive" },
];

// Validation rules
const rules = {
  required: (v: any) => !!v || "This field is required",
  email: (v: string) => /.+@.+\..+/.test(v) || "Valid email required",
  password: (v: string) => {
    if (!v) return "Password is required";
    if (v.length < 6) return "Password must be at least 6 characters";
    return true;
  },
  confirmPassword: (v: string) => {
    if (!v) return "Please confirm password";
    if (v !== form.value.password) return "Passwords do not match";
    return true;
  },
};

// Computed
const filteredUsers = computed(() => {
  let filtered = [...users.value];

  if (searchQuery.value) {
    filtered = filtered.filter(
      (user) =>
        user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  if (selectedRole.value) {
    filtered = filtered.filter((user) => user.role === selectedRole.value);
  }

  if (selectedStatus.value) {
    filtered = filtered.filter((user) => user.status === selectedStatus.value);
  }

  return filtered;
});

const adminCount = computed(
  () => users.value.filter((u) => u.role === "admin").length
);
const cashierCount = computed(
  () => users.value.filter((u) => u.role === "cashier").length
);
const activeUsers = computed(
  () => users.value.filter((u) => u.status === "active").length
);

// Snackbar
const snackbar = ref({
  show: false,
  text: "",
  color: "success",
  icon: "mdi-check-circle",
});

// Helper functions
const getInitials = (name: string) => {
  if (!name) return "U";
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
};

const getAvatarColor = (role: string) => {
  return role === "admin" ? "#E07A5F" : "#2D6A4F";
};

const formatDate = (date: Date) => {
  if (!date) return "Never";
  const now = new Date();
  const diff = now.getTime() - new Date(date).getTime();
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (days === 0) return "Today";
  if (days === 1) return "Yesterday";
  if (days < 7) return `${days} days ago`;
  return new Date(date).toLocaleDateString();
};

const showMessage = (text: string, color: string = "success") => {
  snackbar.value = {
    show: true,
    text,
    color,
    icon: color === "success" ? "mdi-check-circle" : "mdi-alert-circle",
  };
};

// User actions
const openAddUserDialog = () => {
  editingUser.value = null;
  form.value = {
    name: "",
    email: "",
    role: "cashier",
    status: "active",
    password: "",
    confirmPassword: "",
    avatar: null,
    permissions: {
      viewOrders: true,
      createOrders: true,
      manageProducts: false,
      viewReports: false,
    },
  };
  imagePreview.value = "";
  userDialog.value = true;
};

const editUser = (user: any) => {
  editingUser.value = user;
  form.value = {
    name: user.name,
    email: user.email,
    role: user.role,
    status: user.status,
    password: "",
    confirmPassword: "",
    avatar: user.avatar,
    permissions: user.permissions || {
      viewOrders: true,
      createOrders: true,
      manageProducts: user.role === "admin",
      viewReports: true,
    },
  };
  imagePreview.value = user.avatar;
  userDialog.value = true;
};

const saveUser = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  if (editingUser.value) {
    // Update existing user
    const index = users.value.findIndex((u) => u.id === editingUser.value.id);
    if (index !== -1) {
      users.value[index] = {
        ...users.value[index],
        name: form.value.name,
        email: form.value.email,
        role: form.value.role,
        status: form.value.status,
        ...(form.value.password && { password: form.value.password }),
      };
      showMessage("User updated successfully!");
    }
  } else {
    // Create new user
    const newUser = {
      id: users.value.length + 1,
      name: form.value.name,
      email: form.value.email,
      role: form.value.role,
      status: form.value.status,
      lastActive: new Date(),
      avatar: imagePreview.value || null,
    };
    users.value.push(newUser);
    showMessage("User created successfully!");
  }

  userDialog.value = false;
};

const toggleUserStatus = async (user: any) => {
  user.status = user.status === "active" ? "inactive" : "active";
  await authStore.UserStatus(user.id, user.status);
  await authStore.getAllUsers();
  showMessage(
    `User ${
      user.status === "active" ? "activated" : "deactivated"
    } successfully!`
  );
};

const confirmDelete = (user: any) => {
  console.log("User to delete:", user);
  userToDelete.value = user;
  deleteDialog.value = true;
};

const confirmDeleteUser = async () => {
  try {
    users.value = users.value.filter(
      (u: any) => u.id !== userToDelete.value.id
    );
    await authStore.deleteUser(userToDelete.value.id);
    await authStore.getAllUsers();
    console.log("Deleted user and Fetched Users:", userToDelete.value);
    showMessage("User deleted successfully!", "error");
  } catch (error) {
    showMessage("Failed to delete user. Please try again.", "error");
  } finally {
    deleteDialog.value = false;
  }
};

const clearFilters = () => {
  searchQuery.value = "";
  selectedRole.value = "";
  selectedStatus.value = "";
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleImageUpload = (event: any) => {
  const file = event.target.files[0];
  if (file) {
    form.value.avatar = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target?.result;
    };
    reader.readAsDataURL(file);
  }
};

onMounted(async () => {
  // Fetch users from API
  await authStore.getAllUsers();
  loading.value = false;
});
</script>

<style scoped>
.users-container {
  padding: 32px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-badge {
  font-size: 12px;
  font-weight: 600;
  color: #e07a5f;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 8px;
}

.page-title {
  font-family: "Playfair Display", serif;
  font-size: 32px;
  font-weight: 800;
  color: #1b4332;
  margin-bottom: 8px;
}

.page-subtitle {
  color: #6b7280;
}

.add-user-btn {
  text-transform: none;
  border-radius: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Stats Cards */
.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 20px;
  padding: 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  color: #1b4332;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
}

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Filters Card */
.filters-card {
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 24px;
}

.search-field,
.filter-select {
  padding-right: 12px;
}

.clear-btn {
  color: #e07a5f;
  text-transform: none;
}

/* Users Table */
.users-table-card {
  border-radius: 24px;
  overflow: hidden;
}

.users-table {
  border-radius: 24px;
}

.user-avatar-wrapper {
  position: relative;
  display: inline-block;
}

.user-avatar {
  font-size: 16px;
  font-weight: 600;
}

.avatar-text {
  color: white;
  font-weight: 600;
}

.status-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid white;
}

.status-dot.active {
  background: #2d6a4f;
}

.status-dot.inactive {
  background: #9ca3af;
}

.user-name {
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 4px;
}

.user-email {
  font-size: 12px;
  color: #6b7280;
}

.role-chip,
.status-chip {
  text-transform: capitalize;
  font-weight: 500;
}

.last-active {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #6b7280;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.action-btn {
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: scale(1.1);
}

/* Dialog Styles */
.user-dialog {
  border-radius: 32px !important;
  overflow: hidden;
}

.dialog-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0 24px;
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
}

.title-content {
  display: flex;
  align-items: center;
}

.dialog-content {
  padding: 24px;
}

.avatar-upload-section {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}

.avatar-preview {
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-avatar {
  transition: opacity 0.3s ease;
}

.avatar-preview:hover .upload-avatar {
  opacity: 0.7;
}

.upload-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: white;
}

.avatar-preview:hover .upload-overlay {
  opacity: 1;
}

.avatar-info {
  flex: 1;
}

.avatar-label {
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 4px;
}

.avatar-hint {
  font-size: 11px;
  color: #6b7280;
}

.permissions-section {
  margin-top: 8px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 16px;
}

.dialog-actions {
  padding: 16px 24px 24px;
  gap: 12px;
}

.save-btn {
  border-radius: 40px;
  text-transform: none;
}

/* Delete Dialog */
.delete-dialog {
  text-align: center;
  padding: 32px;
  border-radius: 32px !important;
}

.delete-icon-wrapper {
  margin-bottom: 20px;
}

.delete-title {
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 12px;
}

.delete-message {
  color: #6b7280;
  margin-bottom: 24px;
  line-height: 1.5;
}

.delete-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.delete-confirm-btn {
  border-radius: 40px;
  text-transform: none;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 48px;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: #1b4332;
  margin-top: 16px;
  margin-bottom: 8px;
}

.empty-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 20px;
}

/* Snackbar */
.custom-snackbar :deep(.v-snackbar__content) {
  font-weight: 500;
  border-radius: 12px;
}

/* Responsive */
@media (max-width: 768px) {
  .users-container {
    padding: 20px;
  }

  .page-title {
    font-size: 28px;
  }

  .stat-value {
    font-size: 24px;
  }

  .avatar-upload-section {
    flex-direction: column;
    text-align: center;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style>
