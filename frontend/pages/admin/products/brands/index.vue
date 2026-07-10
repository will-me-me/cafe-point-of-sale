<!-- pages/admin/products/brands/index.vue -->
<template>
  <div class="brands-container">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">
          <v-icon size="16" color="#E07A5F">mdi-tag</v-icon>
          Product Management
        </div>
        <h1 class="page-title">Brands</h1>
        <p class="page-subtitle">
          Manage your product brands and manufacturers
        </p>
      </div>
      <v-btn class="add-btn" @click="openAddDialog">
        <v-icon start>mdi-plus</v-icon>
        Add Brand
      </v-btn>
    </div>

    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background: #2d6a4f20; color: #2d6a4f">
          <v-icon>mdi-tag</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ brands.length }}</div>
          <div class="stat-label">Total Brands</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: #2d6a4f20; color: #2d6a4f">
          <v-icon>mdi-check-circle</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ activeBrands.length }}</div>
          <div class="stat-label">Active Brands</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: #e07a5f20; color: #e07a5f">
          <v-icon>mdi-package-variant</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ totalProducts }}</div>
          <div class="stat-label">Products with Brands</div>
        </div>
      </div>
    </div>

    <!-- Search & Filters -->
    <div class="filters-bar">
      <div class="search-wrapper">
        <v-icon class="search-icon">mdi-magnify</v-icon>
        <input
          v-model="searchQuery"
          placeholder="Search brands..."
          class="search-input"
          @input="filterBrands"
        />
      </div>
      <div class="filter-group">
        <select
          v-model="statusFilter"
          class="filter-select"
          @change="filterBrands"
        >
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
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
        class="brand-card-skeleton"
      />
    </div>

    <!-- Brands Grid -->
    <div v-else class="brands-grid">
      <div
        v-for="brand in filteredBrands"
        :key="brand.id || brand._id"
        class="brand-card"
      >
        <div class="brand-logo-wrapper">
          <div class="brand-logo">
            <v-icon size="48" color="#2D6A4F">mdi-tag</v-icon>
          </div>
          <div class="brand-actions">
            <v-btn
              icon
              size="small"
              class="action-btn edit"
              @click="editBrand(brand)"
            >
              <v-icon size="18">mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              size="small"
              class="action-btn delete"
              @click="deleteBrand(brand)"
            >
              <v-icon size="18">mdi-delete</v-icon>
            </v-btn>
          </div>
        </div>
        <div class="brand-details">
          <h3 class="brand-name">{{ brand.name }}</h3>
          <div class="brand-meta">
            <span class="brand-products">
              <v-icon size="14">mdi-package-variant</v-icon>
              {{ brand.product_count || 0 }} products
            </span>
            <v-chip
              :color="brand.is_active !== false ? '#2D6A4F' : '#E07A5F'"
              size="x-small"
              text-color="white"
            >
              {{ brand.is_active !== false ? "Active" : "Inactive" }}
            </v-chip>
          </div>
          <div v-if="brand.description" class="brand-description">
            {{ brand.description }}
          </div>
          <div v-if="brand.website" class="brand-website">
            <v-icon size="14">mdi-web</v-icon>
            <a :href="brand.website" target="_blank">{{ brand.website }}</a>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredBrands.length === 0" class="empty-state">
        <v-icon size="64" color="#9CA3AF">mdi-tag-off</v-icon>
        <h3>No brands found</h3>
        <p>Try adjusting your search or add a new brand</p>
        <v-btn color="#2D6A4F" @click="openAddDialog">
          <v-icon start>mdi-plus</v-icon>
          Add Brand
        </v-btn>
      </div>
    </div>

    <!-- Add/Edit Brand Dialog -->
    <v-dialog v-model="dialogVisible" max-width="500" persistent>
      <v-card class="brand-dialog">
        <div class="dialog-header">
          <h3>{{ editingBrand ? "Edit Brand" : "Add New Brand" }}</h3>
          <v-btn icon variant="text" @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <v-card-text>
          <v-form ref="formRef" v-model="isValid">
            <div class="form-group">
              <label class="form-label required">Brand Name</label>
              <v-text-field
                v-model="form.name"
                placeholder="e.g., Coca-Cola, Samsung, Tuzo"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required]"
                hide-details="auto"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Description</label>
              <v-textarea
                v-model="form.description"
                placeholder="Brand description..."
                variant="outlined"
                rows="2"
                density="comfortable"
                hide-details="auto"
              />
            </div>

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

            <div class="form-group">
              <v-switch v-model="form.is_active" color="#2D6A4F" hide-details>
                <template #label>
                  <div>
                    <div class="switch-label">Active</div>
                    <div class="switch-hint">Brand visible in the system</div>
                  </div>
                </template>
              </v-switch>
            </div>
          </v-form>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="closeDialog">Cancel</v-btn>
          <v-btn
            color="#2D6A4F"
            :disabled="!isValid || submitting"
            :loading="submitting"
            @click="saveBrand"
          >
            {{ editingBrand ? "Update" : "Create" }} Brand
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
        <h3>Delete Brand?</h3>
        <p>
          Are you sure you want to delete "{{ brandToDelete?.name }}"?
          <br />
          <span class="text-caption text-medium-emphasis">
            Products using this brand will be affected.
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
const brands = ref([]);
const loading = ref(true);
const submitting = ref(false);
const deleting = ref(false);
const dialogVisible = ref(false);
const deleteDialog = ref(false);
const editingBrand = ref(null);
const brandToDelete = ref(null);
const searchQuery = ref("");
const statusFilter = ref("");
const isValid = ref(false);
const formRef = ref(null);

const form = ref({
  name: "",
  description: "",
  website: "",
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
const activeBrands = computed(() =>
  brands.value.filter((b) => b.is_active !== false)
);

const totalProducts = computed(() =>
  brands.value.reduce((sum, b) => sum + (b.product_count || 0), 0)
);

const filteredBrands = computed(() => {
  let filtered = [...brands.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (b) =>
        b.name.toLowerCase().includes(query) ||
        (b.description && b.description.toLowerCase().includes(query))
    );
  }

  if (statusFilter.value) {
    filtered = filtered.filter((b) => {
      if (statusFilter.value === "active") return b.is_active !== false;
      if (statusFilter.value === "inactive") return b.is_active === false;
      return true;
    });
  }

  return filtered;
});

// Methods
const filterBrands = () => {
  // Computed handles filtering
};

const resetFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
};

const openAddDialog = () => {
  editingBrand.value = null;
  resetForm();
  dialogVisible.value = true;
};

const editBrand = (brand: any) => {
  editingBrand.value = brand;
  form.value = {
    name: brand.name || "",
    description: brand.description || "",
    website: brand.website || "",
    is_active: brand.is_active !== false,
  };
  dialogVisible.value = true;
};

const resetForm = () => {
  form.value = {
    name: "",
    description: "",
    website: "",
    is_active: true,
  };
};

const closeDialog = () => {
  dialogVisible.value = false;
  resetForm();
};

const saveBrand = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  submitting.value = true;
  try {
    const brandData = {
      name: form.value.name,
      description: form.value.description || undefined,
      website: form.value.website || undefined,
      is_active: form.value.is_active,
    };

    await posStore.addBrand(brandData, editingBrand.value?.id);

    console.log("Brand data:", brandData);

    snackbar.value = {
      show: true,
      text: `Brand ${editingBrand.value ? "updated" : "created"} successfully!`,
      color: "success",
    };

    closeDialog();
    await loadBrands();
  } catch (error) {
    console.error("Error saving brand:", error);
    snackbar.value = {
      show: true,
      text: "Failed to save brand",
      color: "error",
    };
  } finally {
    submitting.value = false;
  }
};

const deleteBrand = (brand: any) => {
  brandToDelete.value = brand;
  deleteDialog.value = true;
};

const confirmDelete = async () => {
  deleting.value = true;
  try {
    // TODO: API Call
    // await $fetch(`/api/v1/brands/${brandToDelete.value.id}`, {
    //   method: 'DELETE',
    // });

    snackbar.value = {
      show: true,
      text: "Brand deleted successfully!",
      color: "success",
    };

    deleteDialog.value = false;
    await loadBrands();
  } catch (error) {
    console.error("Error deleting brand:", error);
    snackbar.value = {
      show: true,
      text: "Failed to delete brand",
      color: "error",
    };
  } finally {
    deleting.value = false;
  }
};

const loadBrands = async () => {
  loading.value = true;
  try {
    brands.value = await posStore.getAllBrands();
    // TODO: API Call
    // brands.value = await $fetch('/api/v1/brands');

    // Mock data
    // brands.value = [
    //   {
    //     id: "1",
    //     name: "Tuzo",
    //     description: "Kenyan dairy brand",
    //     website: "https://tuzo.co.ke",
    //     is_active: true,
    //     product_count: 5,
    //   },
    //   {
    //     id: "2",
    //     name: "Ajab",
    //     description: "Chapati flour brand",
    //     website: "https://ajab.co.ke",
    //     is_active: true,
    //     product_count: 3,
    //   },
    //   {
    //     id: "3",
    //     name: "Sawa",
    //     description: "Personal care brand",
    //     website: "https://sawa.co.ke",
    //     is_active: true,
    //     product_count: 4,
    //   },
    //   {
    //     id: "4",
    //     name: "Festive 20",
    //     description: "Bakery products",
    //     website: "",
    //     is_active: false,
    //     product_count: 2,
    //   },
    // ];
  } catch (error) {
    console.error("Error loading brands:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadBrands();
});
</script>

<style scoped>
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
</style>
