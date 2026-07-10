<!-- pages/admin/inventory/low-stock/index.vue -->
<template>
  <div class="low-stock-container">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">
          <v-icon size="16" color="#F4A261">mdi-alert</v-icon>
          Inventory Management
        </div>
        <h1 class="page-title">Low Stock Alert</h1>
        <p class="page-subtitle">Products that need restocking</p>
      </div>
      <div class="header-actions">
        <v-btn color="#2D6A4F" @click="refreshLowStock">
          <v-icon start>mdi-refresh</v-icon>
          Refresh
        </v-btn>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card warning">
        <div class="stat-icon">
          <v-icon size="32" color="#F4A261">mdi-alert</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ lowStockProducts.length }}</div>
          <div class="stat-label">Low Stock Items</div>
        </div>
      </div>
      <div class="stat-card urgent">
        <div class="stat-icon">
          <v-icon size="32" color="#E07A5F">mdi-alert-circle</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ urgentProducts.length }}</div>
          <div class="stat-label">Urgent (Below 50% of reorder)</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <v-icon size="32" color="#2D6A4F">mdi-package-variant</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ totalProducts }}</div>
          <div class="stat-label">Total Products</div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-grid">
      <v-skeleton-loader
        v-for="n in 4"
        :key="n"
        type="card"
        class="low-stock-skeleton"
      />
    </div>

    <!-- Low Stock Products -->
    <div v-else>
      <div v-if="lowStockProducts.length === 0" class="empty-state">
        <v-icon size="64" color="#2D6A4F">mdi-check-circle</v-icon>
        <h3>All Stock Levels Are Healthy!</h3>
        <p>No products are currently below their reorder level.</p>
      </div>

      <div v-else class="products-grid">
        <div
          v-for="product in lowStockProducts"
          :key="product.id || product._id"
          class="product-card"
          :class="{ urgent: isUrgent(product) }"
        >
          <div class="product-header">
            <div class="product-info">
              <div class="product-avatar">
                <v-img
                  :src="product.image_url || '/images/product-placeholder.png'"
                  width="48"
                  height="48"
                  cover
                  class="rounded"
                />
              </div>
              <div>
                <div class="product-name">{{ product.name }}</div>
                <div class="product-sku">SKU: {{ product.sku || "-" }}</div>
              </div>
            </div>
            <div class="product-status">
              <v-chip
                :color="isUrgent(product) ? '#E07A5F' : '#F4A261'"
                size="small"
                text-color="white"
              >
                {{ isUrgent(product) ? "Urgent" : "Low Stock" }}
              </v-chip>
            </div>
          </div>

          <div class="product-stock-details">
            <div class="stock-item">
              <span class="stock-label">Current Stock</span>
              <span
                class="stock-value"
                :class="isUrgent(product) ? 'urgent-text' : 'warning-text'"
              >
                {{ getStock(product) }}
              </span>
            </div>
            <div class="stock-item">
              <span class="stock-label">Reorder Level</span>
              <span class="stock-value">{{
                product.inventory?.reorder_level || 10
              }}</span>
            </div>
            <div class="stock-item">
              <span class="stock-label">Days to Empty</span>
              <span class="stock-value">{{
                calculateDaysToEmpty(product)
              }}</span>
            </div>
          </div>

          <div class="stock-bar-container">
            <div class="stock-bar">
              <div
                class="stock-bar-fill"
                :style="{ width: `${getStockPercentage(product)}%` }"
                :class="getStockBarClass(product)"
              ></div>
            </div>
            <div class="stock-bar-labels">
              <span>0%</span>
              <span>{{ getStockPercentage(product) }}%</span>
              <span>100%</span>
            </div>
          </div>

          <div class="product-actions">
            <v-btn
              color="#2D6A4F"
              variant="tonal"
              size="small"
              @click="restockProduct(product)"
            >
              <v-icon start size="16">mdi-plus</v-icon>
              Restock
            </v-btn>
            <v-btn
              color="#2D6A4F"
              variant="text"
              size="small"
              @click="viewProduct(product)"
            >
              View Product
            </v-btn>
          </div>
        </div>
      </div>
    </div>

    <!-- Restock Dialog -->
    <v-dialog v-model="restockDialog.show" max-width="500">
      <v-card class="restock-dialog">
        <div class="dialog-header">
          <h3>Restock Product</h3>
          <v-btn icon variant="text" @click="restockDialog.show = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <v-card-text>
          <v-form ref="restockFormRef" v-model="restockValid">
            <div class="product-preview" v-if="restockDialog.product">
              <div class="preview-name">{{ restockDialog.product.name }}</div>
              <div class="preview-sku">
                SKU: {{ restockDialog.product.sku }}
              </div>
              <div class="preview-current">
                Current Stock:
                <strong>{{ getStock(restockDialog.product) }}</strong>
              </div>
              <div class="preview-reorder">
                Reorder Level:
                <strong>{{
                  restockDialog.product.inventory?.reorder_level || 10
                }}</strong>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label required">Quantity to Add</label>
              <v-text-field
                v-model="restockForm.quantity"
                type="number"
                placeholder="Enter quantity"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required, rules.positive]"
                hide-details="auto"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Supplier</label>
              <v-select
                v-model="restockForm.supplier_id"
                :items="supplierOptions"
                placeholder="Select supplier"
                variant="outlined"
                density="comfortable"
                hide-details="auto"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Notes</label>
              <v-textarea
                v-model="restockForm.notes"
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
          <v-btn variant="text" @click="restockDialog.show = false"
            >Cancel</v-btn
          >
          <v-btn
            color="#2D6A4F"
            :disabled="!restockValid || restockSubmitting"
            :loading="restockSubmitting"
            @click="submitRestock"
          >
            Confirm Restock
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

definePageMeta({
  layout: "default",
  middleware: "auth",
});

// State
const products = ref([]);
const loading = ref(true);
const restockSubmitting = ref(false);
const restockValid = ref(false);
const restockFormRef = ref(null);

const restockDialog = ref({
  show: false,
  product: null,
});

const restockForm = ref({
  quantity: "",
  supplier_id: "",
  notes: "",
});

const snackbar = ref({
  show: false,
  text: "",
  color: "success",
});

// Rules
const rules = {
  required: (v: any) => !!v || "This field is required",
  positive: (v: number) => v > 0 || "Quantity must be greater than 0",
};

// Computed
const totalProducts = computed(() => products.value.length);

const lowStockProducts = computed(() =>
  products.value.filter((item) => {
    const stock = getStock(item);
    const reorder = item.inventory?.reorder_level || 10;
    return stock > 0 && stock <= reorder;
  })
);

const urgentProducts = computed(() =>
  lowStockProducts.value.filter((item) => {
    const stock = getStock(item);
    const reorder = item.inventory?.reorder_level || 10;
    return stock <= reorder * 0.5;
  })
);

const supplierOptions = ref([
  { title: "Beverage Distributors Ltd", value: "supplier-1" },
  { title: "Electronics World Ltd", value: "supplier-2" },
]);

// Methods
const getStock = (item: any) => {
  return item.inventory?.available || item.inventory?.quantity || 0;
};

const isUrgent = (item: any) => {
  const stock = getStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  return stock <= reorder * 0.5;
};

const getStockPercentage = (item: any) => {
  const stock = getStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  return Math.min((stock / reorder) * 100, 100);
};

const getStockBarClass = (item: any) => {
  const percentage = getStockPercentage(item);
  if (percentage <= 25) return "danger";
  if (percentage <= 50) return "warning";
  return "normal";
};

const calculateDaysToEmpty = (item: any) => {
  // TODO: Implement actual calculation based on sales velocity
  return "7 days";
};

const viewProduct = (product: any) => {
  console.log("View product:", product);
};

const restockProduct = (product: any) => {
  restockDialog.value = {
    show: true,
    product: product,
  };
  restockForm.value = {
    quantity: (product.inventory?.reorder_level || 10) - getStock(product),
    supplier_id: "",
    notes: "",
  };
  restockValid.value = false;
};

const submitRestock = async () => {
  const { valid } = await restockFormRef.value.validate();
  if (!valid) return;

  restockSubmitting.value = true;
  try {
    const data = {
      product_id:
        restockDialog.value.product.id || restockDialog.value.product._id,
      quantity: parseInt(restockForm.value.quantity),
      supplier_id: restockForm.value.supplier_id || undefined,
      notes: restockForm.value.notes || undefined,
    };

    console.log("Restock data:", data);

    snackbar.value = {
      show: true,
      text: `Stock restocked successfully! Added ${data.quantity} units.`,
      color: "success",
    };

    restockDialog.value.show = false;
    await refreshLowStock();
  } catch (error) {
    console.error("Error restocking:", error);
    snackbar.value = {
      show: true,
      text: "Failed to restock product",
      color: "error",
    };
  } finally {
    restockSubmitting.value = false;
  }
};

const refreshLowStock = async () => {
  loading.value = true;
  try {
    // TODO: API Call
    // products.value = await $fetch('/api/v1/products?low_stock=true');

    // Mock data
    products.value = [
      {
        id: "1",
        name: "Tuzo Milk 500ml",
        sku: "TUZO-MILK-500ML",
        image_url: "",
        inventory: { quantity: 8, available: 8, reorder_level: 30 },
      },
      {
        id: "2",
        name: "Sawa Soap 225g",
        sku: "SAWA-SOAP-225G",
        image_url: "",
        inventory: { quantity: 5, available: 5, reorder_level: 20 },
      },
      {
        id: "3",
        name: "Ajab Chapati Flour 2kg",
        sku: "AJAB-FLOUR-2KG",
        image_url: "",
        inventory: { quantity: 12, available: 12, reorder_level: 40 },
      },
    ];
  } catch (error) {
    console.error("Error loading low stock products:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  refreshLowStock();
});
</script>

<style scoped>
.low-stock-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

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
  color: #f4a261;
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

.header-actions {
  display: flex;
  gap: 12px;
}

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

.stat-card.warning {
  border-left: 4px solid #f4a261;
}

.stat-card.urgent {
  border-left: 4px solid #e07a5f;
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

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.product-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  border-left: 4px solid #f4a261;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.product-card.urgent {
  border-left-color: #e07a5f;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-avatar {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: #f5f3ed;
}

.product-name {
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 2px;
}

.product-sku {
  font-size: 12px;
  color: #6b7280;
}

.product-stock-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.stock-item {
  text-align: center;
}

.stock-label {
  display: block;
  font-size: 11px;
  color: #6b7280;
  margin-bottom: 4px;
}

.stock-value {
  font-size: 18px;
  font-weight: 700;
}

.stock-value.warning-text {
  color: #f4a261;
}

.stock-value.urgent-text {
  color: #e07a5f;
}

.stock-bar-container {
  margin-bottom: 16px;
}

.stock-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.stock-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.stock-bar-fill.normal {
  background: #2d6a4f;
}

.stock-bar-fill.warning {
  background: #f4a261;
}

.stock-bar-fill.danger {
  background: #e07a5f;
}

.stock-bar-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 4px;
  font-size: 10px;
  color: #6b7280;
}

.product-actions {
  display: flex;
  gap: 12px;
  margin-top: 4px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state h3 {
  margin-top: 16px;
  color: #1b4332;
}

.empty-state p {
  color: #6b7280;
  margin: 8px 0;
}

.restock-dialog {
  border-radius: 24px !important;
}

.product-preview {
  padding: 12px 16px;
  background: #f8f6f2;
  border-radius: 12px;
  margin-bottom: 20px;
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
  margin-top: 4px;
}

.preview-reorder {
  font-size: 13px;
}

/* Responsive */
@media (max-width: 768px) {
  .low-stock-container {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-title {
    font-size: 24px;
  }

  .header-actions {
    flex-direction: column;
  }

  .header-actions .v-btn {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .products-grid {
    grid-template-columns: 1fr;
  }

  .product-header {
    flex-direction: column;
  }

  .product-stock-details {
    grid-template-columns: 1fr 1fr;
  }

  .product-actions {
    flex-direction: column;
  }

  .product-actions .v-btn {
    width: 100%;
  }

  .dialog-actions {
    flex-direction: column;
  }

  .dialog-actions .v-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .product-info {
    flex-direction: column;
    align-items: flex-start;
  }

  .product-stock-details {
    grid-template-columns: 1fr;
  }

  .product-stock-details .stock-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
