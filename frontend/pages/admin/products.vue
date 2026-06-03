<!-- frontend/pages/admin/products.vue -->
<template>
  <div class="products-container">
    <!-- Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">Menu Management</div>
        <h1 class="page-title">Products</h1>
        <p class="page-subtitle">Manage your coffee shop menu items</p>
      </div>
      <v-btn class="add-product-btn" @click="openAddDialog">
        <v-icon start>mdi-plus</v-icon>
        Add New Product
      </v-btn>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrapper">
        <v-icon class="search-icon">mdi-magnify</v-icon>
        <input
          v-model="searchQuery"
          placeholder="Search products..."
          class="search-input"
        />
      </div>
      <div class="filter-group">
        <select v-model="selectedCategory" class="filter-select">
          <option value="">All Categories</option>
          <option value="coffee">☕ Coffee</option>
          <option value="tea">🫖 Tea</option>
          <option value="snack">🍪 Snack</option>
        </select>
        <select v-model="sortBy" class="filter-select">
          <option value="name">Sort by Name</option>
          <option value="price-asc">Price: Low to High</option>
          <option value="price-desc">Price: High to Low</option>
        </select>
      </div>
    </div>

    <!-- Products Grid -->
    <div class="products-grid">
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="product-card"
      >
        <div class="product-image-wrapper">
          <img
            :src="product.image_url || '/coffee-placeholder.jpg'"
            :alt="product.name"
            class="product-image"
          />
          <div class="product-actions">
            <v-btn
              icon
              size="small"
              class="action-btn edit"
              @click="editProduct(product)"
            >
              <v-icon size="18">mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              size="small"
              class="action-btn delete"
              @click="deleteProduct(product)"
            >
              <v-icon size="18">mdi-delete</v-icon>
            </v-btn>
          </div>
        </div>
        <div class="product-details">
          <div class="product-category-badge" :class="product.category">
            {{ product.category }}
          </div>
          <h3 class="product-name">{{ product.name }}</h3>
          <div class="product-price">${{ product.price }}</div>
          <div class="product-stats">
            <span class="stat">
              <v-icon size="14">mdi-chart-line</v-icon>
              {{ product.sales || 0 }} sold
            </span>
            <span class="stat">
              <v-icon size="14">mdi-star</v-icon>
              {{ product.rating || 4.5 }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Product Dialog -->
    <v-dialog v-model="dialogVisible" max-width="600">
      <v-card class="product-form-dialog">
        <div class="dialog-header">
          <h2>{{ editingProduct ? "Edit Product" : "Add New Product" }}</h2>
          <v-btn icon variant="text" @click="dialogVisible = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <v-card-text>
          <v-form ref="formRef" v-model="isValid">
            <div class="form-group">
              <label>Product Name</label>
              <v-text-field
                v-model="form.name"
                placeholder="e.g., Caramel Macchiato"
                variant="outlined"
                :rules="[rules.required]"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Price</label>
                <v-text-field
                  v-model="form.price"
                  placeholder="0.00"
                  type="number"
                  prefix="$"
                  variant="outlined"
                  :rules="[rules.required, rules.positive]"
                />
              </div>

              <div class="form-group">
                <label>Category</label>
                <v-select
                  v-model="form.category"
                  :items="categoryOptions"
                  variant="outlined"
                  :rules="[rules.required]"
                />
              </div>
            </div>

            <div class="form-group">
              <label>Product Image</label>
              <div class="image-upload-area" @click="triggerFileInput">
                <input
                  ref="fileInput"
                  type="file"
                  accept="image/*"
                  hidden
                  @change="handleImageUpload"
                />
                <div v-if="imagePreview" class="image-preview">
                  <img :src="imagePreview" alt="Preview" />
                  <div class="image-overlay">
                    <v-icon size="30">mdi-camera</v-icon>
                    <span>Change Image</span>
                  </div>
                </div>
                <div v-else class="upload-placeholder">
                  <v-icon size="48" color="#9CA3AF">mdi-image-plus</v-icon>
                  <p>Click to upload product image</p>
                  <span>PNG, JPG up to 5MB</span>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Description (Optional)</label>
              <v-textarea
                v-model="form.description"
                placeholder="Describe your product..."
                variant="outlined"
                rows="3"
              />
            </div>
          </v-form>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="dialogVisible = false">Cancel</v-btn>
          <v-btn color="#2D6A4F" :disabled="!isValid" @click="saveProduct">
            {{ editingProduct ? "Update" : "Create" }} Product
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
        <h3>Delete Product?</h3>
        <p>
          Are you sure you want to delete "{{ productToDelete?.name }}"? This
          action cannot be undone.
        </p>
        <div class="delete-actions">
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="#E07A5F" @click="confirmDelete">Delete</v-btn>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { usePosStore } from "~/stores/pos";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const store = usePosStore();
const dialogVisible = ref(false);
const deleteDialog = ref(false);
const editingProduct = ref(null);
const productToDelete = ref(null);
const searchQuery = ref("");
const selectedCategory = ref("");
const sortBy = ref("name");
const isValid = ref(false);
const formRef = ref(null);
const fileInput = ref(null);
const imagePreview = ref("");

const form = ref({
  name: "",
  price: "",
  category: "",
  description: "",
  file: null,
});

const rules = {
  required: (v: any) => !!v || "This field is required",
  positive: (v: number) => v > 0 || "Price must be positive",
};

const categoryOptions = [
  { title: "☕ Coffee", value: "coffee" },
  { title: "🫖 Tea", value: "tea" },
  { title: "🍪 Snack", value: "snack" },
];

const filteredProducts = computed(() => {
  let products = [...store.products];

  if (searchQuery.value) {
    products = products.filter((p) =>
      p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  if (selectedCategory.value) {
    products = products.filter((p) => p.category === selectedCategory.value);
  }

  if (sortBy.value === "name") {
    products.sort((a, b) => a.name.localeCompare(b.name));
  } else if (sortBy.value === "price-asc") {
    products.sort((a, b) => a.price - b.price);
  } else if (sortBy.value === "price-desc") {
    products.sort((a, b) => b.price - a.price);
  }

  return products;
});

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    form.value.file = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target?.result;
    };
    reader.readAsDataURL(file);
  }
};

const openAddDialog = () => {
  editingProduct.value = null;
  form.value = {
    name: "",
    price: "",
    category: "",
    description: "",
    file: null,
  };
  imagePreview.value = "";
  dialogVisible.value = true;
};

const editProduct = (product) => {
  editingProduct.value = product;
  form.value = {
    name: product.name,
    price: product.price,
    category: product.category,
    description: product.description || "",
    file: null,
  };
  imagePreview.value = product.image_url;
  dialogVisible.value = true;
};

const saveProduct = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  // Save logic here
  dialogVisible.value = false;
};

const deleteProduct = (product) => {
  productToDelete.value = product;
  deleteDialog.value = true;
};

const confirmDelete = async () => {
  // Delete logic here
  deleteDialog.value = false;
};

onMounted(async () => {
  await store.getAllProducts();
});
</script>

<style scoped>
.products-container {
  padding: 32px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
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

.add-product-btn {
  background: linear-gradient(135deg, #1b4332, #2d6a4f);
  color: white;
  text-transform: none;
  border-radius: 40px;
  padding: 0 24px;
}

.filters-bar {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.search-wrapper {
  flex: 1;
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
}

.filter-select {
  padding: 8px 16px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
  cursor: pointer;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.product-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.product-image-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.product-actions {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .product-actions {
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

.product-details {
  padding: 20px;
}

.product-category-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.product-category-badge.coffee {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.product-category-badge.tea {
  background: #6b4e7120;
  color: #6b4e71;
}

.product-category-badge.snack {
  background: #e07a5f20;
  color: #e07a5f;
}

.product-name {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 8px;
}

.product-price {
  font-size: 20px;
  font-weight: 800;
  color: #e07a5f;
  margin-bottom: 12px;
}

.product-stats {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #6b7280;
}

.stat {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Dialog Styles */
.product-form-dialog {
  border-radius: 32px !important;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
}

.dialog-header h2 {
  font-family: "Playfair Display", serif;
  font-size: 24px;
  font-weight: 700;
  color: #1b4332;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.image-upload-area {
  border: 2px dashed #e5e7eb;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.image-upload-area:hover {
  border-color: #2d6a4f;
  background: rgba(45, 106, 79, 0.05);
}

.image-preview {
  position: relative;
  height: 200px;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-preview:hover .image-overlay {
  opacity: 1;
}

.upload-placeholder {
  padding: 48px;
  text-align: center;
}

.upload-placeholder p {
  margin-top: 12px;
  color: #374151;
}

.upload-placeholder span {
  font-size: 12px;
  color: #9ca3af;
}

.dialog-actions {
  padding: 16px 24px 24px;
  gap: 12px;
}

.delete-dialog {
  text-align: center;
  padding: 32px;
  border-radius: 32px;
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
</style>
