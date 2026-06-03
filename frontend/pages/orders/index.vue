<!-- frontend/pages/orders/index.vue -->
<template>
  <div class="orders-container">
    <!-- Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">Transaction History</div>
        <h1 class="page-title">Orders</h1>
        <p class="page-subtitle">View and manage all customer orders</p>
      </div>
      <div class="header-actions">
        <v-btn variant="outlined" class="export-btn">
          <v-icon start>mdi-export</v-icon>
          Export
        </v-btn>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <div class="search-wrapper">
        <v-icon class="search-icon">mdi-magnify</v-icon>
        <input
          v-model="searchQuery"
          placeholder="Search by receipt number or customer..."
          class="search-input"
        />
      </div>
      <div class="filter-group">
        <select v-model="selectedType" class="filter-select">
          <option value="">All Types</option>
          <option value="dine-in">🍽️ Dine In</option>
          <option value="take-away">📦 Take Away</option>
          <option value="order-online">📱 Online</option>
        </select>
        <select v-model="selectedStatus" class="filter-select">
          <option value="">All Status</option>
          <option value="completed">✅ Completed</option>
          <option value="preparing">🔄 Preparing</option>
          <option value="cancelled">❌ Cancelled</option>
        </select>
        <input type="date" v-model="dateFilter" class="date-picker" />
      </div>
    </div>

    <!-- Stats Summary -->
    <div class="stats-summary">
      <div class="summary-card">
        <div class="summary-icon" style="background: #2d6a4f20">
          <v-icon color="#2D6A4F">mdi-cart-outline</v-icon>
        </div>
        <div class="summary-info">
          <div class="summary-value">{{ filteredOrders.length }}</div>
          <div class="summary-label">Total Orders</div>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon" style="background: #e07a5f20">
          <v-icon color="#E07A5F">mdi-currency-usd</v-icon>
        </div>
        <div class="summary-info">
          <div class="summary-value">${{ totalRevenue }}</div>
          <div class="summary-label">Total Revenue</div>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon" style="background: #f4a26120">
          <v-icon color="#F4A261">mdi-chart-line</v-icon>
        </div>
        <div class="summary-info">
          <div class="summary-value">${{ avgOrderValue }}</div>
          <div class="summary-label">Average Order</div>
        </div>
      </div>
    </div>

    <!-- Orders Table -->
    <v-card class="orders-table-card" elevation="0">
      <div class="table-container">
        <table class="orders-table">
          <thead>
            <tr>
              <th>Receipt #</th>
              <th>Customer</th>
              <th>Order Type</th>
              <th>Items</th>
              <th>Total</th>
              <th>Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in paginatedOrders" :key="order.id">
              <td class="receipt-cell">{{ order.receiptNumber }}</td>
              <td>{{ order.customerName }}</td>
              <td>
                <span class="order-type-badge" :class="order.orderType">
                  {{ order.orderType }}
                </span>
              </td>
              <td>{{ order.items.length }} items</td>
              <td class="amount-cell">${{ order.total }}</td>
              <td>{{ formatDate(order.created_at) }}</td>
              <td>
                <span class="status-badge" :class="order.status || 'completed'">
                  {{ order.status || "completed" }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    @click="viewOrderDetails(order)"
                  >
                    <v-icon size="18">mdi-eye</v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    @click="printReceipt(order)"
                  >
                    <v-icon size="18">mdi-printer</v-icon>
                  </v-btn>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination-section">
        <div class="items-per-page">
          <span>Show</span>
          <select v-model="itemsPerPage">
            <option :value="10">10</option>
            <option :value="25">25</option>
            <option :value="50">50</option>
          </select>
          <span>entries</span>
        </div>
        <div class="pagination-controls">
          <v-btn
            icon
            variant="text"
            size="small"
            @click="prevPage"
            :disabled="currentPage === 1"
          >
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
          <v-btn
            icon
            variant="text"
            size="small"
            @click="nextPage"
            :disabled="currentPage === totalPages"
          >
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </div>
      </div>
    </v-card>

    <!-- Order Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="800">
      <v-card class="order-details-dialog">
        <div class="dialog-header">
          <div>
            <div class="receipt-badge">Order Details</div>
            <h2>{{ selectedOrder?.receiptNumber }}</h2>
          </div>
          <v-btn icon variant="text" @click="detailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <div class="order-info-grid">
          <div class="info-card">
            <div class="info-label">Customer Name</div>
            <div class="info-value">{{ selectedOrder?.customerName }}</div>
          </div>
          <div class="info-card">
            <div class="info-label">Order Type</div>
            <div class="info-value">{{ selectedOrder?.orderType }}</div>
          </div>
          <div class="info-card">
            <div class="info-label">Table/Number</div>
            <div class="info-value">
              {{ selectedOrder?.tableNumber || "N/A" }}
            </div>
          </div>
          <div class="info-card">
            <div class="info-label">Date & Time</div>
            <div class="info-value">
              {{ formatDate(selectedOrder?.created_at) }}
            </div>
          </div>
        </div>

        <div class="items-list">
          <h3>Order Items</h3>
          <div
            v-for="item in selectedOrder?.items"
            :key="item.id"
            class="order-item-detail"
          >
            <div class="item-detail-info">
              <div class="item-detail-name">{{ item.name }}</div>
              <div class="item-detail-meta">
                <span>{{ item.size || "Regular" }}</span>
                <span>{{ item.temp || "Hot" }}</span>
              </div>
            </div>
            <div class="item-detail-qty">x{{ item.quantity }}</div>
            <div class="item-detail-price">
              ${{ (item.unitPrice * item.quantity).toFixed(2) }}
            </div>
          </div>
        </div>

        <div class="order-summary">
          <div class="summary-row">
            <span>Subtotal</span>
            <span>${{ selectedOrder?.subtotal }}</span>
          </div>
          <div class="summary-row">
            <span>Tax (10%)</span>
            <span>${{ selectedOrder?.tax }}</span>
          </div>
          <div class="summary-row total">
            <span>Total</span>
            <span>${{ selectedOrder?.total }}</span>
          </div>
        </div>

        <div class="dialog-actions">
          <v-btn variant="outlined" @click="printReceipt(selectedOrder)">
            <v-icon start>mdi-printer</v-icon>
            Print Receipt
          </v-btn>
          <v-btn color="#2D6A4F" @click="detailsDialog = false">Close</v-btn>
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
const searchQuery = ref("");
const selectedType = ref("");
const selectedStatus = ref("");
const dateFilter = ref("");
const itemsPerPage = ref(10);
const currentPage = ref(1);
const detailsDialog = ref(false);
const selectedOrder = ref(null);

const orders = computed(() => store.AllOrders);

const filteredOrders = computed(() => {
  let filtered = [...orders.value];

  if (searchQuery.value) {
    filtered = filtered.filter(
      (order) =>
        order.receiptNumber
          ?.toLowerCase()
          .includes(searchQuery.value.toLowerCase()) ||
        order.customerName
          ?.toLowerCase()
          .includes(searchQuery.value.toLowerCase())
    );
  }

  if (selectedType.value) {
    filtered = filtered.filter(
      (order) => order.orderType === selectedType.value
    );
  }

  if (dateFilter.value) {
    filtered = filtered.filter((order) => {
      const orderDate = new Date(order.created_at).toISOString().split("T")[0];
      return orderDate === dateFilter.value;
    });
  }

  return filtered;
});

const totalRevenue = computed(() => {
  return filteredOrders.value
    .reduce((sum, order) => sum + order.total, 0)
    .toFixed(2);
});

const avgOrderValue = computed(() => {
  if (filteredOrders.value.length === 0) return "0";
  return (totalRevenue.value / filteredOrders.value.length).toFixed(2);
});

const totalPages = computed(() =>
  Math.ceil(filteredOrders.value.length / itemsPerPage.value)
);

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredOrders.value.slice(start, end);
});

const formatDate = (date) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleString();
};

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const viewOrderDetails = (order) => {
  selectedOrder.value = order;
  detailsDialog.value = true;
};

const printReceipt = (order) => {
  // Print receipt logic
  window.print();
};

onMounted(async () => {
  await store.getAllOrders();
});
</script>

<style scoped>
.orders-container {
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

.export-btn {
  border-color: #e5e7eb;
  border-radius: 40px;
}

.filters-section {
  background: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 24px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.search-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background: #f8f6f2;
  border-radius: 40px;
  padding: 0 16px;
  gap: 12px;
}

.search-input {
  flex: 1;
  border: none;
  padding: 12px 0;
  background: transparent;
  outline: none;
}

.filter-group {
  display: flex;
  gap: 12px;
}

.filter-select,
.date-picker {
  padding: 8px 16px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.summary-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.summary-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.summary-value {
  font-size: 28px;
  font-weight: 800;
  color: #1b4332;
}

.summary-label {
  font-size: 13px;
  color: #6b7280;
}

.orders-table-card {
  border-radius: 24px;
  overflow: hidden;
}

.table-container {
  overflow-x: auto;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
}

.orders-table th {
  text-align: left;
  padding: 16px 20px;
  background: #f8f6f2;
  font-weight: 600;
  color: #374151;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.orders-table td {
  padding: 16px 20px;
  border-bottom: 1px solid #f3f4f6;
  color: #4b5563;
}

.receipt-cell {
  font-weight: 600;
  color: #1b4332;
  font-family: monospace;
}

.amount-cell {
  font-weight: 600;
  color: #e07a5f;
}

.order-type-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.order-type-badge.dine-in {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.order-type-badge.take-away {
  background: #f4a26120;
  color: #f4a261;
}

.order-type-badge.order-online {
  background: #6b4e7120;
  color: #6b4e71;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.status-badge.completed {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.status-badge.preparing {
  background: #f4a26120;
  color: #f4a261;
}

.status-badge.cancelled {
  background: #e07a5f20;
  color: #e07a5f;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-top: 1px solid #f3f4f6;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.items-per-page select {
  padding: 4px 8px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-info {
  font-size: 13px;
  color: #6b7280;
}

/* Dialog Styles */
.order-details-dialog {
  border-radius: 32px !important;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
}

.dialog-header .receipt-badge {
  font-size: 11px;
  font-weight: 600;
  color: #e07a5f;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.dialog-header h2 {
  font-family: "Playfair Display", serif;
  font-size: 24px;
  font-weight: 700;
  color: #1b4332;
}

.order-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 24px;
}

.info-card {
  background: #f8f6f2;
  padding: 16px;
  border-radius: 16px;
}

.info-label {
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.info-value {
  font-weight: 600;
  color: #1b4332;
}

.items-list {
  padding: 0 24px;
}

.items-list h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 16px;
}

.order-item-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.item-detail-name {
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 4px;
}

.item-detail-meta {
  display: flex;
  gap: 12px;
  font-size: 11px;
  color: #6b7280;
}

.item-detail-price {
  font-weight: 600;
  color: #e07a5f;
}

.order-summary {
  background: #f8f6f2;
  margin: 24px;
  padding: 20px;
  border-radius: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
}

.summary-row.total {
  border-top: 2px solid #e5e7eb;
  margin-top: 8px;
  padding-top: 12px;
  font-size: 18px;
  font-weight: 800;
  color: #1b4332;
}

.dialog-actions {
  padding: 16px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
