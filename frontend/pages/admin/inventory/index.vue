<!-- pages/admin/inventory/index.vue -->
<template>
  <div class="inventory-container">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#E07A5F">mdi-warehouse</v-icon>
          Inventory Management
        </div>
        <h1 class="page-title">Stock Overview</h1>
        <p class="page-subtitle">
          View and manage current stock levels for all products
        </p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right mt-4 mt-md-0">
        <v-btn
          variant="outlined"
          color="#2D6A4F"
          @click="exportInventory"
          class="mr-2"
        >
          <v-icon start>mdi-download</v-icon>
          Export
        </v-btn>
        <v-btn color="#2D6A4F" @click="refreshInventory" :loading="loading">
          <v-icon start>mdi-refresh</v-icon>
          Refresh
        </v-btn>
      </v-col>
    </v-row>

    <!-- Stats Summary -->
    <v-row class="stats-grid" no-gutters>
      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card class="stat-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon"
                  style="background: #2d6a4f20; color: #2d6a4f"
                >
                  <v-icon size="24">mdi-package-variant</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ totalProducts }}</div>
                <div class="stat-label">Total Products</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card class="stat-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon"
                  style="background: #2d6a4f20; color: #2d6a4f"
                >
                  <v-icon size="24">mdi-check-circle</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ inStockCount }}</div>
                <div class="stat-label">In Stock</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card
          class="stat-card"
          elevation="0"
          rounded="xl"
          @click="navigateTo('/admin/inventory/low-stock')"
          style="cursor: pointer"
        >
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon"
                  style="background: #f4a26120; color: #f4a261"
                >
                  <v-icon size="24">mdi-alert</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value" style="color: #f4a261">
                  {{ lowStockCount }}
                </div>
                <div class="stat-label">Low Stock</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card
          class="stat-card"
          elevation="0"
          rounded="xl"
          @click="navigateTo('/admin/inventory/out-of-stock')"
          style="cursor: pointer"
        >
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon"
                  style="background: #e07a5f20; color: #e07a5f"
                >
                  <v-icon size="24">mdi-close-circle</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value" style="color: #e07a5f">
                  {{ outOfStockCount }}
                </div>
                <div class="stat-label">Out of Stock</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Filters -->
    <v-card class="filters-card mb-4" elevation="0" rounded="xl">
      <v-card-text class="pa-4">
        <v-row no-gutters>
          <v-col cols="12" md="5" class="pr-md-4">
            <div class="search-wrapper">
              <v-icon class="search-icon">mdi-magnify</v-icon>
              <input
                v-model="searchQuery"
                placeholder="Search products..."
                class="search-input"
                @input="filterInventory"
              />
            </div>
          </v-col>
          <v-col cols="12" md="7">
            <v-row no-gutters class="filter-group">
              <v-col cols="6" sm="4" class="pr-1">
                <select
                  v-model="categoryFilter"
                  class="filter-select"
                  @change="filterInventory"
                >
                  <option value="">All Categories</option>
                  <option
                    v-for="cat in uniqueCategories"
                    :key="cat"
                    :value="cat"
                  >
                    {{ cat }}
                  </option>
                </select>
              </v-col>
              <v-col cols="6" sm="4" class="px-1">
                <select
                  v-model="stockStatusFilter"
                  class="filter-select"
                  @change="filterInventory"
                >
                  <option value="">All Stock</option>
                  <option value="in_stock">In Stock</option>
                  <option value="low_stock">Low Stock</option>
                  <option value="out_of_stock">Out of Stock</option>
                </select>
              </v-col>
              <v-col cols="12" sm="4" class="pl-1">
                <v-btn
                  color="#2D6A4F"
                  variant="tonal"
                  size="small"
                  block
                  @click="resetFilters"
                >
                  <v-icon start size="16">mdi-close</v-icon>
                  Reset
                </v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Loading State -->
    <div v-if="loading" class="loading-grid">
      <v-skeleton-loader
        v-for="n in 8"
        :key="n"
        type="card"
        class="inventory-skeleton"
      />
    </div>

    <!-- Inventory Table -->
    <div v-else>
      <v-card class="inventory-table-card" elevation="0" rounded="xl">
        <v-card-text class="pa-0">
          <v-data-table
            :headers="headers"
            :items="filteredInventory"
            :loading="loading"
            :items-per-page="itemsPerPage"
            :page="currentPage"
            @update:page="currentPage = $event"
            @update:items-per-page="itemsPerPage = $event"
            class="inventory-table"
            item-value="id"
          >
            <template v-slot:item.name="{ item }">
              <div class="product-info">
                <div class="product-avatar">
                  <v-img
                    :src="item.image_url || ''"
                    width="40"
                    height="40"
                    cover
                    class="rounded"
                  />
                </div>
                <div>
                  <div class="product-name">{{ item.name }}</div>
                  <div v-if="item.has_variants" class="product-variants">
                    <v-icon size="12">mdi-swap-horizontal</v-icon>
                    {{ item.variants?.length || 0 }} variants
                  </div>
                </div>
              </div>
            </template>

            <template v-slot:item.sku="{ item }">
              <span class="text-caption">{{ item.sku || "-" }}</span>
            </template>

            <template v-slot:item.category_id="{ item }">
              <span class="category-tag">{{
                item.category_id || "Uncategorized"
              }}</span>
            </template>

            <template v-slot:item.stock="{ item }">
              <span :class="getStockClass(item)">{{ getStock(item) }}</span>
            </template>

            <template v-slot:item.reorder_level="{ item }">
              {{ item.inventory?.reorder_level || 10 }}
            </template>

            <template v-slot:item.status="{ item }">
              <v-chip
                :color="getStatusColor(item)"
                size="x-small"
                text-color="white"
              >
                {{ getStatusText(item) }}
              </v-chip>
            </template>

            <template v-slot:item.actions="{ item }">
              <v-btn
                icon
                size="small"
                variant="text"
                color="#2D6A4F"
                @click="viewProduct(item)"
              >
                <v-icon size="18">mdi-eye</v-icon>
              </v-btn>
              <v-btn
                icon
                size="small"
                variant="text"
                color="#2D6A4F"
                @click="adjustStock(item)"
              >
                <v-icon size="18">mdi-pencil</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </div>

    <!-- Adjust Stock Dialog -->
    <v-dialog v-model="adjustDialog.show" max-width="500" persistent>
      <v-card class="adjust-dialog">
        <v-card-title class="dialog-header">
          <div>
            <div class="dialog-title font-weight-bold">Adjust Stock</div>
            <div class="dialog-subtitle text-caption text-medium-emphasis">
              Update inventory quantity
            </div>
          </div>
          <v-btn icon variant="text" @click="adjustDialog.show = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-form ref="adjustFormRef" v-model="adjustValid">
            <div class="product-preview" v-if="adjustDialog.product">
              <v-row align="center" no-gutters>
                <v-col cols="auto">
                  <v-img
                    :src="adjustDialog.product.image_url || ''"
                    width="48"
                    height="48"
                    cover
                    class="rounded"
                  />
                </v-col>
                <v-col class="pl-3">
                  <div class="preview-name">
                    {{ adjustDialog.product.name }}
                  </div>
                  <div class="preview-sku">
                    SKU: {{ adjustDialog.product.sku }}
                  </div>
                  <div class="preview-current">
                    Current Stock:
                    <strong>{{ getStock(adjustDialog.product) }}</strong>
                  </div>
                </v-col>
              </v-row>
            </div>

            <div class="form-group mt-4">
              <label class="form-label required">Adjustment Type</label>
              <v-select
                v-model="adjustForm.type"
                :items="adjustmentTypes"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required]"
                hide-details="auto"
              />
            </div>

            <div class="form-group">
              <label class="form-label required">Quantity</label>
              <v-text-field
                v-model="adjustForm.quantity"
                type="number"
                placeholder="0"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required, rules.positive]"
                hide-details="auto"
              />
              <div class="input-hint text-caption text-medium-emphasis">
                {{
                  adjustForm.type === "add"
                    ? "Add to stock"
                    : "Remove from stock"
                }}
              </div>
            </div>

            <div class="form-group">
              <label class="form-label required">Reason</label>
              <v-text-field
                v-model="adjustForm.reason"
                placeholder="e.g., Physical count, Damaged items, Customer return"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required]"
                hide-details="auto"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Notes</label>
              <v-textarea
                v-model="adjustForm.notes"
                placeholder="Additional notes..."
                variant="outlined"
                rows="2"
                density="comfortable"
                hide-details="auto"
              />
            </div>
          </v-form>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="adjustDialog.show = false"
            >Cancel</v-btn
          >
          <v-btn
            color="#2D6A4F"
            :disabled="!adjustValid || adjustSubmitting"
            :loading="adjustSubmitting"
            @click="submitAdjustment"
          >
            Confirm Adjustment
          </v-btn>
        </v-card-actions>
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
import { usePosStore } from "~/stores/pos";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const store = usePosStore();
const loading = ref(false);
const searchQuery = ref("");
const categoryFilter = ref("");
const stockStatusFilter = ref("");
const currentPage = ref(1);
const itemsPerPage = ref(10);
const adjustSubmitting = ref(false);
const adjustValid = ref(false);
const adjustFormRef = ref(null);

const adjustDialog = ref({
  show: false,
  product: null,
});

const adjustForm = ref({
  type: "add",
  quantity: "",
  reason: "",
  notes: "",
});

const snackbar = ref({
  show: false,
  text: "",
  color: "success",
  icon: "mdi-check-circle",
});

// Rules
const rules = {
  required: (v: any) => !!v || "This field is required",
  positive: (v: number) => v > 0 || "Quantity must be greater than 0",
};

const adjustmentTypes = [
  { title: "Add Stock", value: "add" },
  { title: "Remove Stock", value: "remove" },
  { title: "Damaged", value: "damage" },
  { title: "Expired", value: "expired" },
  { title: "Returned", value: "returned" },
];

// Table Headers
const headers = [
  { title: "Product", key: "name", sortable: true },
  { title: "SKU", key: "sku", sortable: true },
  { title: "Category", key: "category_id", sortable: true },
  { title: "Stock", key: "stock", sortable: true },
  { title: "Reorder Level", key: "reorder_level", sortable: true },
  { title: "Status", key: "status", sortable: true },
  { title: "Actions", key: "actions", sortable: false },
];

// Computed
const products = computed(() => store.products || []);

const totalProducts = computed(() => products.value.length);

const getStock = (item: any) => {
  return item.inventory?.available || item.inventory?.quantity || 0;
};

const inStockCount = computed(() => {
  return products.value.filter((item) => getStock(item) > 0).length;
});

const lowStockCount = computed(() => {
  return products.value.filter((item) => {
    const stock = getStock(item);
    const reorder = item.inventory?.reorder_level || 10;
    return stock > 0 && stock <= reorder;
  }).length;
});

const outOfStockCount = computed(() => {
  return products.value.filter((item) => getStock(item) <= 0).length;
});

const uniqueCategories = computed(() => {
  const cats = new Set();
  products.value.forEach((item) => {
    if (item.category_id) cats.add(item.category_id);
    if (item.tags) item.tags.forEach((t) => cats.add(t));
  });
  return Array.from(cats);
});

const filteredInventory = computed(() => {
  let filtered = [...products.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (item) =>
        item.name.toLowerCase().includes(query) ||
        (item.sku && item.sku.toLowerCase().includes(query)) ||
        (item.barcode && item.barcode.includes(query))
    );
  }

  if (categoryFilter.value) {
    filtered = filtered.filter(
      (item) =>
        item.category_id === categoryFilter.value ||
        (item.tags && item.tags.includes(categoryFilter.value))
    );
  }

  if (stockStatusFilter.value) {
    filtered = filtered.filter((item) => {
      const stock = getStock(item);
      const reorder = item.inventory?.reorder_level || 10;
      if (stockStatusFilter.value === "in_stock") return stock > reorder;
      if (stockStatusFilter.value === "low_stock")
        return stock > 0 && stock <= reorder;
      if (stockStatusFilter.value === "out_of_stock") return stock <= 0;
      return true;
    });
  }

  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filtered.slice(start, end);
});

// Helper Methods
const getStockClass = (item: any) => {
  const stock = getStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  if (stock <= 0) return "stock-out";
  if (stock <= reorder) return "stock-low";
  return "stock-ok";
};

const getStatusColor = (item: any) => {
  const stock = getStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  if (stock <= 0) return "#E07A5F";
  if (stock <= reorder) return "#F4A261";
  return "#2D6A4F";
};

const getStatusText = (item: any) => {
  const stock = getStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  if (stock <= 0) return "Out of Stock";
  if (stock <= reorder) return "Low Stock";
  return "In Stock";
};

// Actions
const filterInventory = () => {
  // Computed handles filtering
};

const resetFilters = () => {
  searchQuery.value = "";
  categoryFilter.value = "";
  stockStatusFilter.value = "";
  currentPage.value = 1;
};

const viewProduct = (product: any) => {
  navigateTo(`/admin/products/${product.id || product._id}`);
};

const adjustStock = (product: any) => {
  adjustDialog.value = {
    show: true,
    product: product,
  };
  adjustForm.value = {
    type: "add",
    quantity: "",
    reason: "",
    notes: "",
  };
  adjustValid.value = false;
};

const submitAdjustment = async () => {
  const { valid } = await adjustFormRef.value.validate();
  if (!valid) return;

  adjustSubmitting.value = true;
  try {
    const data = {
      product_id:
        adjustDialog.value.product.id || adjustDialog.value.product._id,
      type: adjustForm.value.type,
      quantity: parseInt(adjustForm.value.quantity),
      reason: adjustForm.value.reason,
      notes: adjustForm.value.notes,
    };

    // TODO: API Call to adjust stock
    // await $fetch('/api/v1/inventory/adjust', {
    //   method: 'POST',
    //   body: data,
    // })

    console.log("Adjustment data:", data);

    snackbar.value = {
      show: true,
      text: `Stock ${
        adjustForm.value.type === "add" ? "added" : "removed"
      } successfully!`,
      color: "success",
      icon: "mdi-check-circle",
    };

    adjustDialog.value.show = false;
    await refreshInventory();
  } catch (error) {
    console.error("Error adjusting stock:", error);
    snackbar.value = {
      show: true,
      text: "Failed to adjust stock",
      color: "error",
      icon: "mdi-alert-circle",
    };
  } finally {
    adjustSubmitting.value = false;
  }
};

const refreshInventory = async () => {
  loading.value = true;
  try {
    await store.getAllProducts();
  } catch (error) {
    console.error("Error loading inventory:", error);
    snackbar.value = {
      show: true,
      text: "Failed to load inventory",
      color: "error",
      icon: "mdi-alert-circle",
    };
  } finally {
    loading.value = false;
  }
};

const exportInventory = () => {
  const data = products.value.map((item) => ({
    name: item.name,
    sku: item.sku,
    category: item.category_id,
    stock: getStock(item),
    reorderLevel: item.inventory?.reorder_level || 10,
    status: getStatusText(item),
    costPrice: item.pricing?.cost_price || 0,
    sellingPrice: item.pricing?.selling_price || 0,
  }));

  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `inventory_${new Date().toISOString().split("T")[0]}.json`;
  link.click();
  URL.revokeObjectURL(url);
};

const navigateTo = (path: string) => {
  navigateTo(path);
};

// Lifecycle
onMounted(async () => {
  await refreshInventory();
});
</script>

<style scoped>
.inventory-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

.page-header {
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

.stats-grid {
  margin-bottom: 16px;
}

.stat-card {
  background: white;
  border: 1px solid #f3f4f6;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 800;
  color: #1b4332;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
}

.filters-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.search-wrapper {
  display: flex;
  align-items: center;
  background: #f8f6f2;
  border-radius: 40px;
  padding: 0 16px;
  gap: 12px;
  height: 44px;
}

.search-input {
  flex: 1;
  border: none;
  padding: 12px 0;
  background: transparent;
  outline: none;
  font-size: 14px;
}

.search-icon {
  color: #9ca3af;
}

.filter-group {
  display: flex;
  gap: 8px;
  height: 44px;
}

.filter-select {
  padding: 8px 12px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
  width: 100%;
  height: 44px;
  font-size: 13px;
}

.inventory-table-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.inventory-table :deep(.v-data-table__th) {
  background: #f8f6f2;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-avatar {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: #f5f3ed;
}

.product-name {
  font-weight: 600;
  color: #1b4332;
}

.product-variants {
  font-size: 11px;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 4px;
}

.category-tag {
  display: inline-block;
  padding: 4px 12px;
  background: #f0ede5;
  border-radius: 12px;
  font-size: 12px;
  color: #1b4332;
}

.stock-ok {
  color: #2d6a4f;
  font-weight: 600;
}

.stock-low {
  color: #f4a261;
  font-weight: 600;
}

.stock-out {
  color: #e07a5f;
  font-weight: 600;
}

/* Dialog */
.adjust-dialog {
  border-radius: 24px !important;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f3f4f6;
}

.dialog-title {
  font-size: 18px;
  color: #1b4332;
}

.dialog-subtitle {
  color: #6b7280;
}

.product-preview {
  padding: 12px 16px;
  background: #f8f6f2;
  border-radius: 12px;
}

.preview-name {
  font-weight: 600;
  color: #1b4332;
}

.preview-sku {
  font-size: 12px;
  color: #6b7280;
}

.preview-current {
  font-size: 13px;
  margin-top: 2px;
}

.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.form-label.required::after {
  content: " *";
  color: #e07a5f;
}

.input-hint {
  margin-top: 4px;
}

.dialog-actions {
  padding: 16px 24px;
  border-top: 1px solid #f3f4f6;
  gap: 8px;
}

.custom-snackbar :deep(.v-snackbar__content) {
  font-weight: 500;
  border-radius: 60px;
}

/* Responsive */
@media (max-width: 768px) {
  .inventory-container {
    padding: 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .stat-value {
    font-size: 18px;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
  }

  .search-wrapper {
    height: 38px;
    margin-bottom: 8px;
  }

  .filter-group {
    height: auto;
    flex-wrap: wrap;
    gap: 4px;
  }

  .filter-select {
    height: 38px;
    font-size: 12px;
  }

  .inventory-table :deep(.v-data-table__th),
  .inventory-table :deep(.v-data-table__td) {
    padding: 8px 12px !important;
    font-size: 12px;
  }

  .product-info {
    flex-direction: column;
    align-items: flex-start;
  }

  .product-avatar {
    width: 32px;
    height: 32px;
  }

  .dialog-actions {
    flex-direction: column;
  }

  .dialog-actions .v-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }

  .stat-value {
    font-size: 16px;
  }

  .stat-icon {
    width: 36px;
    height: 36px;
  }

  .stat-icon .v-icon {
    font-size: 18px !important;
  }

  .product-name {
    font-size: 13px;
  }

  .category-tag {
    font-size: 10px;
    padding: 2px 8px;
  }

  .dialog-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
