<!-- pages/admin/sales/today/index.vue -->
<template>
  <div class="today-sales-container">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#2D6A4F">mdi-calendar-today</v-icon>
          Sales Management
        </div>
        <h1 class="page-title">Today's Sales</h1>
        <p class="page-subtitle">Daily sales summary and performance</p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right mt-4 mt-md-0">
        <v-btn
          variant="outlined"
          color="#2D6A4F"
          @click="exportSales"
          class="mr-2"
        >
          <v-icon start>mdi-download</v-icon>
          Export
        </v-btn>
        <v-btn color="#2D6A4F" @click="refreshSales" :loading="loading">
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
                  <v-icon size="24">mdi-currency-usd</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">
                  KSh {{ todayRevenue.toLocaleString() }}
                </div>
                <div class="stat-label">Total Revenue</div>
                <div class="stat-change" :class="revenueChangeClass">
                  <v-icon size="14">{{ revenueChangeIcon }}</v-icon>
                  <span>{{ revenueChangePercent }}</span>
                </div>
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
                  <v-icon size="24">mdi-cart-outline</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ todayOrdersCount }}</div>
                <div class="stat-label">Total Orders</div>
                <div class="stat-change" :class="ordersChangeClass">
                  <v-icon size="14">{{ ordersChangeIcon }}</v-icon>
                  <span>{{ ordersChangePercent }}</span>
                </div>
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
                  <v-icon size="24">mdi-chart-line</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">
                  KSh {{ averageOrderValue.toFixed(2) }}
                </div>
                <div class="stat-label">Average Order Value</div>
                <div class="stat-change" :class="avgOrderChangeClass">
                  <v-icon size="14">{{ avgOrderChangeIcon }}</v-icon>
                  <span>{{ avgOrderChangePercent }}</span>
                </div>
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
                  <v-icon size="24">mdi-account-cash</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ todayDebtOrders }}</div>
                <div class="stat-label">Debt Orders</div>
                <div class="stat-debt-amount">
                  KSh {{ todayDebtAmount.toLocaleString() }}
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Charts Row -->
    <v-row class="mt-2" no-gutters>
      <v-col cols="12" lg="8" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Sales by Hour</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Hourly sales distribution
                </div>
              </div>
              <v-select
                v-model="chartPeriod"
                :items="['Today', 'Yesterday', 'Last 7 Days']"
                variant="outlined"
                density="compact"
                class="period-select"
                style="max-width: 140px"
                @update:model-value="updateChart"
              />
            </div>
            <div class="chart-container">
              <canvas ref="hourlyChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="4" class="pa-2">
        <v-card class="payment-breakdown-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Payment Methods</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Today's payment distribution
                </div>
              </div>
            </div>
            <div class="payment-breakdown">
              <div
                v-for="method in paymentBreakdown"
                :key="method.name"
                class="payment-item"
              >
                <div class="payment-info">
                  <div
                    class="payment-icon"
                    :style="{ background: method.color + '20' }"
                  >
                    <v-icon size="20" :color="method.color">{{
                      method.icon
                    }}</v-icon>
                  </div>
                  <div>
                    <div class="payment-name">{{ method.name }}</div>
                    <div class="payment-count">{{ method.count }} orders</div>
                  </div>
                </div>
                <div class="payment-amount">
                  <div class="payment-total">
                    KSh {{ method.total.toLocaleString() }}
                  </div>
                  <div class="payment-percentage">{{ method.percentage }}%</div>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Today's Orders Table -->
    <v-row class="mt-2" no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="orders-table-card" elevation="0" rounded="xl">
          <v-card-text class="pa-0">
            <div class="table-header pa-4">
              <span class="table-title font-weight-bold">Today's Orders</span>
              <span class="table-count text-caption text-medium-emphasis">
                {{ filteredOrders.length }} orders
              </span>
            </div>
            <v-data-table
              :headers="headers"
              :items="filteredOrders"
              :loading="loading"
              :items-per-page="10"
              class="orders-table"
              item-value="id"
            >
              <template v-slot:item.receiptNumber="{ item }">
                <span class="order-number font-weight-medium">
                  #{{ item.receipt_number || item.id?.slice(-6) }}
                </span>
              </template>

              <template v-slot:item.created_at="{ item }">
                {{ formatTime(item.created_at) }}
              </template>

              <template v-slot:item.customer_name="{ item }">
                {{ item.customer_name || item.customerName || "Walk-in" }}
              </template>

              <template v-slot:item.order_type="{ item }">
                <v-chip
                  :color="getOrderTypeColor(item.order_type || item.orderType)"
                  size="x-small"
                  text-color="white"
                >
                  {{ formatOrderType(item.order_type || item.orderType) }}
                </v-chip>
              </template>

              <template v-slot:item.items="{ item }">
                {{ item.items?.length || 0 }}
              </template>

              <template v-slot:item.total="{ item }">
                <span class="font-weight-bold"
                  >KSh {{ (item.total || 0).toLocaleString() }}</span
                >
              </template>

              <template v-slot:item.payment_mode="{ item }">
                <v-chip
                  :color="
                    getPaymentColor(item.payment_mode || item.paymentMode)
                  "
                  size="x-small"
                  text-color="white"
                >
                  {{ formatPaymentMode(item.payment_mode || item.paymentMode) }}
                </v-chip>
              </template>

              <template v-slot:item.payment_status="{ item }">
                <v-chip
                  :color="
                    getStatusColor(item.payment_status || item.paymentStatus)
                  "
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
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Order Detail Dialog -->
    <v-dialog v-model="detailDialog.show" max-width="700">
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
import { ref, computed, onMounted, watch } from "vue";
import Chart from "chart.js/auto";
import { usePosStore } from "~/stores/pos";
import { useReceipt } from "~/composables/useReceipt";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const store = usePosStore();
const receipt = useReceipt();
const loading = ref(false);
const chartPeriod = ref("Today");
const hourlyChartCanvas = ref<HTMLCanvasElement | null>(null);
let hourlyChartInstance: Chart | null = null;

const detailDialog = ref({
  show: false,
  order: null,
});

// Table Headers
const headers = [
  { title: "Order #", key: "receiptNumber", sortable: true },
  { title: "Time", key: "created_at", sortable: true },
  { title: "Customer", key: "customer_name", sortable: true },
  { title: "Type", key: "order_type", sortable: true },
  { title: "Items", key: "items", sortable: true },
  { title: "Total", key: "total", sortable: true },
  { title: "Payment", key: "payment_mode", sortable: true },
  { title: "Status", key: "payment_status", sortable: true },
  { title: "Actions", key: "actions", sortable: false },
];

// Computed
const today = new Date().toISOString().split("T")[0];
const yesterday = new Date(Date.now() - 86400000).toISOString().split("T")[0];

const allOrders = computed(() => store.AllOrders || []);

const todayOrdersFiltered = computed(() => {
  return allOrders.value.filter((order) => {
    const orderDate = new Date(order.created_at).toISOString().split("T")[0];
    return orderDate === today;
  });
});

const yesterdayOrders = computed(() => {
  return allOrders.value.filter((order) => {
    const orderDate = new Date(order.created_at).toISOString().split("T")[0];
    return orderDate === yesterday;
  });
});

const todayRevenue = computed(() => {
  return todayOrdersFiltered.value.reduce(
    (sum, order) => sum + (order.total || 0),
    0
  );
});

const yesterdayRevenue = computed(() => {
  return yesterdayOrders.value.reduce(
    (sum, order) => sum + (order.total || 0),
    0
  );
});

const todayOrdersCount = computed(() => todayOrdersFiltered.value.length);

const averageOrderValue = computed(() => {
  if (todayOrdersFiltered.value.length === 0) return 0;
  return todayRevenue.value / todayOrdersFiltered.value.length;
});

const yesterdayAvgOrder = computed(() => {
  if (yesterdayOrders.value.length === 0) return 0;
  return yesterdayRevenue.value / yesterdayOrders.value.length;
});

const todayDebtOrders = computed(() => {
  return todayOrdersFiltered.value.filter(
    (order) =>
      (order.payment_status || order.paymentStatus) === "pending" ||
      (order.payment_mode || order.paymentMode) === "debt"
  ).length;
});

const todayDebtAmount = computed(() => {
  return todayOrdersFiltered.value
    .filter(
      (order) => (order.payment_status || order.paymentStatus) === "pending"
    )
    .reduce((sum, order) => sum + (order.total || 0), 0);
});

const filteredOrders = computed(() => {
  return todayOrdersFiltered.value.sort(
    (a, b) =>
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );
});

// Changes
const calculateChange = (current: number, previous: number) => {
  if (previous === 0) return { percent: "+100%", isPositive: true };
  const percent = ((current - previous) / previous) * 100;
  return {
    percent: `${percent >= 0 ? "+" : ""}${percent.toFixed(1)}%`,
    isPositive: percent >= 0,
  };
};

const revenueChange = computed(() =>
  calculateChange(todayRevenue.value, yesterdayRevenue.value)
);
const ordersChange = computed(() =>
  calculateChange(
    todayOrdersFiltered.value.length,
    yesterdayOrders.value.length
  )
);
const avgOrderChange = computed(() =>
  calculateChange(averageOrderValue.value, yesterdayAvgOrder.value)
);

const revenueChangeClass = computed(() =>
  revenueChange.value.isPositive ? "positive" : "negative"
);
const revenueChangeIcon = computed(() =>
  revenueChange.value.isPositive ? "mdi-arrow-up" : "mdi-arrow-down"
);
const revenueChangePercent = computed(() => revenueChange.value.percent);

const ordersChangeClass = computed(() =>
  ordersChange.value.isPositive ? "positive" : "negative"
);
const ordersChangeIcon = computed(() =>
  ordersChange.value.isPositive ? "mdi-arrow-up" : "mdi-arrow-down"
);
const ordersChangePercent = computed(() => ordersChange.value.percent);

const avgOrderChangeClass = computed(() =>
  avgOrderChange.value.isPositive ? "positive" : "negative"
);
const avgOrderChangeIcon = computed(() =>
  avgOrderChange.value.isPositive ? "mdi-arrow-up" : "mdi-arrow-down"
);
const avgOrderChangePercent = computed(() => avgOrderChange.value.percent);

// Payment Breakdown
const paymentBreakdown = computed(() => {
  const breakdown: Record<string, any> = {};

  todayOrdersFiltered.value.forEach((order) => {
    const method = order.payment_mode || order.paymentMode || "Cash";
    if (!breakdown[method]) {
      breakdown[method] = {
        name: method.charAt(0).toUpperCase() + method.slice(1),
        count: 0,
        total: 0,
        icon: getPaymentIcon(method),
        color: getPaymentColor(method),
      };
    }
    breakdown[method].count += 1;
    breakdown[method].total += order.total || 0;
  });

  const total = Object.values(breakdown).reduce(
    (sum: any, b: any) => sum + b.total,
    0
  );

  return Object.values(breakdown).map((b: any) => ({
    ...b,
    percentage: total > 0 ? ((b.total / total) * 100).toFixed(1) : 0,
  }));
});

// Helper Methods
const formatTime = (date: string) => {
  if (!date) return "-";
  return new Date(date).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

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

const getOrderTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    "dine-in": "#2D6A4F",
    takeaway: "#F4A261",
    delivery: "#4A90D9",
    "order-online": "#6B4E71",
  };
  return colors[type?.toLowerCase()] || "#6B7280";
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

const getPaymentIcon = (method: string) => {
  const icons: Record<string, string> = {
    cash: "mdi-cash",
    mpesa: "mdi-cellphone",
    debt: "mdi-account-cash",
    card: "mdi-credit-card",
  };
  return icons[method?.toLowerCase()] || "mdi-cash";
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

// Actions
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

const exportSales = () => {
  // Export today's sales data
  const data = filteredOrders.value.map((order) => ({
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
  link.download = `sales_${today}.json`;
  link.click();
  URL.revokeObjectURL(url);
};

const refreshSales = async () => {
  loading.value = true;
  try {
    await store.getAllOrders();
    updateChart();
  } catch (error) {
    console.error("Error refreshing sales:", error);
  } finally {
    loading.value = false;
  }
};

// Chart
const updateChart = () => {
  if (hourlyChartInstance) {
    hourlyChartInstance.destroy();
    hourlyChartInstance = null;
  }

  const ctx = hourlyChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  // Get data based on period
  let ordersData = todayOrdersFiltered.value;
  if (chartPeriod.value === "Yesterday") {
    ordersData = yesterdayOrders.value;
  } else if (chartPeriod.value === "Last 7 Days") {
    // Get last 7 days
    const last7Days = new Date();
    last7Days.setDate(last7Days.getDate() - 7);
    ordersData = allOrders.value.filter((order) => {
      const orderDate = new Date(order.created_at);
      return orderDate >= last7Days;
    });
  }

  // Group by hour
  const hourlyData = Array.from({ length: 12 }, (_, i) => {
    const hour = i + 8;
    return { hour, total: 0, count: 0 };
  });

  ordersData.forEach((order) => {
    const orderHour = new Date(order.created_at).getHours();
    const index = orderHour - 8;
    if (index >= 0 && index < 12) {
      hourlyData[index].total += order.total || 0;
      hourlyData[index].count += 1;
    }
  });

  const labels = hourlyData.map((d) => `${d.hour}:00`);
  const data = hourlyData.map((d) => d.total);

  hourlyChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Sales (KSh)",
          data: data,
          backgroundColor: "rgba(45, 106, 79, 0.6)",
          borderColor: "#2D6A4F",
          borderWidth: 1,
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (context) => `Revenue: KSh ${context.raw.toLocaleString()}`,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => "KSh " + value.toLocaleString(),
          },
        },
      },
    },
  });
};

// Watchers
watch(chartPeriod, () => {
  updateChart();
});

// Lifecycle
onMounted(async () => {
  await refreshSales();
});
</script>

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
