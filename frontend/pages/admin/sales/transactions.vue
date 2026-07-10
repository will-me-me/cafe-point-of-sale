<!-- pages/admin/sales/transactions/index.vue -->
<template>
  <div class="transactions-container">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#2D6A4F">mdi-cash-multiple</v-icon>
          Sales Management
        </div>
        <h1 class="page-title">Transactions</h1>
        <p class="page-subtitle">All completed orders and transactions</p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right mt-4 mt-md-0">
        <v-btn
          variant="outlined"
          color="#2D6A4F"
          @click="exportTransactions"
          class="mr-2"
        >
          <v-icon start>mdi-download</v-icon>
          Export
        </v-btn>
        <v-btn color="#2D6A4F" @click="refreshTransactions" :loading="loading">
          <v-icon start>mdi-refresh</v-icon>
          Refresh
        </v-btn>
      </v-col>
    </v-row>

    <!-- Stats -->
    <v-row class="stats-grid" no-gutters>
      <v-col cols="12" sm="4" class="pa-2">
        <v-card class="stat-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon"
                  style="background: #2d6a4f20; color: #2d6a4f"
                >
                  <v-icon size="24">mdi-cart-outline</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ totalTransactions }}</div>
                <div class="stat-label">Total Transactions</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4" class="pa-2">
        <v-card class="stat-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon"
                  style="background: #e07a5f20; color: #e07a5f"
                >
                  <v-icon size="24">mdi-currency-usd</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">
                  KSh {{ totalRevenue.toLocaleString() }}
                </div>
                <div class="stat-label">Total Revenue</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4" class="pa-2">
        <v-card class="stat-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon"
                  style="background: #f4a26120; color: #f4a261"
                >
                  <v-icon size="24">mdi-chart-line</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">
                  KSh {{ averageTransaction.toFixed(2) }}
                </div>
                <div class="stat-label">Average Transaction</div>
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
          <v-col cols="12" md="4" class="pr-md-4">
            <div class="search-wrapper">
              <v-icon class="search-icon">mdi-magnify</v-icon>
              <input
                v-model="searchQuery"
                placeholder="Search by receipt or customer..."
                class="search-input"
              />
            </div>
          </v-col>
          <v-col cols="12" md="8">
            <v-row no-gutters class="filter-group">
              <v-col cols="6" sm="4" class="pr-1">
                <input type="date" v-model="dateFrom" class="filter-date" />
              </v-col>
              <v-col cols="6" sm="4" class="px-1">
                <input type="date" v-model="dateTo" class="filter-date" />
              </v-col>
              <v-col cols="12" sm="4" class="pl-1">
                <select v-model="paymentFilter" class="filter-select">
                  <option value="">All Payments</option>
                  <option value="cash">Cash</option>
                  <option value="mpesa">M-Pesa</option>
                  <option value="debt">Debt</option>
                  <option value="card">Card</option>
                </select>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Transactions Table -->
    <v-card class="transactions-table-card" elevation="0" rounded="xl">
      <v-card-text class="pa-0">
        <v-data-table
          :headers="headers"
          :items="filteredTransactions"
          :loading="loading"
          :items-per-page="10"
          class="transactions-table"
          item-value="id"
        >
          <template v-slot:item.receiptNumber="{ item }">
            <span class="receipt-number font-weight-medium"
              >#{{ item.receiptNumber || item.id?.slice(-6) }}</span
            >
          </template>

          <template v-slot:item.created_at="{ item }">
            <div>{{ formatDate(item.created_at) }}</div>
            <div class="time">{{ formatTime(item.created_at) }}</div>
          </template>

          <template v-slot:item.customer_name="{ item }">
            {{ item.customer_name || item.customerName || "Walk-in" }}
          </template>

          <template v-slot:item.items="{ item }">
            {{ item.items?.length || 0 }}
          </template>

          <template v-slot:item.total="{ item }">
            <span class="amount-cell"
              >KSh {{ (item.total || 0).toFixed(2) }}</span
            >
          </template>

          <template v-slot:item.payment_mode="{ item }">
            <v-chip
              :color="getPaymentColor(item.payment_mode || item.paymentMode)"
              size="x-small"
              text-color="white"
            >
              {{ formatPaymentMode(item.payment_mode || item.paymentMode) }}
            </v-chip>
          </template>

          <template v-slot:item.payment_status="{ item }">
            <v-chip
              :color="getStatusColor(item.payment_status || item.paymentStatus)"
              size="x-small"
              text-color="white"
            >
              {{ formatStatus(item.payment_status || item.paymentStatus) }}
            </v-chip>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-btn
              icon
              size="small"
              variant="text"
              color="#2D6A4F"
              @click="viewTransaction(item)"
            >
              <v-icon size="18">mdi-eye</v-icon>
            </v-btn>
            <v-btn
              icon
              size="small"
              variant="text"
              color="#2D6A4F"
              @click="printReceipt(item)"
            >
              <v-icon size="18">mdi-printer</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Transaction Detail Dialog (same as Today's Sales) -->
    <v-dialog v-model="detailDialog.show" max-width="700">
      <!-- Same dialog as Today's Sales -->
      <v-card class="detail-dialog">
        <v-card-title class="dialog-header">
          <div>
            <div class="receipt-badge">Order Details</div>
            <h3>
              #{{
                detailDialog.order?.receipt_number ||
                detailDialog.order?.id?.slice(-6)
              }}
            </h3>
          </div>
          <v-btn icon variant="text" @click="detailDialog.show = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <div v-if="detailDialog.order" class="detail-content">
            <v-row class="detail-section">
              <v-col cols="12" sm="6">
                <div class="detail-row">
                  <span class="detail-label">Customer</span>
                  <span class="detail-value">
                    {{
                      detailDialog.order.customer_name ||
                      detailDialog.order.customerName ||
                      "Walk-in"
                    }}
                  </span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Order Type</span>
                  <span class="detail-value">
                    {{
                      formatOrderType(
                        detailDialog.order.order_type ||
                          detailDialog.order.orderType
                      )
                    }}
                  </span>
                </div>
              </v-col>
              <v-col cols="12" sm="6">
                <div class="detail-row">
                  <span class="detail-label">Date & Time</span>
                  <span class="detail-value">{{
                    formatFullDate(detailDialog.order.created_at)
                  }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Table / Number</span>
                  <span class="detail-value">{{
                    detailDialog.order.table_number ||
                    detailDialog.order.tableNumber ||
                    "N/A"
                  }}</span>
                </div>
              </v-col>
            </v-row>

            <v-divider class="my-2" />

            <div class="detail-section">
              <div class="section-title font-weight-bold mb-2">Items</div>
              <div
                v-for="(item, index) in detailDialog.order.items"
                :key="index"
                class="order-item-detail"
              >
                <div class="item-info">
                  <span class="item-name">{{
                    item.name || item.product_name
                  }}</span>
                  <span class="item-meta text-caption text-medium-emphasis">
                    {{ item.quantity || 1 }} × KSh
                    {{ (item.unit_price || item.price || 0).toFixed(2) }}
                  </span>
                </div>
                <span class="item-total font-weight-bold">
                  KSh
                  {{
                    (
                      (item.unit_price || item.price || 0) *
                      (item.quantity || 1)
                    ).toFixed(2)
                  }}
                </span>
              </div>
            </div>

            <v-divider class="my-2" />

            <div class="detail-section totals">
              <div class="total-row">
                <span class="font-weight-medium">Subtotal</span>
                <span
                  >KSh {{ (detailDialog.order.subtotal || 0).toFixed(2) }}</span
                >
              </div>
              <div class="total-row">
                <span class="font-weight-medium">Tax</span>
                <span>KSh {{ (detailDialog.order.tax || 0).toFixed(2) }}</span>
              </div>
              <div class="total-row grand-total">
                <span class="font-weight-bold">Total</span>
                <span class="font-weight-bold"
                  >KSh {{ (detailDialog.order.total || 0).toFixed(2) }}</span
                >
              </div>
              <div class="total-row">
                <span class="font-weight-medium">Payment Method</span>
                <span>{{
                  formatPaymentMode(
                    detailDialog.order.payment_mode ||
                      detailDialog.order.paymentMode
                  )
                }}</span>
              </div>
              <div class="total-row">
                <span class="font-weight-medium">Payment Status</span>
                <v-chip
                  :color="
                    getStatusColor(
                      detailDialog.order.payment_status ||
                        detailDialog.order.paymentStatus
                    )
                  "
                  size="small"
                  text-color="white"
                >
                  {{
                    formatStatus(
                      detailDialog.order.payment_status ||
                        detailDialog.order.paymentStatus
                    )
                  }}
                </v-chip>
              </div>
            </div>
          </div>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="detailDialog.show = false">Close</v-btn>
          <v-btn color="#2D6A4F" @click="printReceipt(detailDialog.order)">
            <v-icon start>mdi-printer</v-icon>
            Print Receipt
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { usePosStore } from "~/stores/pos";
import { useReceipt } from "~/composables/useReceipt";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const store = usePosStore();
const receipt = useReceipt();
const loading = ref(false);
const searchQuery = ref("");
const dateFrom = ref("");
const dateTo = ref("");
const paymentFilter = ref("");

const detailDialog = ref({
  show: false,
  order: null,
});

// Table Headers
const headers = [
  { title: "Receipt #", key: "receipt_number", sortable: true },
  { title: "Date & Time", key: "created_at", sortable: true },
  { title: "Customer", key: "customer_name", sortable: true },
  { title: "Items", key: "items", sortable: true },
  { title: "Total", key: "total", sortable: true },
  { title: "Payment", key: "payment_mode", sortable: true },
  { title: "Status", key: "payment_status", sortable: true },
  { title: "Actions", key: "actions", sortable: false },
];

// Computed
const allOrders = computed(() => store.AllOrders || []);

const totalTransactions = computed(() => allOrders.value.length);

const totalRevenue = computed(() => {
  return allOrders.value.reduce((sum, order) => sum + (order.total || 0), 0);
});

const averageTransaction = computed(() => {
  if (totalTransactions.value === 0) return 0;
  return totalRevenue.value / totalTransactions.value;
});

const filteredTransactions = computed(() => {
  let filtered = [...allOrders.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (order) =>
        order.receiptNumber?.toLowerCase().includes(query) ||
        order.customer_name?.toLowerCase().includes(query) ||
        order.customerName?.toLowerCase().includes(query)
    );
  }

  if (dateFrom.value) {
    filtered = filtered.filter(
      (order) => new Date(order.created_at) >= new Date(dateFrom.value)
    );
  }

  if (dateTo.value) {
    const endDate = new Date(dateTo.value);
    endDate.setHours(23, 59, 59);
    filtered = filtered.filter(
      (order) => new Date(order.created_at) <= endDate
    );
  }

  if (paymentFilter.value) {
    filtered = filtered.filter(
      (order) =>
        (order.payment_mode || order.paymentMode) === paymentFilter.value
    );
  }

  return filtered.sort(
    (a, b) =>
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );
});

// Helper Methods (reuse from Today's Sales)
const formatFullDate = (date: string) => {
  if (!date) return "-";
  return new Date(date).toLocaleString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};
const formatOrderType = (type: string) => {
  const types: Record<string, string> = {
    "dine-in": "Dine In",
    takeaway: "Take Away",
    delivery: "Delivery",
    "order-online": "Online",
  };
  return types[type] || type || "N/A";
};
const formatDate = (date: string) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const formatTime = (date: string) => {
  if (!date) return "-";
  return new Date(date).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatPaymentMode = (mode: string) => {
  const modes: Record<string, string> = {
    cash: "Cash",
    mpesa: "M-Pesa",
    debt: "Debt",
    card: "Card",
  };
  return modes[mode] || mode || "N/A";
};

const formatStatus = (status: string) => {
  const statuses: Record<string, string> = {
    paid: "Paid",
    completed: "Completed",
    pending: "Pending",
    overdue: "Overdue",
    cancelled: "Cancelled",
  };
  return statuses[status] || status || "N/A";
};

const getPaymentColor = (method: string) => {
  const colors: Record<string, string> = {
    cash: "#2D6A4F",
    mpesa: "#4A90D9",
    debt: "#E07A5F",
    card: "#6B4E71",
  };
  return colors[method?.toLowerCase()] || "#6B7280";
};

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    paid: "#2D6A4F",
    completed: "#2D6A4F",
    pending: "#F4A261",
    overdue: "#E07A5F",
    cancelled: "#6B7280",
  };
  return colors[status?.toLowerCase()] || "#6B7280";
};

const viewTransaction = (order: any) => {
  detailDialog.value = {
    show: true,
    order: order,
  };
};

const printReceipt = (order: any) => {
  if (order) {
    receipt.printReceipt(order);
  }
};

const exportTransactions = () => {
  const data = filteredTransactions.value.map((order) => ({
    receipt: order.receiptNumber,
    customer: order.customer_name || "Guest",
    total: order.total,
    payment: order.payment_mode,
    status: order.payment_status,
    date: order.created_at,
  }));

  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `transactions_${new Date().toISOString().split("T")[0]}.json`;
  link.click();
  URL.revokeObjectURL(url);
};

const refreshTransactions = async () => {
  loading.value = true;
  try {
    await store.getAllOrders();
  } catch (error) {
    console.error("Error refreshing transactions:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await refreshTransactions();
});
</script>

<style scoped>
.transactions-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Reuse styles from Today's Sales with adjustments */
.page-header {
  margin-bottom: 24px;
}

.page-badge {
  font-size: 12px;
  font-weight: 600;
  color: #2d6a4f;
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

.stat-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  margin-top: 4px;
}

.stat-change.positive {
  color: #2d6a4f;
}

.stat-change.negative {
  color: #e07a5f;
}

.stat-debt-amount {
  font-size: 14px;
  font-weight: 600;
  color: #e07a5f;
  margin-top: 4px;
}

.chart-card,
.payment-breakdown-card,
.orders-table-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.chart-container {
  height: 250px;
  position: relative;
}

.payment-breakdown {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.payment-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8f6f2;
  border-radius: 12px;
}

.payment-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.payment-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.payment-name {
  font-weight: 600;
  color: #1b4332;
}

.payment-count {
  font-size: 12px;
  color: #6b7280;
}

.payment-amount {
  text-align: right;
}

.payment-total {
  font-weight: 700;
  color: #1b4332;
}

.payment-percentage {
  font-size: 12px;
  color: #6b7280;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-title {
  font-size: 16px;
  color: #1b4332;
}

.orders-table :deep(.v-data-table__th) {
  background: #f8f6f2;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

.order-number {
  color: #1b4332;
}

.detail-dialog {
  border-radius: 24px !important;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f3f4f6;
}

.receipt-badge {
  font-size: 11px;
  font-weight: 600;
  color: #e07a5f;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.dialog-header h3 {
  font-family: "Playfair Display", serif;
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
  margin: 0;
}

.detail-content {
  padding: 8px 0;
}

.detail-section {
  margin-bottom: 8px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
}

.detail-label {
  color: #6b7280;
}

.detail-value {
  font-weight: 500;
  color: #1b4332;
}

.section-title {
  color: #1b4332;
}

.order-item-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
}

.order-item-detail:last-child {
  border-bottom: none;
}

.item-name {
  font-weight: 500;
  color: #1b4332;
}

.item-meta {
  margin-left: 8px;
}

.item-total {
  color: #e07a5f;
}

.totals {
  margin-top: 8px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
}

.grand-total {
  border-top: 2px solid #f3f4f6;
  padding-top: 12px;
  margin-top: 8px;
  font-size: 18px;
}

.dialog-actions {
  padding: 16px 24px;
  border-top: 1px solid #f3f4f6;
  gap: 8px;
}

/* Responsive */
@media (max-width: 768px) {
  .today-sales-container {
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

  .chart-container {
    height: 200px;
  }

  .orders-table :deep(.v-data-table__th),
  .orders-table :deep(.v-data-table__td) {
    padding: 8px 12px !important;
    font-size: 12px;
  }

  .payment-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .payment-amount {
    width: 100%;
    display: flex;
    justify-content: space-between;
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

  .chart-container {
    height: 160px;
  }

  .order-item-detail {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}
.page-header {
  margin-bottom: 24px;
}

.page-badge {
  font-size: 12px;
  font-weight: 600;
  color: #2d6a4f;
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

.filter-date,
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

.transactions-table-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.transactions-table :deep(.v-data-table__th) {
  background: #f8f6f2;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

.receipt-number {
  color: #1b4332;
}

.amount-cell {
  font-weight: 600;
  color: #e07a5f;
}

.time {
  font-size: 11px;
  color: #6b7280;
}

/* Responsive */
@media (max-width: 768px) {
  .transactions-container {
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

  .filter-date,
  .filter-select {
    height: 38px;
    font-size: 12px;
  }

  .transactions-table :deep(.v-data-table__th),
  .transactions-table :deep(.v-data-table__td) {
    padding: 8px 12px !important;
    font-size: 12px;
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
}
</style>
