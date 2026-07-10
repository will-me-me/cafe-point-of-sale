<!-- pages/admin/products/categories/index.vue -->
<template>
  <div class="categories-container">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">
          <v-icon size="16" color="#E07A5F">mdi-folder</v-icon>
          Product Management
        </div>
        <h1 class="page-title">Categories</h1>
        <p class="page-subtitle">Manage hierarchical product categories</p>
      </div>
      <v-btn class="add-btn" @click="openAddDialog">
        <v-icon start>mdi-plus</v-icon>
        Add Category
      </v-btn>
    </div>

    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background: #2d6a4f20; color: #2d6a4f">
          <v-icon>mdi-folder</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ categories.length }}</div>
          <div class="stat-label">Total Categories</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: #2d6a4f20; color: #2d6a4f">
          <v-icon>mdi-folder-tree</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ parentCategories.length }}</div>
          <div class="stat-label">Parent Categories</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: #e07a5f20; color: #e07a5f">
          <v-icon>mdi-package-variant</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ totalProductsInCategories }}</div>
          <div class="stat-label">Products Categorized</div>
        </div>
      </div>
    </div>

    <!-- Search & Filters -->
    <div class="filters-bar">
      <div class="search-wrapper">
        <v-icon class="search-icon">mdi-magnify</v-icon>
        <input
          v-model="searchQuery"
          placeholder="Search categories..."
          class="search-input"
          @input="filterCategories"
        />
      </div>
      <div class="filter-group">
        <select
          v-model="parentFilter"
          class="filter-select"
          @change="filterCategories"
        >
          <option value="">All Categories</option>
          <option value="root">Root Categories</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
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
        class="category-card-skeleton"
      />
    </div>

    <!-- Categories Grid -->
    <div v-else class="categories-grid">
      <div
        v-for="category in filteredCategories"
        :key="category.id || category._id"
        class="category-card"
        :style="
          category.level > 0 ? `margin-left: ${category.level * 24}px;` : ''
        "
      >
        <div class="category-icon-wrapper">
          <div
            class="category-icon"
            :style="{ background: getCategoryColor(category) }"
          >
            <v-icon size="28" color="white">{{
              getCategoryIcon(category)
            }}</v-icon>
          </div>
        </div>
        <div class="category-details">
          <div class="category-header">
            <h3 class="category-name">{{ category.name }}</h3>
            <div class="category-actions">
              <v-btn
                icon
                size="small"
                class="action-btn edit"
                @click="editCategory(category)"
              >
                <v-icon size="16">mdi-pencil</v-icon>
              </v-btn>
              <v-btn
                icon
                size="small"
                class="action-btn add-child"
                @click="openAddDialog(category)"
              >
                <v-icon size="16">mdi-plus</v-icon>
              </v-btn>
              <v-btn
                icon
                size="small"
                class="action-btn delete"
                @click="deleteCategory(category)"
              >
                <v-icon size="16">mdi-delete</v-icon>
              </v-btn>
            </div>
          </div>
          <div class="category-meta">
            <span class="category-level">
              <v-icon size="14">mdi-folder-outline</v-icon>
              Level {{ category.level || 0 }}
            </span>
            <span class="category-products">
              <v-icon size="14">mdi-package-variant</v-icon>
              {{ category.product_count || 0 }} products
            </span>
            <v-chip
              :color="category.is_active !== false ? '#2D6A4F' : '#E07A5F'"
              size="x-small"
              text-color="white"
            >
              {{ category.is_active !== false ? "Active" : "Inactive" }}
            </v-chip>
          </div>
          <div v-if="category.description" class="category-description">
            {{ category.description }}
          </div>
          <div
            v-if="getChildren(category.id).length > 0"
            class="category-children"
          >
            <span class="children-label">Sub-categories:</span>
            <span
              v-for="child in getChildren(category.id)"
              :key="child.id"
              class="child-tag"
            >
              {{ child.name }}
            </span>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredCategories.length === 0" class="empty-state">
        <v-icon size="64" color="#9CA3AF">mdi-folder-off</v-icon>
        <h3>No categories found</h3>
        <p>Try adjusting your search or add a new category</p>
        <v-btn color="#2D6A4F" @click="openAddDialog">
          <v-icon start>mdi-plus</v-icon>
          Add Category
        </v-btn>
      </div>
    </div>

    <!-- Add/Edit Category Dialog -->
    <v-dialog v-model="dialogVisible" max-width="500" persistent>
      <v-card class="category-dialog">
        <div class="dialog-header">
          <h3>{{ editingCategory ? "Edit Category" : "Add New Category" }}</h3>
          <v-btn icon variant="text" @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <v-card-text>
          <v-form ref="formRef" v-model="isValid">
            <div class="form-group">
              <label class="form-label required">Category Name</label>
              <v-text-field
                v-model="form.name"
                placeholder="e.g., Beverages, Electronics, Clothing"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required]"
                hide-details="auto"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Parent Category</label>
              <v-select
                v-model="form.parent_id"
                :items="parentCategoryOptions"
                placeholder="Select parent category (optional)"
                variant="outlined"
                density="comfortable"
                hide-details="auto"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Description</label>
              <v-textarea
                v-model="form.description"
                placeholder="Category description..."
                variant="outlined"
                rows="2"
                density="comfortable"
                hide-details="auto"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Icon</label>
              <v-text-field
                v-model="form.icon"
                placeholder="e.g., mdi-coffee, mdi-food, mdi-phone"
                variant="outlined"
                density="comfortable"
                hide-details="auto"
              />
              <div class="input-hint">Enter a Material Design icon name</div>
            </div>

            <div class="form-group">
              <v-switch v-model="form.is_active" color="#2D6A4F" hide-details>
                <template #label>
                  <div>
                    <div class="switch-label">Active</div>
                    <div class="switch-hint">
                      Category visible in the system
                    </div>
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
            @click="saveCategory"
          >
            {{ editingCategory ? "Update" : "Create" }} Category
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
        <h3>Delete Category?</h3>
        <p>
          Are you sure you want to delete "{{ categoryToDelete?.name }}"?
          <br />
          <span class="text-caption text-medium-emphasis">
            {{ getChildren(categoryToDelete?.id).length }} sub-categories and
            {{ categoryToDelete?.product_count || 0 }} products will be
            affected.
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
const categories = ref([]);
const loading = ref(true);
const submitting = ref(false);
const deleting = ref(false);
const dialogVisible = ref(false);
const deleteDialog = ref(false);
const editingCategory = ref(null);
const categoryToDelete = ref(null);
const searchQuery = ref("");
const parentFilter = ref("");
const isValid = ref(false);
const formRef = ref(null);

const form = ref({
  name: "",
  parent_id: null,
  description: "",
  icon: "mdi-folder",
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
const parentCategories = computed(() =>
  categories.value.filter((c) => !c.parent_id)
);

const totalProductsInCategories = computed(() =>
  categories.value.reduce((sum, c) => sum + (c.product_count || 0), 0)
);

const parentCategoryOptions = computed(() => {
  const options = [{ title: "None (Root Category)", value: null }];
  categories.value.forEach((c) => {
    options.push({ title: c.name, value: c.id || c._id });
  });
  return options;
});

const filteredCategories = computed(() => {
  let filtered = [...categories.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (c) =>
        c.name.toLowerCase().includes(query) ||
        (c.description && c.description.toLowerCase().includes(query))
    );
  }

  if (parentFilter.value) {
    if (parentFilter.value === "root") {
      filtered = filtered.filter((c) => !c.parent_id);
    } else {
      filtered = filtered.filter((c) => c.parent_id === parentFilter.value);
    }
  }

  return filtered;
});

// Methods
const filterCategories = () => {
  // Computed handles filtering
};

const resetFilters = () => {
  searchQuery.value = "";
  parentFilter.value = "";
};

const getCategoryIcon = (category: any) => {
  return category.icon || "mdi-folder";
};

const getCategoryColor = (category: any) => {
  const colors = [
    "#2D6A4F",
    "#E07A5F",
    "#F4A261",
    "#6B4E71",
    "#4A90D9",
    "#E9C46A",
    "#2A9D8F",
    "#E76F51",
  ];
  const index = (category.name?.length || 0) % colors.length;
  return colors[index];
};

const getChildren = (categoryId: string) => {
  return categories.value.filter((c) => c.parent_id === categoryId);
};

const openAddDialog = (parentCategory = null) => {
  editingCategory.value = null;
  resetForm();
  if (parentCategory) {
    form.value.parent_id = parentCategory.id || parentCategory._id;
  }
  dialogVisible.value = true;
};

const editCategory = (category: any) => {
  editingCategory.value = category;
  form.value = {
    name: category.name || "",
    parent_id: category.parent_id || null,
    description: category.description || "",
    icon: category.icon || "mdi-folder",
    is_active: category.is_active !== false,
  };
  dialogVisible.value = true;
};

const resetForm = () => {
  form.value = {
    name: "",
    parent_id: null,
    description: "",
    icon: "mdi-folder",
    is_active: true,
  };
};

const closeDialog = () => {
  dialogVisible.value = false;
  resetForm();
};

const saveCategory = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  submitting.value = true;
  try {
    const categoryData = {
      name: form.value.name,
      parent_id: form.value.parent_id || undefined,
      description: form.value.description || undefined,
      icon: form.value.icon || "mdi-folder",
      is_active: form.value.is_active,
    };

    console.log("Category data:", categoryData);
    await posStore.addCategory(categoryData);

    snackbar.value = {
      show: true,
      text: `Category ${
        editingCategory.value ? "updated" : "created"
      } successfully!`,
      color: "success",
    };

    closeDialog();
    await loadCategories();
  } catch (error) {
    console.error("Error saving category:", error);
    snackbar.value = {
      show: true,
      text: "Failed to save category",
      color: "error",
    };
  } finally {
    submitting.value = false;
  }
};

const deleteCategory = (category: any) => {
  categoryToDelete.value = category;
  deleteDialog.value = true;
};

const confirmDelete = async () => {
  deleting.value = true;
  try {
    snackbar.value = {
      show: true,
      text: "Category deleted successfully!",
      color: "success",
    };

    deleteDialog.value = false;
    await loadCategories();
  } catch (error) {
    console.error("Error deleting category:", error);
    snackbar.value = {
      show: true,
      text: "Failed to delete category",
      color: "error",
    };
  } finally {
    deleting.value = false;
  }
};

const loadCategories = async () => {
  loading.value = true;
  try {
    // TODO: API Call
    categories.value = await posStore.getAllCategories();
    // categories.value = [
    //   {
    //     id: "1",
    //     name: "Beverages",
    //     description: "Drinks and beverages",
    //     parent_id: null,
    //     level: 0,
    //     icon: "mdi-drink",
    //     is_active: true,
    //     product_count: 10,
    //   },
    //   {
    //     id: "2",
    //     name: "Soft Drinks",
    //     description: "Carbonated drinks",
    //     parent_id: "1",
    //     level: 1,
    //     icon: "mdi-bottle-soda",
    //     is_active: true,
    //     product_count: 6,
    //   },
    //   {
    //     id: "3",
    //     name: "Dairy",
    //     description: "Milk and dairy products",
    //     parent_id: null,
    //     level: 0,
    //     icon: "mdi-cow",
    //     is_active: true,
    //     product_count: 8,
    //   },
    // ];
  } catch (error) {
    console.error("Error loading categories:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadCategories();
});
</script>

<style scoped>
.categories-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Use same styles as brands with category-specific additions */
.category-card {
  background: white;
  border-radius: 16px;
  padding: 16px 20px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 12px;
}

.category-card:hover {
  transform: translateX(4px);
  border-color: #2d6a4f;
}

.category-icon-wrapper {
  flex-shrink: 0;
}

.category-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.category-details {
  flex: 1;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 8px;
}

.category-name {
  font-size: 16px;
  font-weight: 700;
  color: #1b4332;
  margin: 0;
}

.category-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
  flex-wrap: wrap;
}

.category-level,
.category-products {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #6b7280;
}

.category-description {
  font-size: 13px;
  color: #6b7280;
  margin-top: 4px;
}

.category-children {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.children-label {
  font-size: 12px;
  color: #6b7280;
}

.child-tag {
  font-size: 11px;
  padding: 2px 12px;
  background: #f0ede5;
  border-radius: 12px;
  color: #1b4332;
}

/* Responsive */
@media (max-width: 768px) {
  .categories-container {
    padding: 16px;
  }

  .category-card {
    flex-direction: column;
    align-items: stretch;
    margin-left: 0 !important;
  }

  .category-header {
    flex-direction: column;
  }

  .category-actions {
    align-self: flex-start;
    margin-top: 8px;
  }

  .category-meta {
    flex-wrap: wrap;
  }
}

/* Reuse other styles from brands page */
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
