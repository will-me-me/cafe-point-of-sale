<!-- pages/admin/sales/debt/index.vue -->
<template>
  <div class="debt-orders-container">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#E07A5F">mdi-account-cash</v-icon>
          Sales Management
        </div>
        <h1 class="page-title">Debt Orders</h1>
        <p class="page-subtitle">Orders with pending payment</p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right mt-4 mt-md-0">
        <v-btn
          variant="outlined"
          color="#E07A5F"
          @click="exportDebtOrders"
          class="mr-2"
        >
          <v-icon start>mdi-download</v-icon>
          Export
        </v-btn>
        <v-btn color="#2D6A4F" @click="refreshDebtOrders" :loading="loading">
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
                  style="background: #e07a5f20; color: #e07a5f"
                >
                  <v-icon size="24">mdi-account-cash</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ totalDebtOrders }}</div>
                <div class="stat-label">Total Debt Orders</div>
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
                  style="background: #e07a5f20; color: #e07a5f"
                >
                  <v-icon size="24">mdi-currency-usd</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">
                  KSh {{ totalDebtAmount.toLocaleString() }}
                </div>
                <div class="stat-label">Total Outstanding</div>
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
                  <v-icon size="24">mdi-account-group</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ uniqueDebtCustomers }}</div>
                <div class="stat-label">Customers with Debt</div>
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
                  style="background: #f4a26120; color: #f4a261"
                >
                  <v-icon size="24">mdi-clock-outline</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ averageDebtAge }} days</div>
                <div class="stat-label">Average Debt Age</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Debt Aging Breakdown -->
    <v-row no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="aging-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="aging-header">
              <span class="aging-title font-weight-bold">Aging Breakdown</span>
              <span class="aging-subtitle text-caption text-medium-emphasis">
                Debt distribution by age
              </span>
            </div>
            <v-row no-gutters>
              <v-col
                v-for="(item, key) in agingData"
                :key="key"
                cols="6"
                sm="3"
                class="pa-1"
              >
                <div class="aging-item" :style="{ borderColor: item.color }">
                  <div class="aging-label">{{ item.label }}</div>
                  <div class="aging-value" :style="{ color: item.color }">
                    KSh {{ getAgingAmount(key).toLocaleString() }}
                  </div>
                  <div class="aging-count">{{ getAgingCount(key) }} orders</div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Debt Orders Table -->
    <v-row no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="debt-table-card" elevation="0" rounded="xl">
          <v-card-text class="pa-0">
            <div class="table-header pa-4">
              <span class="table-title font-weight-bold">Pending Debts</span>
              <span class="table-count text-caption text-medium-emphasis">
                {{ filteredDebtOrders.length }} orders
              </span>
            </div>
            <v-data-table
              :headers="headers"
              :items="filteredDebtOrders"
              :loading="loading"
              :items-per-page="10"
              class="debt-table"
              item-value="id"
            >
              <template v-slot:item.receiptNumber="{ item }">
                <span class="receipt-number font-weight-medium">
                  #{{ item.receiptNumber || item.id?.slice(-6) }}
                </span>
              </template>

              <template v-slot:item.customer_name="{ item }">
                <div class="customer-info">
                  <div class="customer-name">
                    {{ item.customer_name || item.customerName || "Guest" }}
                  </div>
                  <div
                    v-if="item.customer_phone"
                    class="customer-phone text-caption text-medium-emphasis"
                  >
                    {{ item.customer_phone }}
                  </div>
                </div>
              </template>

              <template v-slot:item.total="{ item }">
                <span class="amount-cell"
                  >KSh {{ (item.total || 0).toFixed(2) }}</span
                >
              </template>

              <template v-slot:item.created_at="{ item }">
                <div>{{ formatDate(item.created_at) }}</div>
                <div class="debt-age" :class="getAgeClass(item)">
                  {{ getDaysAgo(item.created_at) }}
                </div>
              </template>

              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  color="#2D6A4F"
                  @click="viewOrder(item)"
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
                <v-btn size="small" color="#2D6A4F" @click="markAsPaid(item)">
                  <v-icon start size="16">mdi-check</v-icon>
                  Mark Paid
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Mark as Paid Confirmation Dialog -->
    <v-dialog v-model="paidDialog.show" max-width="400">
      <v-card class="confirm-dialog">
        <v-card-text class="text-center pa-6">
          <v-icon size="64" color="#2D6A4F">mdi-check-circle</v-icon>
          <h3 class="mt-4">Mark as Paid?</h3>
          <p class="mt-2 text-medium-emphasis">
            Confirm that
            <strong>{{ paidDialog.order?.customer_name || "Guest" }}</strong>
            has paid
            <strong>KSh {{ (paidDialog.order?.total || 0).toFixed(2) }}</strong>
            for order <strong>{{ paidDialog.order?.receiptNumber }}</strong>
          </p>
          <v-btn variant="text" @click="paidDialog.show = false" class="mr-2"
            >Cancel</v-btn
          >
          <v-btn
            color="#2D6A4F"
            :loading="processing"
            @click="confirmMarkAsPaid"
          >
            Confirm Payment
          </v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Order Detail Dialog -->
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
const processing = ref(false);

const detailDialog = ref({
  show: false,
  order: null,
});

const paidDialog = ref({
  show: false,
  order: null,
});

// Table Headers
const headers = [
  { title: "Receipt #", key: "receipt_number", sortable: true },
  { title: "Customer", key: "customer_name", sortable: true },
  { title: "Total", key: "total", sortable: true },
  { title: "Date", key: "created_at", sortable: true },
  { title: "Actions", key: "actions", sortable: false },
];

// Computed
const allOrders = computed(() => store.AllOrders || []);

const debtOrders = computed(() => {
  return allOrders.value.filter(
    (order) =>
      (order.payment_mode === "debt" || order.paymentMode === "debt") &&
      (order.payment_status === "pending" || order.paymentStatus === "pending")
  );
});

const totalDebtOrders = computed(() => debtOrders.value.length);

const totalDebtAmount = computed(() => {
  return debtOrders.value.reduce((sum, order) => sum + (order.total || 0), 0);
});

const uniqueDebtCustomers = computed(() => {
  const customers = new Set();
  debtOrders.value.forEach((order) => {
    customers.add(order.customer_name || order.customerName || "Guest");
  });
  return customers.size;
});

const averageDebtAge = computed(() => {
  if (debtOrders.value.length === 0) return 0;
  const totalDays = debtOrders.value.reduce((sum, order) => {
    const days = Math.floor(
      (Date.now() - new Date(order.created_at).getTime()) /
        (1000 * 60 * 60 * 24)
    );
    return sum + days;
  }, 0);
  return Math.round(totalDays / debtOrders.value.length);
});

const filteredDebtOrders = computed(() => {
  return debtOrders.value.sort(
    (a, b) =>
      new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  );
});

// Aging Data
const agingData = {
  "0-7_days": { label: "0-7 Days", color: "#2D6A4F" },
  "8-14_days": { label: "8-14 Days", color: "#F4A261" },
  "15-30_days": { label: "15-30 Days", color: "#E07A5F" },
  "30+_days": { label: "30+ Days", color: "#EF4444" },
};

const getAgingAmount = (key: string) => {
  const orders = debtOrders.value.filter((order) => {
    const days = Math.floor(
      (Date.now() - new Date(order.created_at).getTime()) /
        (1000 * 60 * 60 * 24)
    );
    if (key === "0-7_days") return days >= 0 && days <= 7;
    if (key === "8-14_days") return days >= 8 && days <= 14;
    if (key === "15-30_days") return days >= 15 && days <= 30;
    if (key === "30+_days") return days > 30;
    return false;
  });
  return orders.reduce((sum, order) => sum + (order.total || 0), 0);
};

const getAgingCount = (key: string) => {
  const orders = debtOrders.value.filter((order) => {
    const days = Math.floor(
      (Date.now() - new Date(order.created_at).getTime()) /
        (1000 * 60 * 60 * 24)
    );
    if (key === "0-7_days") return days >= 0 && days <= 7;
    if (key === "8-14_days") return days >= 8 && days <= 14;
    if (key === "15-30_days") return days >= 15 && days <= 30;
    if (key === "30+_days") return days > 30;
    return false;
  });
  return orders.length;
};

// Helper Methods
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

const formatOrderType = (type: string) => {
  const types: Record<string, string> = {
    "dine-in": "Dine In",
    takeaway: "Take Away",
    delivery: "Delivery",
    "order-online": "Online",
  };
  return types[type] || type || "N/A";
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
const formatDate = (date: string) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const getDaysAgo = (date: string) => {
  if (!date) return "-";
  const days = Math.floor(
    (Date.now() - new Date(date).getTime()) / (1000 * 60 * 60 * 24)
  );
  return `${days} days ago`;
};

const getAgeClass = (order: any) => {
  const days = Math.floor(
    (Date.now() - new Date(order.created_at).getTime()) / (1000 * 60 * 60 * 24)
  );
  if (days > 30) return "age-critical";
  if (days > 14) return "age-warning";
  return "age-normal";
};

const viewOrder = (order: any) => {
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

const markAsPaid = (order: any) => {
  paidDialog.value = {
    show: true,
    order: order,
  };
};

const confirmMarkAsPaid = async () => {
  if (!paidDialog.value.order) return;

  processing.value = true;
  try {
    const order = paidDialog.value.order;
    const orderId = order._id || order.id;

    // Update order status
    await store.updateDebtOrderStatus(orderId);

    // Refresh data
    await store.getAllOrders();

    paidDialog.value.show = false;

    // Show success notification
    // You can add a snackbar here
  } catch (error) {
    console.error("Error marking debt as paid:", error);
  } finally {
    processing.value = false;
  }
};

const exportDebtOrders = () => {
  const data = filteredDebtOrders.value.map((order) => ({
    receipt: order.receiptNumber,
    customer: order.customer_name || "Guest",
    total: order.total,
    date: order.created_at,
    days_old: Math.floor(
      (Date.now() - new Date(order.created_at).getTime()) /
        (1000 * 60 * 60 * 24)
    ),
  }));

  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `debt_orders_${new Date().toISOString().split("T")[0]}.json`;
  link.click();
  URL.revokeObjectURL(url);
};

const refreshDebtOrders = async () => {
  loading.value = true;
  try {
    await store.getAllOrders();
  } catch (error) {
    console.error("Error refreshing debt orders:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await refreshDebtOrders();
});
</script>

<style scoped>
.debt-orders-container {
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

.aging-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.aging-header {
  margin-bottom: 16px;
}

.aging-title {
  font-size: 16px;
  color: #1b4332;
}

.aging-item {
  padding: 12px;
  border-left: 3px solid;
  background: #f8f6f2;
  border-radius: 8px;
}

.aging-label {
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.aging-value {
  font-size: 18px;
  font-weight: 800;
  margin: 4px 0;
}

.aging-count {
  font-size: 12px;
  color: #6b7280;
}

.debt-table-card {
  background: white;
  border: 1px solid #f3f4f6;
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

.debt-table :deep(.v-data-table__th) {
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

.customer-info .customer-name {
  font-weight: 500;
}

.customer-info .customer-phone {
  font-size: 11px;
}

.debt-age {
  font-size: 11px;
  font-weight: 500;
  margin-top: 2px;
}

.debt-age.age-normal {
  color: #2d6a4f;
}

.debt-age.age-warning {
  color: #f4a261;
}

.debt-age.age-critical {
  color: #e07a5f;
}

.confirm-dialog {
  border-radius: 24px !important;
}

.confirm-dialog p {
  line-height: 1.5;
}

/* Responsive */
@media (max-width: 768px) {
  .debt-orders-container {
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

  .aging-item {
    padding: 8px;
  }

  .aging-value {
    font-size: 16px;
  }

  .debt-table :deep(.v-data-table__th),
  .debt-table :deep(.v-data-table__td) {
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

  .aging-value {
    font-size: 14px;
  }

  .customer-info .customer-name {
    font-size: 13px;
  }
}
</style>
<style scoped>
.today-sales-container {
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
</style>
