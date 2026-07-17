<!-- frontend/pages/admin/products.vue -->
<template>
  <div class="products-container">
    <!-- Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">Menu Management</div>
        <h1 class="page-title">Products</h1>
        <p class="page-subtitle">Manage your shop inventory items</p>
      </div>
      <v-btn class="add-product-btn" @click="navigateToAdd">
        <v-icon start>mdi-plus</v-icon>
        Add New Product
      </v-btn>
    </div>

    <!-- Stats Summary -->
    <div class="stats-summary">
      <div class="stat-item">
        <span class="stat-value">{{ products.length }}</span>
        <span class="stat-label">Total Products</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{ activeProducts.length }}</span>
        <span class="stat-label">Active</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{ productsWithVariants.length }}</span>
        <span class="stat-label">With Variants</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{ lowStockProducts.length }}</span>
        <span class="stat-label">Low Stock</span>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrapper">
        <v-icon class="search-icon">mdi-magnify</v-icon>
        <input
          v-model="searchQuery"
          placeholder="Search products..."
          class="search-input"
          @input="filterProducts"
        />
      </div>
      <div class="filter-group">
        <select
          v-model="selectedCategory"
          class="filter-select"
          @change="filterProducts"
        >
          <option value="">All Categories</option>
          <option v-for="cat in uniqueCategories" :key="cat" :value="cat">
            {{ cat }}
          </option>
        </select>
        <select
          v-model="stockFilter"
          class="filter-select"
          @change="filterProducts"
        >
          <option value="">All Stock</option>
          <option value="in_stock">In Stock</option>
          <option value="low_stock">Low Stock</option>
          <option value="out_of_stock">Out of Stock</option>
        </select>
        <select v-model="sortBy" class="filter-select" @change="filterProducts">
          <option value="name">Sort by Name</option>
          <option value="price-asc">Price: Low to High</option>
          <option value="price-desc">Price: High to Low</option>
          <option value="stock">Sort by Stock</option>
          <option value="newest">Newest First</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-grid">
      <v-skeleton-loader
        v-for="n in 6"
        :key="n"
        type="card"
        class="product-card-skeleton"
      />
    </div>

    <!-- Products Grid -->
    <div v-else class="products-grid">
      <div
        v-for="product in filteredProductsList"
        :key="product.id || product._id"
        class="product-card"
        @click="navigateToEdit(product)"
      >
        <div class="product-image-wrapper">
          <img
            :src="getProductImage(product)"
            :alt="product.name"
            class="product-image"
            @error="handleImageError($event, product)"
            @click.stop
          />
          <div class="stock-badge" :class="getStockStatusClass(product)">
            {{ getStockStatusText(product) }}
          </div>
          <div class="product-actions" @click.stop>
            <v-btn
              icon
              size="small"
              class="action-btn edit"
              @click="navigateToEdit(product)"
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
          <div class="product-header">
            <div
              class="product-category-badge"
              :class="getCategoryClass(product)"
            >
              {{ getCategoryName(product) }}
            </div>
            <div v-if="product.has_variants" class="variant-badge">
              <v-icon size="12">mdi-swap-horizontal</v-icon>
              {{ product.variants?.length || 0 }} variants
            </div>
          </div>
          <h3 class="product-name">{{ product.name }}</h3>
          <div class="product-sku" v-if="product.sku">
            SKU: {{ product.sku }}
          </div>
          <div class="product-price-section">
            <span class="product-price"
              >KSh {{ getProductPrice(product) }}</span
            >
            <span class="product-cost" v-if="getProductCost(product)">
              Cost: KSh {{ getProductCost(product) }}
            </span>
          </div>
          <div class="product-stats">
            <span class="stat">
              <v-icon size="14">mdi-package-variant</v-icon>
              {{ getProductStock(product) }} in stock
            </span>
            <span class="stat" v-if="product.reorder_level">
              <v-icon size="14">mdi-alert</v-icon>
              Reorder at {{ product.reorder_level }}
            </span>
          </div>
          <div class="product-tags" v-if="product.tags && product.tags.length">
            <span
              v-for="tag in product.tags.slice(0, 3)"
              :key="tag"
              class="tag"
            >
              #{{ tag }}
            </span>
            <span v-if="product.tags.length > 3" class="tag-more">
              +{{ product.tags.length - 3 }} more
            </span>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredProductsList.length === 0" class="empty-state">
        <v-icon size="64" color="#9CA3AF">mdi-package-variant</v-icon>
        <h3>No products found</h3>
        <p>Try adjusting your filters or add a new product</p>
        <v-btn color="#2D6A4F" @click="navigateToAdd">
          <v-icon start>mdi-plus</v-icon>
          Add Product
        </v-btn>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination-section" v-if="filteredProductsList.length > 0">
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        :total-visible="5"
        @update:model-value="filterProducts"
      />
      <span class="pagination-info">
        Showing {{ (currentPage - 1) * pageSize + 1 }} -
        {{ Math.min(currentPage * pageSize, filteredProductsList.length) }}
        of {{ filteredProductsList.length }} products
      </span>
    </div>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card class="delete-dialog">
        <div class="delete-icon">
          <v-icon size="60" color="#E07A5F">mdi-alert-circle</v-icon>
        </div>
        <h3>Delete Product?</h3>
        <p>
          Are you sure you want to delete "{{ productToDelete?.name }}"?
          <br /><span class="text-caption text-medium-emphasis"
            >This action cannot be undone.</span
          >
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
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { usePosStore } from "~/stores/pos";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const router = useRouter();
const store = usePosStore();

const loading = ref(true);
const deleting = ref(false);
const deleteDialog = ref(false);
const productToDelete = ref(null);
const searchQuery = ref("");
const selectedCategory = ref("");
const stockFilter = ref("");
const sortBy = ref("name");
const currentPage = ref(1);
const pageSize = ref(12);

const snackbar = ref({
  show: false,
  text: "",
  color: "success",
});

// Computed properties
const products = computed(() => store.products || []);

const activeProducts = computed(() =>
  products.value.filter((p) => p.is_active !== false)
);

const productsWithVariants = computed(() =>
  products.value.filter((p) => p.has_variants)
);

const lowStockProducts = computed(() =>
  products.value.filter((p) => {
    const stock = p.inventory?.available || p.inventory?.quantity || 0;
    const reorder = p.inventory?.reorder_level || 10;
    return stock <= reorder && stock > 0;
  })
);

const uniqueCategories = computed(() => {
  const cats = new Set();
  products.value.forEach((p) => {
    if (p.category_id) cats.add(p.category_id);
    if (p.tags) p.tags.forEach((t) => cats.add(t));
  });
  return Array.from(cats).slice(0, 20);
});

const filteredProductsList = ref([]);

const totalPages = computed(() =>
  Math.ceil(filteredProductsList.value.length / pageSize.value)
);

// Navigation methods
const navigateToAdd = () => {
  router.push("/admin/products/add");
};

const navigateToEdit = (product: any) => {
  const id = product._id || product.id;
  if (id) {
    router.push(`/admin/products/${id}`);
  } else {
    console.error("Product ID not found:", product);
    snackbar.value = {
      show: true,
      text: "Error: Product ID not found",
      color: "error",
    };
  }
};

// Helper methods
const getProductImage = (product: any) => {
  if (product.image_url) return product.image_url;
  if (product.media?.images?.length) return product.media.images[0].url;
  return "";
};

const handleImageError = (event: Event, product: any) => {
  const img = event.target as HTMLImageElement;
  img.src = "";
};

const getProductPrice = (product: any) => {
  return product.pricing?.selling_price || product.price || 0;
};

const getProductCost = (product: any) => {
  return product.pricing?.cost_price || 0;
};

const getProductStock = (product: any) => {
  return product.inventory?.available || product.inventory?.quantity || 0;
};

const getStockStatusClass = (product: any) => {
  const stock = getProductStock(product);
  const reorder = product.inventory?.reorder_level || 10;
  if (stock <= 0) return "out-of-stock";
  if (stock <= reorder) return "low-stock";
  return "in-stock";
};

const getStockStatusText = (product: any) => {
  const stock = getProductStock(product);
  const reorder = product.inventory?.reorder_level || 10;
  if (stock <= 0) return "Out of Stock";
  if (stock <= reorder) return "Low Stock";
  return "In Stock";
};

const getCategoryName = (product: any) => {
  if (product.category_id) return product.category_id;
  if (product.tags && product.tags.length > 0) return product.tags[0];
  return "Uncategorized";
};

const getCategoryClass = (product: any) => {
  const cat = getCategoryName(product).toLowerCase();
  const classes: Record<string, string> = {
    coffee: "coffee",
    tea: "tea",
    snack: "snack",
    rice: "rice",
    beans: "beans",
    oil: "oil",
    flour: "flour",
    bread: "bread",
    soap: "soap",
    dairy: "dairy",
  };
  return classes[cat] || "default";
};

// Filter products
const filterProducts = () => {
  let filtered = [...products.value];

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (p) =>
        p.name?.toLowerCase().includes(query) ||
        p.sku?.toLowerCase().includes(query) ||
        p.barcode?.includes(query)
    );
  }

  // Category filter
  if (selectedCategory.value) {
    filtered = filtered.filter(
      (p) =>
        p.category_id === selectedCategory.value ||
        p.tags?.includes(selectedCategory.value)
    );
  }

  // Stock filter
  if (stockFilter.value) {
    filtered = filtered.filter((p) => {
      const stock = getProductStock(p);
      const reorder = p.inventory?.reorder_level || 10;
      if (stockFilter.value === "in_stock") return stock > reorder;
      if (stockFilter.value === "low_stock")
        return stock <= reorder && stock > 0;
      if (stockFilter.value === "out_of_stock") return stock <= 0;
      return true;
    });
  }

  // Sort
  switch (sortBy.value) {
    case "name":
      filtered.sort((a, b) => (a.name || "").localeCompare(b.name || ""));
      break;
    case "price-asc":
      filtered.sort((a, b) => getProductPrice(a) - getProductPrice(b));
      break;
    case "price-desc":
      filtered.sort((a, b) => getProductPrice(b) - getProductPrice(a));
      break;
    case "stock":
      filtered.sort((a, b) => getProductStock(a) - getProductStock(b));
      break;
    case "newest":
      filtered.sort(
        (a, b) =>
          new Date(b.created_at || 0).getTime() -
          new Date(a.created_at || 0).getTime()
      );
      break;
  }

  // Paginate
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  filteredProductsList.value = filtered.slice(start, end);

  // Reset to page 1 if current page has no items
  if (filteredProductsList.value.length === 0 && currentPage.value > 1) {
    currentPage.value = 1;
    filterProducts();
  }
};

// Delete methods
const deleteProduct = (product: any) => {
  productToDelete.value = product;
  deleteDialog.value = true;
};

const confirmDelete = async () => {
  deleting.value = true;
  try {
    // TODO: Implement API call to delete product
    // await store.deleteProduct(productToDelete.value._id || productToDelete.value.id);

    snackbar.value = {
      show: true,
      text: "Product deleted successfully!",
      color: "success",
    };

    deleteDialog.value = false;
    await store.getAllProducts();
    filterProducts();
  } catch (error) {
    console.error("Error deleting product:", error);
    snackbar.value = {
      show: true,
      text: "Failed to delete product",
      color: "error",
    };
  } finally {
    deleting.value = false;
  }
};

// Watch for product changes
watch(
  () => store.products,
  () => {
    filterProducts();
  },
  { deep: true }
);

// Lifecycle
onMounted(async () => {
  loading.value = true;
  try {
    await store.getAllProducts();
    filterProducts();
  } catch (error) {
    console.error("Error loading products:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.products-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-badge {
  font-size: 12px;
  font-weight: 600;
  color: #e07a5f;
  text-transform: uppercase;
  letter-spacing: 2px;
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

.add-product-btn {
  background: linear-gradient(135deg, #1b4332, #2d6a4f);
  color: white;
  text-transform: none;
  border-radius: 40px;
  padding: 0 24px;
  height: 44px;
}

/* Stats Summary */
.stats-summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-item {
  background: white;
  padding: 16px 20px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 800;
  color: #1b4332;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
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
  flex-wrap: wrap;
}

.filter-select {
  padding: 10px 16px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
  cursor: pointer;
  font-size: 14px;
  min-width: 140px;
}

/* Products Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.product-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #e5e7eb;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  border-color: #2d6a4f;
}

.product-image-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: #f5f3ed;
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

.stock-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: white;
}

.stock-badge.in-stock {
  background: #2d6a4f;
}

.stock-badge.low-stock {
  background: #f4a261;
}

.stock-badge.out-of-stock {
  background: #e07a5f;
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

/* Show actions on mobile always */
@media (max-width: 768px) {
  .product-actions {
    opacity: 1;
  }
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
  padding: 16px 20px;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 8px;
}

.product-category-badge {
  display: inline-block;
  padding: 2px 12px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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

.product-category-badge.rice,
.product-category-badge.flour {
  background: #f4a26120;
  color: #f4a261;
}

.product-category-badge.beans {
  background: #8b5a2b20;
  color: #8b5a2b;
}

.product-category-badge.dairy {
  background: #4a90d920;
  color: #4a90d9;
}

.product-category-badge.bread {
  background: #d4a37320;
  color: #d4a373;
}

.product-category-badge.soap {
  background: #e8d5b720;
  color: #b8860b;
}

.product-category-badge.default {
  background: #e5e7eb;
  color: #6b7280;
}

.variant-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #6b7280;
}

.product-name {
  font-size: 16px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 4px;
}

.product-sku {
  font-size: 11px;
  color: #9ca3af;
  margin-bottom: 8px;
}

.product-price-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.product-price {
  font-size: 18px;
  font-weight: 800;
  color: #e07a5f;
}

.product-cost {
  font-size: 12px;
  color: #9ca3af;
}

.product-stats {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #6b7280;
  padding-top: 8px;
  border-top: 1px solid #f0ede5;
}

.stat {
  display: flex;
  align-items: center;
  gap: 4px;
}

.product-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}

.tag {
  font-size: 10px;
  color: #6b7280;
  background: #f0ede5;
  padding: 2px 10px;
  border-radius: 12px;
}

.tag-more {
  font-size: 10px;
  color: #9ca3af;
}

/* Empty State */
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-state h3 {
  margin-top: 16px;
  color: #1b4332;
  font-weight: 700;
}

.empty-state p {
  color: #6b7280;
  margin: 8px 0 20px;
}

/* Loading Grid */
.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* Pagination */
.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.pagination-info {
  font-size: 14px;
  color: #6b7280;
}

/* Delete Dialog */
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

/* Mobile Responsive */
@media (max-width: 768px) {
  .products-container {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .page-title {
    font-size: 24px;
  }

  .add-product-btn {
    width: 100%;
  }

  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-item {
    padding: 12px 16px;
  }

  .stat-value {
    font-size: 20px;
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
    min-width: unset;
  }

  .products-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .product-image-wrapper {
    height: 150px;
  }

  .product-details {
    padding: 12px 16px;
  }

  .pagination-section {
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 480px) {
  .stats-summary {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  .stat-item {
    padding: 8px 12px;
  }

  .stat-value {
    font-size: 16px;
  }

  .stat-label {
    font-size: 10px;
  }

  .product-name {
    font-size: 14px;
  }

  .product-price {
    font-size: 16px;
  }

  .product-card {
    border-radius: 16px;
  }

  .product-image-wrapper {
    height: 120px;
  }
}
</style>
