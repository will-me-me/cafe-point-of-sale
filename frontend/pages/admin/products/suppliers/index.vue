<!-- pages/admin/products/suppliers/index.vue -->
<template>
  <div class="suppliers-container">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">
          <v-icon size="16" color="#E07A5F">mdi-truck</v-icon>
          Product Management
        </div>
        <h1 class="page-title">Suppliers</h1>
        <p class="page-subtitle">Manage product suppliers and vendors</p>
      </div>
      <v-btn class="add-btn" @click="openAddDialog">
        <v-icon start>mdi-plus</v-icon>
        Add Supplier
      </v-btn>
    </div>

    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background: #2d6a4f20; color: #2d6a4f">
          <v-icon>mdi-truck</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ suppliers.length }}</div>
          <div class="stat-label">Total Suppliers</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: #2d6a4f20; color: #2d6a4f">
          <v-icon>mdi-check-circle</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ activeSuppliers.length }}</div>
          <div class="stat-label">Active Suppliers</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: #e07a5f20; color: #e07a5f">
          <v-icon>mdi-package-variant</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ totalProductsSupplied }}</div>
          <div class="stat-label">Products Supplied</div>
        </div>
      </div>
    </div>

    <!-- Search & Filters -->
    <div class="filters-bar">
      <div class="search-wrapper">
        <v-icon class="search-icon">mdi-magnify</v-icon>
        <input
          v-model="searchQuery"
          placeholder="Search suppliers..."
          class="search-input"
          @input="filterSuppliers"
        />
      </div>
      <div class="filter-group">
        <select
          v-model="statusFilter"
          class="filter-select"
          @change="filterSuppliers"
        >
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
        <select
          v-model="ratingFilter"
          class="filter-select"
          @change="filterSuppliers"
        >
          <option value="">All Ratings</option>
          <option value="4.5">⭐⭐⭐⭐⭐ (4.5+)</option>
          <option value="4.0">⭐⭐⭐⭐ (4.0+)</option>
          <option value="3.0">⭐⭐⭐ (3.0+)</option>
        </select>
        <v-btn
          color="#2D6A4F"
          variant="tonal"
          size="small"
          @click="resetFilters"
        >
          Reset
        </v-btn>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-grid">
      <v-skeleton-loader
        v-for="n in 6"
        :key="n"
        type="card"
        class="supplier-card-skeleton"
      />
    </div>

    <!-- Suppliers Grid -->
    <div v-else class="suppliers-grid">
      <div
        v-for="supplier in filteredSuppliers"
        :key="supplier.id || supplier._id"
        class="supplier-card"
      >
        <div class="supplier-header">
          <div class="supplier-info">
            <div class="supplier-name">{{ supplier.name }}</div>
            <div class="supplier-code" v-if="supplier.code">
              {{ supplier.code }}
            </div>
          </div>
          <div class="supplier-actions">
            <v-btn
              icon
              size="small"
              class="action-btn edit"
              @click="editSupplier(supplier)"
            >
              <v-icon size="16">mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              size="small"
              class="action-btn delete"
              @click="deleteSupplier(supplier)"
            >
              <v-icon size="16">mdi-delete</v-icon>
            </v-btn>
          </div>
        </div>

        <div class="supplier-details">
          <div class="supplier-contact">
            <div class="contact-item" v-if="supplier.contact?.name">
              <v-icon size="16">mdi-account</v-icon>
              <span>{{ supplier.contact.name }}</span>
            </div>
            <div class="contact-item" v-if="supplier.contact?.phone">
              <v-icon size="16">mdi-phone</v-icon>
              <span>{{ supplier.contact.phone }}</span>
            </div>
            <div class="contact-item" v-if="supplier.contact?.email">
              <v-icon size="16">mdi-email</v-icon>
              <span>{{ supplier.contact.email }}</span>
            </div>
          </div>

          <div class="supplier-meta">
            <div class="meta-item">
              <span class="meta-label">Products:</span>
              <span class="meta-value">{{ supplier.product_count || 0 }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Total Spent:</span>
              <span class="meta-value"
                >KSh {{ (supplier.total_spent || 0).toLocaleString() }}</span
              >
            </div>
            <div class="meta-item">
              <v-chip
                :color="supplier.is_active !== false ? '#2D6A4F' : '#E07A5F'"
                size="x-small"
                text-color="white"
              >
                {{ supplier.is_active !== false ? "Active" : "Inactive" }}
              </v-chip>
            </div>
          </div>

          <div class="supplier-rating" v-if="supplier.rating">
            <div class="stars">
              <v-icon
                v-for="n in 5"
                :key="n"
                size="16"
                :color="
                  n <= Math.round(supplier.rating) ? '#F4A261' : '#E5E7EB'
                "
              >
                mdi-star
              </v-icon>
            </div>
            <span class="rating-value">{{ supplier.rating.toFixed(1) }}</span>
            <span class="rating-count" v-if="supplier.rating_count">
              ({{ supplier.rating_count }} reviews)
            </span>
          </div>

          <div v-if="supplier.notes" class="supplier-notes">
            <v-icon size="14">mdi-note-text</v-icon>
            {{ supplier.notes }}
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-if="filteredSuppliers.length === 0"
        class="empty-state d-flex flex-column align-items-center justify-content-center"
      >
        <v-icon size="64" color="#9CA3AF">mdi-truck-off</v-icon>
        <h3>No suppliers found</h3>
        <p>Try adjusting your search or add a new supplier</p>
        <v-btn color="#2D6A4F" @click="openAddDialog">
          <v-icon start>mdi-plus</v-icon>
          Add Supplier
        </v-btn>
      </div>
    </div>

    <!-- Add/Edit Supplier Dialog -->
    <v-dialog v-model="dialogVisible" max-width="600" persistent>
      <v-card class="supplier-dialog">
        <div class="dialog-header">
          <h3>{{ editingSupplier ? "Edit Supplier" : "Add New Supplier" }}</h3>
          <v-btn icon variant="text" @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <v-card-text>
          <v-form ref="formRef" v-model="isValid">
            <v-row>
              <v-col cols="12">
                <div class="form-group">
                  <label class="form-label required">Supplier Name</label>
                  <v-text-field
                    v-model="form.name"
                    placeholder="e.g., Bulk Foods Ltd"
                    variant="outlined"
                    density="comfortable"
                    :rules="[rules.required]"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12" md="6">
                <div class="form-group">
                  <label class="form-label">Supplier Code</label>
                  <v-text-field
                    v-model="form.code"
                    placeholder="e.g., BFL-001"
                    variant="outlined"
                    density="comfortable"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12" md="6">
                <div class="form-group">
                  <label class="form-label">Tax ID</label>
                  <v-text-field
                    v-model="form.tax_id"
                    placeholder="e.g., KRA-123456789"
                    variant="outlined"
                    density="comfortable"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12">
                <div class="form-group">
                  <label class="form-label">Contact Person</label>
                  <v-text-field
                    v-model="form.contact_name"
                    placeholder="Contact person name"
                    variant="outlined"
                    density="comfortable"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12" md="6">
                <div class="form-group">
                  <label class="form-label required">Phone</label>
                  <v-text-field
                    v-model="form.phone"
                    placeholder="e.g., +254-700-123456"
                    variant="outlined"
                    density="comfortable"
                    :rules="[rules.required]"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12" md="6">
                <div class="form-group">
                  <label class="form-label">Email</label>
                  <v-text-field
                    v-model="form.email"
                    placeholder="email@supplier.com"
                    variant="outlined"
                    density="comfortable"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12">
                <div class="form-group">
                  <label class="form-label">Address</label>
                  <v-textarea
                    v-model="form.address"
                    placeholder="Supplier address"
                    variant="outlined"
                    rows="2"
                    density="comfortable"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12">
                <div class="form-group">
                  <label class="form-label">Website</label>
                  <v-text-field
                    v-model="form.website"
                    placeholder="https://www.example.com"
                    variant="outlined"
                    density="comfortable"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12">
                <div class="form-group">
                  <label class="form-label">Notes</label>
                  <v-textarea
                    v-model="form.notes"
                    placeholder="Additional notes about the supplier..."
                    variant="outlined"
                    rows="2"
                    density="comfortable"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12">
                <v-switch v-model="form.is_active" color="#2D6A4F" hide-details>
                  <template #label>
                    <div>
                      <div class="switch-label">Active</div>
                      <div class="switch-hint">
                        Supplier visible in the system
                      </div>
                    </div>
                  </template>
                </v-switch>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="closeDialog">Cancel</v-btn>
          <v-btn
            color="#2D6A4F"
            :disabled="!isValid || submitting"
            :loading="submitting"
            @click="saveSupplier"
          >
            {{ editingSupplier ? "Update" : "Create" }} Supplier
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card class="delete-dialog">
        <div class="delete-icon">
          <v-icon size="60" color="#E07A5F">mdi-alert-circle</v-icon>
        </div>
        <h3>Delete Supplier?</h3>
        <p>
          Are you sure you want to delete "{{ supplierToDelete?.name }}"?
          <br />
          <span class="text-caption text-medium-emphasis">
            {{ supplierToDelete?.product_count || 0 }} products are supplied by
            this vendor.
          </span>
        </p>
        <div class="delete-actions">
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="#E07A5F" :loading="deleting" @click="confirmDelete">
            Delete
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
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" icon="mdi-close" @click="snackbar.show = false" />
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { usePosStore } from "~/stores/pos";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

// State
const posStore = usePosStore();
const suppliers = ref([]);
const loading = ref(true);
const submitting = ref(false);
const deleting = ref(false);
const dialogVisible = ref(false);
const deleteDialog = ref(false);
const editingSupplier = ref(null);
const supplierToDelete = ref(null);
const searchQuery = ref("");
const statusFilter = ref("");
const ratingFilter = ref("");
const isValid = ref(false);
const formRef = ref(null);

const form = ref({
  name: "",
  code: "",
  tax_id: "",
  contact_name: "",
  phone: "",
  email: "",
  address: "",
  website: "",
  notes: "",
  is_active: true,
});

const snackbar = ref({
  show: false,
  text: "",
  color: "success",
});

// Rules
const rules = {
  required: (v: any) => !!v || "This field is required",
};

// Computed
const activeSuppliers = computed(() =>
  suppliers.value.filter((s) => s.is_active !== false)
);

const totalProductsSupplied = computed(() =>
  suppliers.value.reduce((sum, s) => sum + (s.product_count || 0), 0)
);

const filteredSuppliers = computed(() => {
  let filtered = [...suppliers.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (s) =>
        s.name.toLowerCase().includes(query) ||
        (s.code && s.code.toLowerCase().includes(query)) ||
        (s.contact?.name && s.contact.name.toLowerCase().includes(query)) ||
        (s.contact?.email && s.contact.email.toLowerCase().includes(query))
    );
  }

  if (statusFilter.value) {
    filtered = filtered.filter((s) => {
      if (statusFilter.value === "active") return s.is_active !== false;
      if (statusFilter.value === "inactive") return s.is_active === false;
      return true;
    });
  }

  if (ratingFilter.value) {
    const minRating = parseFloat(ratingFilter.value);
    filtered = filtered.filter((s) => (s.rating || 0) >= minRating);
  }

  return filtered;
});

// Methods
const filterSuppliers = () => {
  // Computed handles filtering
};

const resetFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
  ratingFilter.value = "";
};

const openAddDialog = () => {
  editingSupplier.value = null;
  resetForm();
  dialogVisible.value = true;
};

const editSupplier = (supplier: any) => {
  console.log("Editing supplier:", supplier);
  editingSupplier.value = supplier;
  const contact = supplier.contact || {};
  form.value = {
    name: supplier.name || "",
    code: supplier.code || "",
    tax_id: supplier.tax_id || "",
    contact_name: contact.name || "",
    phone: contact.phone || "",
    email: contact.email || "",
    address: contact.address.street || "",
    website: supplier.website || "",
    notes: supplier.notes || "",
    is_active: supplier.is_active !== false,
  };
  console.log("Form data for editing:", form.value);

  dialogVisible.value = true;
};

const resetForm = () => {
  form.value = {
    name: "",
    code: "",
    tax_id: "",
    contact_name: "",
    phone: "",
    email: "",
    address: "",
    website: "",
    notes: "",
    is_active: true,
  };
};

const closeDialog = () => {
  dialogVisible.value = false;
  resetForm();
};

const saveSupplier = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  submitting.value = true;
  try {
    const supplierData = {
      name: form.value.name,
      code: form.value.code || undefined,
      tax_id: form.value.tax_id || undefined,
      contact: {
        name: form.value.contact_name || undefined,
        phone: form.value.phone,
        email: form.value.email || undefined,
        address: form.value.address || undefined,
      },
      website: form.value.website || undefined,
      notes: form.value.notes || undefined,
      is_active: form.value.is_active,
    };
    if (editingSupplier.value) {
      // Update existing supplier
      await posStore.updateSupplier(editingSupplier.value.id, supplierData);
      await loadSuppliers();
    } else {
      // Create new supplier
      await posStore.addSupplier(supplierData);
      console.log("Supplier data:", supplierData);
    }

    snackbar.value = {
      show: true,
      text: `Supplier ${
        editingSupplier.value ? "updated" : "created"
      } successfully!`,
      color: "success",
    };

    closeDialog();
    await loadSuppliers();
  } catch (error) {
    console.error("Error saving supplier:", error);
    snackbar.value = {
      show: true,
      text: "Failed to save supplier",
      color: "error",
    };
  } finally {
    submitting.value = false;
  }
};

const deleteSupplier = (supplier: any) => {
  supplierToDelete.value = supplier;
  deleteDialog.value = true;
};

const confirmDelete = async () => {
  deleting.value = true;
  try {
    snackbar.value = {
      show: true,
      text: "Supplier deleted successfully!",
      color: "success",
    };
    console.log("Deleting supplier:", supplierToDelete.value.id);

    await posStore.deleteSupplier(supplierToDelete.value.id);
    deleteDialog.value = false;
    await loadSuppliers();
  } catch (error) {
    console.error("Error deleting supplier:", error);
    snackbar.value = {
      show: true,
      text: "Failed to delete supplier",
      color: "error",
    };
  } finally {
    deleting.value = false;
  }
};

const loadSuppliers = async () => {
  loading.value = true;
  try {
    // TODO: API Call
    suppliers.value = await posStore.getAllSuppliers();
    // suppliers.value = [
    //   {
    //     id: "1",
    //     name: "Beverage Distributors Ltd",
    //     code: "BDL-001",
    //     contact: {
    //       name: "John Smith",
    //       phone: "+254-700-123456",
    //       email: "john@bdl.com",
    //       address: "123 Industrial Area, Nairobi",
    //     },
    //     rating: 4.5,
    //     rating_count: 12,
    //     is_active: true,
    //     product_count: 8,
    //     total_spent: 1250000,
    //     notes: "Main beverage supplier",
    //   },
    //   {
    //     id: "2",
    //     name: "Electronics World Ltd",
    //     code: "EWL-001",
    //     contact: {
    //       name: "Mary Wangari",
    //       phone: "+254-722-987654",
    //       email: "mary@ewl.com",
    //       address: "456 Tech Park, Nairobi",
    //     },
    //     rating: 4.2,
    //     rating_count: 8,
    //     is_active: true,
    //     product_count: 5,
    //     total_spent: 850000,
    //     notes: "Electronics and gadgets",
    //   },
    // ];
  } catch (error) {
    console.error("Error loading suppliers:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadSuppliers();
});
</script>

<style scoped>
.suppliers-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Reuse styles from brands page with supplier-specific additions */
.brands-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

.page-badge {
  font-size: 12px;
  font-weight: 600;
  color: #e07a5f;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.page-title {
  font-family: "Playfair Display", serif;
  font-size: 28px;
  font-weight: 800;
  color: #1b4332;
  margin-bottom: 4px;
}

.page-subtitle {
  color: #6b7280;
  font-size: 14px;
}

.add-btn {
  background: linear-gradient(135deg, #1b4332, #2d6a4f);
  color: white;
  text-transform: none;
  border-radius: 40px;
  padding: 0 24px;
  height: 44px;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 800;
  color: #1b4332;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
}

/* Filters */
.filters-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-wrapper {
  flex: 1;
  min-width: 200px;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 40px;
  padding: 0 16px;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.search-icon {
  color: #9ca3af;
}

.search-input {
  flex: 1;
  border: none;
  padding: 12px 0;
  font-size: 14px;
  outline: none;
  background: transparent;
}

.filter-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select {
  padding: 10px 16px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
  cursor: pointer;
  font-size: 14px;
}

/* Brands Grid */
.brands-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.brand-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #e5e7eb;
}

.brand-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  border-color: #2d6a4f;
}

.brand-logo-wrapper {
  position: relative;
  height: 140px;
  background: #f8f6f2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-logo {
  width: 80px;
  height: 80px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.brand-actions {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.brand-card:hover .brand-actions {
  opacity: 1;
}

.action-btn {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-btn.edit:hover {
  background: #2d6a4f;
  color: white;
}

.action-btn.delete:hover {
  background: #e07a5f;
  color: white;
}

.brand-details {
  padding: 16px 20px;
}

.brand-name {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 8px;
}

.brand-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.brand-products {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #6b7280;
}

.brand-description {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 8px;
}

.brand-website {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
}

.brand-website a {
  color: #2d6a4f;
  text-decoration: none;
}

.brand-website a:hover {
  text-decoration: underline;
}

/* Dialog */
.brand-dialog {
  border-radius: 24px !important;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 0;
}

.dialog-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}
.delete-dialog {
  text-align: center;
  padding: 32px;
  border-radius: 24px !important;
}

.delete-icon {
  margin-bottom: 20px;
}

.delete-dialog h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 12px;
}

.delete-dialog p {
  color: #6b7280;
  margin-bottom: 24px;
}

.delete-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

/* Responsive */
@media (max-width: 768px) {
  .brands-container {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-title {
    font-size: 24px;
  }

  .add-btn {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .filters-bar {
    flex-direction: column;
  }

  .search-wrapper {
    width: 100%;
  }

  .filter-group {
    width: 100%;
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
  }

  .brands-grid {
    grid-template-columns: 1fr;
  }

  .brand-logo-wrapper {
    height: 120px;
  }

  .brand-logo {
    width: 60px;
    height: 60px;
  }

  .brand-actions {
    opacity: 1;
  }
}

.supplier-card {
  background: white;
  border-radius: 16px;
  padding: 16px 20px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #e5e7eb;
}

.supplier-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  border-color: #2d6a4f;
}

.supplier-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 8px;
}

.supplier-name {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.supplier-code {
  font-size: 12px;
  color: #6b7280;
}

.supplier-contact {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 4px 16px;
  margin-bottom: 12px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #374151;
}

.supplier-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
}

.meta-label {
  color: #6b7280;
}

.meta-value {
  font-weight: 600;
  color: #1b4332;
}

.supplier-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.stars {
  display: flex;
  align-items: center;
  gap: 2px;
}

.rating-value {
  font-weight: 700;
  color: #1b4332;
}

.rating-count {
  font-size: 12px;
  color: #6b7280;
}

.supplier-notes {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  font-size: 13px;
  color: #6b7280;
  padding: 8px 12px;
  background: #f8f6f2;
  border-radius: 8px;
  margin-top: 8px;
}

/* Responsive */
@media (max-width: 768px) {
  .suppliers-container {
    padding: 16px;
  }

  .supplier-contact {
    grid-template-columns: 1fr;
  }

  .supplier-header {
    flex-direction: column;
  }

  .supplier-actions {
    align-self: flex-start;
  }

  .supplier-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}

/* Reuse other styles from brands page */
</style>
