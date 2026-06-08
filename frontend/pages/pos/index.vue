<template>
  <div class="pos-container">
    <!-- Left Section -->
    <div class="left-section">
      <div class="header" v-if="headerLoading">
        <v-skeleton-loader type="heading" class="mb-2" width="40%" />
        <v-skeleton-loader type="text" width="60%" class="mb-1" />
        <v-skeleton-loader type="text" width="50%" />
      </div>
      <!-- Header -->
      <div class="header" v-else>
        <div class="logo-section">
          <div class="logo-icon">🍔</div>
          <div class="logo-text">BABADEACON</div>
          <div class="logo-badge">COFFEE</div>
        </div>
        <div class="header-right">
          <div class="stats-group">
            <div class="stat-item">
              <span class="stat-label">Today</span>
              <span class="stat-value">{{ today }}</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-label">Orders</span>
              <span class="stat-value highlight">{{ TodaysTotalOrders }}</span>
            </div>
          </div>

          <v-btn variant="text" class="report-btn">
            <span>Report</span>
            <v-icon end size="18">mdi-file-document-outline</v-icon>
          </v-btn>

          <div class="cart-badge-wrapper">
            <v-badge
              color="#E07A5F"
              :content="store.cart.length"
              offset-x="8"
              offset-y="8"
              v-if="store.hasCartItems"
            >
              <v-btn icon variant="text" size="small" class="cart-btn">
                <v-icon size="22">mdi-cart-outline</v-icon>
              </v-btn>
            </v-badge>
            <v-btn v-else icon variant="text" size="small" class="cart-btn">
              <v-icon size="22">mdi-cart-outline</v-icon>
            </v-btn>
          </div>
        </div>
      </div>

      <!-- Search -->
      <div class="search-section" v-if="searchLoading">
        <v-skeleton-loader type="text" class="mr-3" width="80%" />
        <v-skeleton-loader type="button" width="80px" />
      </div>
      <div v-else class="search-section">
        <div class="search-container">
          <v-icon class="search-icon">mdi-magnify</v-icon>
          <v-text-field
            v-model="searchQuery"
            variant="plain"
            placeholder="Search coffee, snacks, tea..."
            hide-details
            density="comfortable"
            class="search-field"
            @update:model-value="store.setSearchQuery(searchQuery)"
          />
          <v-btn class="filter-btn" variant="text" size="small">
            <v-icon>mdi-tune-variant</v-icon>
          </v-btn>
        </div>
      </div>

      <!-- Category Cards -->
      <div class="category-cards">
        <v-card
          v-for="category in store.filteredCategories"
          :key="category.id"
          :class="[
            'category-card',
            { active: store.selectedCategory === category.id },
          ]"
          :style="
            category.id === 'coffee'
              ? 'background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%);'
              : 'background: white;'
          "
          @click="store.setCategory(category.id)"
          elevation="0"
        >
          <div class="category-icon-large">{{ category.icon }}</div>
          <div class="category-content">
            <div class="category-title">{{ category.name }}</div>
            <div class="category-count">{{ category.itemCount }} items</div>
          </div>
          <v-chip
            :class="[
              'status-chip',
              category.status === 'restock' ? 'restock-chip' : 'available-chip',
            ]"
            size="x-small"
          >
            {{
              category.status === "available" ? "In Stock" : "Restock Needed"
            }}
          </v-chip>
        </v-card>
      </div>

      <div v-if="loading" class="product-grid">
        <v-skeleton-loader
          v-for="n in 8"
          :key="n"
          type="card"
          class="product-card-skeleton"
        />
      </div>

      <!-- Products -->
      <div v-else class="product-grid">
        <div
          v-for="product in store.filteredProducts"
          :key="product.id"
          class="product-card"
          @click="store.addToCart(product)"
        >
          <div class="product-image-wrapper">
            <v-img :src="product.image_url" class="product-image" cover>
              <template v-slot:placeholder>
                <div class="image-placeholder">☕</div>
              </template>
            </v-img>
            <v-btn
              icon
              class="quick-add-btn"
              size="small"
              @click="store.addToCart(product)"
            >
              <v-icon size="18">mdi-plus</v-icon>
            </v-btn>
          </div>
          <div class="product-info">
            <div class="product-name">{{ product.name }}</div>
            <div class="product-price">ksh{{ product.price }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Section -->
    <div class="right-section" v-if="rightSectionLoading">
      <v-card class="pa-4 mb-4" elevation="0">
        <v-skeleton-loader type="heading" class="mb-3" />
        <v-skeleton-loader type="text" class="mb-2" width="70%" />
        <v-skeleton-loader type="text" class="mb-2" width="60%" />
        <v-skeleton-loader type="text" width="80%" />
      </v-card>
      <v-card class="pa-4" elevation="0">
        <v-skeleton-loader
          type="image"
          class="mb-3"
          width="100%"
          height="150"
        />
        <v-skeleton-loader type="text" class="mb-2" width="90%" />
        <v-skeleton-loader type="text" class="mb-2" width="70%" />
      </v-card>
    </div>
    <div class="right-section" v-else>
      <div class="order-header">
        <div class="receipt-info">
          <div class="receipt-badge">RECEIPT</div>
          <div class="receipt-number">{{ receiptNumber }}</div>
        </div>
        <div class="order-actions">
          <v-btn icon variant="text" size="small" class="action-btn">
            <v-icon size="20">mdi-printer-outline</v-icon>
          </v-btn>
          <v-btn icon variant="text" size="small" class="action-btn">
            <v-icon size="20">mdi-format-list-bulleted</v-icon>
          </v-btn>
        </div>
      </div>

      <!-- Order Type -->
      <div class="order-type-tabs">
        <v-btn
          :class="['order-type-btn', { active: orderType === 'dine-in' }]"
          @click="orderType = 'dine-in'"
          variant="text"
        >
          <v-icon start size="18" v-if="orderType === 'dine-in'"
            >mdi-seat</v-icon
          >
          Dine In
        </v-btn>
        <v-btn
          :class="['order-type-btn', { active: orderType === 'take-away' }]"
          @click="orderType = 'take-away'"
          variant="text"
        >
          <v-icon start size="18" v-if="orderType === 'take-away'"
            >mdi-food-takeout-box</v-icon
          >
          Take Away
        </v-btn>
        <v-btn
          :class="['order-type-btn', { active: orderType === 'order-online' }]"
          @click="orderType = 'order-online'"
          variant="text"
        >
          <v-icon start size="18" v-if="orderType === 'order-online'"
            >mdi-cellphone</v-icon
          >
          Order Online
        </v-btn>
      </div>

      <!-- Customer Info -->
      <div class="customer-section">
        <div class="input-group">
          <label>Customer</label>
          <v-text-field
            v-model="customerName"
            variant="outlined"
            density="comfortable"
            placeholder="Customer name"
            hide-details
            class="custom-input"
          />
        </div>
        <div class="input-group">
          <label>Table / Takeaway #</label>
          <v-select
            v-model="tableNumber"
            :items="[
              'Table B12',
              'Table B11',
              'Table B13',
              'Takeaway #1',
              'Takeaway #2',
            ]"
            variant="outlined"
            density="comfortable"
            hide-details
            class="custom-select"
          />
        </div>
      </div>

      <!-- Order List -->
      <div v-if="store.hasCartItems" class="order-list-section">
        <div class="order-list-header">
          <span>Current Order</span>
          <span class="item-count">{{ store.cartItems.length }} items</span>
        </div>
        <div class="order-items">
          <div
            v-for="item in store.cartItems"
            :key="item.id"
            class="order-item"
          >
            <div class="item-info">
              <div class="item-name-row">
                <span class="item-name">{{ item.name }}</span>
                <v-btn
                  icon
                  size="x-small"
                  variant="text"
                  class="remove-item-btn"
                  @click="store.removeFromCart(item.id)"
                >
                  <v-icon size="14">mdi-close</v-icon>
                </v-btn>
              </div>
              <div class="item-meta">
                <span class="item-size">{{ item.size || "Regular" }}</span>
                <span class="item-temp">{{ item.temp || "Hot" }}</span>
              </div>
              <div class="item-modifier" v-if="item.modifier">
                <v-icon size="12">mdi-cube-outline</v-icon>
                {{ item.modifier }}
              </div>
            </div>
            <div class="item-price">
              ksh{{ (item.unitPrice * item.quantity).toFixed(2) }}
            </div>
            <div class="item-quantity">
              <v-btn
                icon
                size="x-small"
                variant="text"
                class="qty-btn"
                @click="store.decrementQuantity(item.id)"
              >
                <v-icon size="12">mdi-minus</v-icon>
              </v-btn>
              <span class="quantity">{{ item.quantity }}</span>
              <v-btn
                icon
                size="x-small"
                variant="text"
                class="qty-btn"
                @click="store.incrementQuantity(item.id)"
              >
                <v-icon size="12">mdi-plus</v-icon>
              </v-btn>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty cart -->
      <div v-else class="empty-cart">
        <div class="empty-cart-icon">🛒</div>
        <div class="empty-cart-text">No items yet</div>
        <div class="empty-cart-subtext">
          Start by adding items from the menu
        </div>
      </div>

      <!-- Payment Section -->
      <div v-if="store.hasCartItems" class="payment-section">
        <div class="payment-header">Payment Summary</div>
        <div class="payment-details">
          <div class="payment-row">
            <span>Subtotal</span>
            <span>ksh{{ store.subtotal.toFixed(2) }}</span>
          </div>
          <div class="payment-row">
            <span>Tax (10%)</span>
            <span>ksh{{ store.tax.toFixed(2) }}</span>
          </div>
          <div class="payment-row total-row">
            <span>Total</span>
            <span class="total-amount">ksh{{ store.total.toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <!-- Place Order Button -->
      <v-btn
        v-if="store.hasCartItems"
        class="place-order-btn"
        block
        size="large"
        @click="placeOrder"
      >
        <span>Place Order</span>
        <span class="order-total">ksh{{ store.total.toFixed(2) }}</span>
        <v-icon end>mdi-arrow-right</v-icon>
      </v-btn>
    </div>

    <!-- FAB for adding products (Admin only) -->
    <v-fab
      icon="mdi-plus"
      color="#E07A5F"
      location="bottom start"
      size="large"
      app
      @click="dialog = true"
      class="fab-add-product"
      v-if="authStore.isAdmin"
    />

    <!-- Add Product Dialog -->
    <v-dialog v-model="dialog" max-width="550" transition="dialog-transition">
      <v-card class="product-dialog">
        <v-card-title class="dialog-title">
          Add New Product
          <v-btn
            icon
            variant="text"
            @click="dialog = false"
            class="close-dialog-btn"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="isValid" class="product-form">
            <v-text-field
              v-model="product.name"
              label="Product Name"
              :rules="[rules.required]"
              variant="outlined"
              density="comfortable"
            />
            <v-text-field
              v-model="product.price"
              label="Price"
              type="number"
              :rules="[rules.required, rules.positive]"
              variant="outlined"
              density="comfortable"
              prefix="ksh"
            />
            <v-select
              v-model="product.category"
              :items="categoryOptions"
              label="Category"
              :rules="[rules.required]"
              variant="outlined"
              density="comfortable"
            />
            <v-file-input
              v-model="product.file"
              label="Product Image"
              accept="image/*"
              :rules="[rules.required]"
              variant="outlined"
              density="comfortable"
              prepend-icon=""
              prepend-inner-icon="mdi-image"
            />
            <div v-if="imagePreview" class="image-preview">
              <img :src="imagePreview" alt="Preview" class="preview-img" />
            </div>
          </v-form>
        </v-card-text>
        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="dialog = false" class="cancel-btn"
            >Cancel</v-btn
          >
          <v-btn
            color="#1B4332"
            :disabled="!isValid"
            @click="submitProduct"
            class="save-btn"
          >
            Save Product
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
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" icon="mdi-close" @click="snackbar.show = false" />
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { usePosStore } from "~/stores/pos";
import { useAuthStore } from "~/stores/auth";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const authStore = useAuthStore();
const store = usePosStore();
const searchQuery = ref("");
const orderType = ref("dine-in");
const customerName = ref("");
const tableNumber = ref("Table B12");
const receiptNumber = ref("");
const TodaysTotalOrders = ref(0);
const loading = ref(true);
const rightSectionLoading = ref(true);
const headerLoading = ref(true);
const searchLoading = ref(true);

const dialog = ref(false);
const isValid = ref(false);
const form = ref(null);
const imagePreview = ref("");
const snackbar = ref({
  show: false,
  text: "",
  color: "success",
});

const product = ref({
  name: "",
  price: "",
  category: "",
  file: null,
});

const categoryOptions = [
  { title: "Coffee", value: "coffee" },
  { title: "Snack", value: "snack" },
  { title: "Tea", value: "tea" },
];

const rules = {
  required: (v: any) => !!v || "This field is required",
  positive: (v: number) => v > 0 || "Price must be positive",
};

const usedReceipts = new Set<string>();
function generateUniqueReceipt() {
  let receipt: string;
  do {
    receipt = `RCP-${Math.floor(10000 + Math.random() * 90000)}`;
  } while (usedReceipts.has(receipt));
  usedReceipts.add(receipt);
  return receipt;
}
receiptNumber.value = generateUniqueReceipt();

const today = new Date().toLocaleDateString(undefined, {
  weekday: "short",
  day: "numeric",
  month: "short",
});

// Set customer name from auth user if available
if (authStore.user) {
  customerName.value = authStore.user.name;
}

const placeOrder = async () => {
  if (store.hasCartItems) {
    const orderData = {
      receiptNumber: receiptNumber.value,
      orderType: orderType.value,
      customerName: customerName.value || authStore.user?.name || "Guest",
      tableNumber: tableNumber.value,
      items: store.cartItems,
      subtotal: store.subtotal,
      tax: store.tax,
      total: store.total,
    };

    try {
      await store.saveOrder(orderData);
      const orders = await store.getAllOrders();
      console.log("All orders after placing new order:", orders);
      const todaysDateString = new Date().toLocaleDateString();
      TodaysTotalOrders.value = orders.reduce((count, order) => {
        const orderDate = new Date(order.created_at).toLocaleDateString();
        console.log(
          `Order ${order._id} date: ${orderDate}, matches today: ${
            orderDate === todaysDateString
          }`
        );
        return count + (orderDate === todaysDateString ? 1 : 0);
      }, 0);
      console.log(
        "Today's total orders after placing new order:",
        TodaysTotalOrders.value
      );

      store.clearCart();
      receiptNumber.value = generateUniqueReceipt();

      snackbar.value = {
        show: true,
        text: "Order placed successfully!",
        color: "success",
      };
    } catch (error) {
      snackbar.value = {
        show: true,
        text: "Failed to place order",
        color: "error",
      };
    }
  }
};

watch(
  () => product.value.file,
  async (file) => {
    if (!file) {
      imagePreview.value = "";
      return;
    }
    const base64 = await processFormImage(file);
    imagePreview.value = base64;
  }
);

const processFormImage = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
};

const submitProduct = async () => {
  const { valid } = await form.value.validate();
  if (!valid) return;

  try {
    const formData = new FormData();
    formData.append("name", product.value.name);
    formData.append("price", product.value.price);
    formData.append("category", product.value.category);
    formData.append("image", product.value.file);

    await store.addProduct(formData);
    await store.getAllProducts();
    dialog.value = false;
    form.value.reset();
    product.value.file = null;
    imagePreview.value = "";

    snackbar.value = {
      show: true,
      text: "Product added successfully!",
      color: "success",
    };
  } catch (error) {
    console.error("Error adding product:", error);
    snackbar.value = {
      show: true,
      text: "Failed to add product",
      color: "error",
    };
  }
};

// Check authentication before loading
onMounted(async () => {
  // Redirect if not authenticated
  if (!authStore.checkAuth()) {
    await navigateTo("/login");
    return;
  }

  try {
    loading.value = true;
    headerLoading.value = true;
    rightSectionLoading.value = true;
    searchLoading.value = true;

    const [_, orders] = await Promise.all([
      store.getAllProducts(),
      store.getAllOrders(),
    ]);

    const todayString = new Date().toLocaleDateString();
    TodaysTotalOrders.value = orders.reduce((count, order) => {
      const orderDate = new Date(order.created_at).toLocaleDateString();
      return count + (orderDate === todayString ? 1 : 0);
    }, 0);
    console.log("Today's total orders:", TodaysTotalOrders.value);
  } catch (error) {
    console.error("Error loading data:", error);
    snackbar.value = {
      show: true,
      text: "Failed to load data",
      color: "error",
    };
  } finally {
    loading.value = false;
    rightSectionLoading.value = false;
    headerLoading.value = false;
    searchLoading.value = false;
  }
});
</script>

<style scoped>
.pos-container {
  display: flex;
  gap: 0;
  min-height: calc(100vh - 64px);
  background: #f8f6f2;
}

.left-section {
  flex: 1;
  padding: 28px 32px;
  background: #f8f6f2;
  overflow-y: auto;
}

.right-section {
  width: 420px;
  background: white;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.05);
  border-radius: 32px 0 0 32px;
}

/* Header Styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-badge {
  font-size: 12px;
  font-weight: 600;
  color: #e07a5f;
  background: rgba(224, 122, 95, 0.1);
  padding: 4px 8px;
  border-radius: 20px;
  letter-spacing: 0.5px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stats-group {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 16px;
  background: white;
  border-radius: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.stat-label {
  font-size: 11px;
  font-weight: 500;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.stat-value.highlight {
  color: #e07a5f;
  font-size: 16px;
}

.stat-divider {
  width: 1px;
  height: 24px;
  background: #e5e0d5;
}

.report-btn {
  text-transform: none;
  font-weight: 500;
  color: #666;
  background: white;
  border-radius: 40px;
  padding: 0 16px;
}

.cart-badge-wrapper {
  margin: 0 -8px;
}

.cart-btn {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* Search Section */
.search-section {
  margin-bottom: 28px;
}

.search-container {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 60px;
  padding: 0 8px 0 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.search-container:focus-within {
  box-shadow: 0 4px 16px rgba(27, 67, 50, 0.12);
}

.search-icon {
  color: #999;
  font-size: 20px;
}

.search-field {
  flex: 1;
}

.search-field :deep(.v-field) {
  --v-field-padding-start: 8px;
}

.filter-btn {
  color: #666;
  background: #f5f3ed;
  margin: 6px;
  border-radius: 40px;
}

/* Category Cards */
.category-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.category-card {
  padding: 20px 16px;
  position: relative;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 20px !important;
  border: 1px solid #e5e0d5;
}

.category-card:hover {
  transform: translateY(-2px);
}

.category-card.active {
  border-color: #1b4332;
  box-shadow: 0 8px 20px rgba(27, 67, 50, 0.15);
}

.category-icon-large {
  font-size: 32px;
  margin-bottom: 12px;
}

.category-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.category-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
  color: #1b4332;
}

.category-card:not([style*="linear-gradient"]) .category-title {
  color: #1b4332;
}

.category-card[style*="linear-gradient"] .category-title {
  color: white;
}

.category-count {
  font-size: 12px;
  color: #888;
}

.category-card[style*="linear-gradient"] .category-count {
  color: rgba(255, 255, 255, 0.8);
}

.status-chip {
  position: absolute;
  top: 16px;
  right: 16px;
  font-weight: 500;
}

.available-chip {
  background: #e8f5e9 !important;
  color: #2e7d32 !important;
}

.restock-chip {
  background: #ffebee !important;
  color: #c62828 !important;
}

/* Product Grid */
.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.product-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #e5e0d5;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  border-color: #1b4332;
}

.product-image-wrapper {
  position: relative;
  height: 120px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  background: #f5f3ed;
}

.quick-add-btn {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: white;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.quick-add-btn:hover {
  background: #1b4332;
  color: white;
  transform: scale(1.05);
}

.product-info {
  padding: 12px;
  text-align: center;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-price {
  font-size: 14px;
  font-weight: 700;
  color: #e07a5f;
}

/* Right Section Components */
.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.receipt-info {
  display: flex;
  flex-direction: column;
}

.receipt-badge {
  font-size: 11px;
  font-weight: 600;
  color: #e07a5f;
  letter-spacing: 1px;
}

.receipt-number {
  font-size: 20px;
  font-weight: 800;
  color: #1b4332;
  letter-spacing: -0.5px;
}

.order-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: #f5f3ed;
}

.order-type-tabs {
  display: flex;
  gap: 12px;
  background: #f5f3ed;
  padding: 4px;
  border-radius: 60px;
}

.order-type-btn {
  flex: 1;
  text-transform: none;
  font-weight: 600;
  font-size: 13px;
  border-radius: 40px !important;
  padding: 8px 0;
  color: #666;
  transition: all 0.2s ease;
}

.order-type-btn.active {
  background: #1b4332;
  color: white;
}

.customer-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #f8f6f2;
  padding: 16px;
  border-radius: 20px;
}

.input-group label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #666;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.custom-input :deep(.v-field),
.custom-select :deep(.v-field) {
  border-radius: 12px;
}

/* Order List */
.order-list-section {
  flex: 1;
  overflow-y: auto;
  max-height: 320px;
}

.order-list-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 16px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.item-count {
  font-size: 12px;
  font-weight: 500;
  color: #999;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: #f8f6f2;
  border-radius: 16px;
  transition: all 0.2s ease;
}

.order-item:hover {
  background: #f0ede5;
}

.item-info {
  flex: 1;
}

.item-name-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.item-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.remove-item-btn {
  opacity: 0.5;
  transition: opacity 0.2s ease;
}

.remove-item-btn:hover {
  opacity: 1;
}

.item-meta {
  display: flex;
  gap: 12px;
  font-size: 11px;
  color: #999;
  margin-bottom: 4px;
}

.item-modifier {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #888;
}

.item-price {
  font-size: 15px;
  font-weight: 700;
  color: #1b4332;
  min-width: 65px;
  text-align: right;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 6px;
  background: white;
  padding: 4px 8px;
  border-radius: 40px;
}

.qty-btn {
  background: transparent;
}

.quantity {
  font-size: 14px;
  font-weight: 600;
  min-width: 24px;
  text-align: center;
  color: #1b4332;
}

/* Empty Cart */
.empty-cart {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 48px 20px;
}

.empty-cart-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.4;
}

.empty-cart-text {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.empty-cart-subtext {
  font-size: 13px;
  color: #999;
}

/* Payment Section */
.payment-section {
  background: #f8f6f2;
  border-radius: 20px;
  padding: 20px;
}

.payment-header {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.payment-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.payment-row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
}

.total-row {
  font-size: 18px;
  font-weight: 800;
  color: #1b4332;
  padding-top: 12px;
  border-top: 2px solid #e5e0d5;
  margin-top: 4px;
}

.total-amount {
  color: #e07a5f;
}

/* Place Order Button */
.place-order-btn {
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%) !important;
  color: white !important;
  text-transform: none;
  font-weight: 700;
  font-size: 16px;
  border-radius: 60px !important;
  display: flex;
  justify-content: space-between;
  padding: 8px 24px !important;
}

.order-total {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 40px;
  font-size: 14px;
}

/* FAB */
.fab-add-product {
  position: fixed;
  bottom: 28px;
  left: 28px;
  z-index: 100;
}

/* Dialog Styles */
.product-dialog {
  border-radius: 28px !important;
}

.dialog-title {
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
  padding: 24px 24px 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-dialog-btn {
  color: #999;
}

.product-form {
  padding: 8px 0;
}

.image-preview {
  margin-top: 16px;
  text-align: center;
}

.preview-img {
  max-width: 100%;
  max-height: 150px;
  border-radius: 12px;
  object-fit: cover;
}

.dialog-actions {
  padding: 16px 24px 24px 24px;
  gap: 12px;
}

.cancel-btn {
  text-transform: none;
  font-weight: 500;
  color: #666;
}

.save-btn {
  text-transform: none;
  font-weight: 600;
  color: white !important;
  background: #1b4332 !important;
  border-radius: 40px !important;
  padding: 0 24px !important;
}

/* Snackbar */
.custom-snackbar :deep(.v-snackbar__content) {
  font-weight: 500;
  border-radius: 60px;
}

/* Skeleton Loaders */
.product-card-skeleton {
  border-radius: 20px !important;
}

/* Scrollbar */
.left-section::-webkit-scrollbar,
.order-list-section::-webkit-scrollbar {
  width: 6px;
}

.left-section::-webkit-scrollbar-track,
.order-list-section::-webkit-scrollbar-track {
  background: #e5e0d5;
  border-radius: 10px;
}

.left-section::-webkit-scrollbar-thumb,
.order-list-section::-webkit-scrollbar-thumb {
  background: #1b4332;
  border-radius: 10px;
}

/* Responsive */
@media (max-width: 1200px) {
  .product-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .pos-container {
    flex-direction: column;
  }

  .right-section {
    width: 100%;
    border-radius: 32px 32px 0 0;
  }

  .product-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 768px) {
  .left-section {
    padding: 20px;
  }

  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .category-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .header-right {
    gap: 12px;
  }

  .stats-group {
    display: none;
  }
}
</style>
