<!-- frontend/pages/reports/sales/index.vue -->
<template>
  <div class="sales-report-container">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#2D6A4F">mdi-chart-line</v-icon>
          Reports
        </div>
        <h1 class="page-title">Sales Report</h1>
        <p class="page-subtitle">Track revenue, orders, and sales trends</p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right mt-4 mt-md-0">
        <v-btn
          variant="outlined"
          color="#6B7280"
          @click="exportReport"
          class="mr-2"
        >
          <v-icon start>mdi-export</v-icon>
          Export
        </v-btn>
        <v-btn color="#2D6A4F" @click="refreshData" :loading="loading">
          <v-icon start>mdi-refresh</v-icon>
          Refresh
        </v-btn>
      </v-col>
    </v-row>

    <!-- Period Selector -->
    <v-card class="period-card mb-4" elevation="0" rounded="xl">
      <v-card-text class="pa-4">
        <v-row align="center" no-gutters>
          <v-col cols="12" sm="6" md="4">
            <div class="period-toggle">
              <v-btn-toggle
                v-model="periodType"
                color="#2D6A4F"
                group
                mandatory
                density="compact"
                class="period-toggle-group"
              >
                <v-btn value="daily" size="small">Daily</v-btn>
                <v-btn value="weekly" size="small">Weekly</v-btn>
                <v-btn value="monthly" size="small">Monthly</v-btn>
              </v-btn-toggle>
            </div>
          </v-col>
          <v-col cols="12" sm="6" md="4" class="mt-2 mt-sm-0">
            <v-text-field
              v-model="dateRange"
              type="date"
              label="Select Date"
              variant="outlined"
              density="compact"
              hide-details
              class="date-picker-field"
            />
          </v-col>
          <v-col cols="12" md="4" class="mt-2 mt-md-0 text-md-right">
            <span class="text-caption text-medium-emphasis">
              {{ dateRangeLabel }}
            </span>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

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
                  KSh {{ totalRevenue.toLocaleString() }}
                </div>
                <div class="stat-label">Total Revenue</div>
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
                  <v-icon size="24">mdi-cart-outline</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ totalOrders }}</div>
                <div class="stat-label">Total Orders</div>
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
                  style="background: #6b4e7120; color: #6b4e71"
                >
                  <v-icon size="24">mdi-cash</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ totalItems }}</div>
                <div class="stat-label">Total Items Sold</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Revenue Chart -->
    <v-row no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Revenue Trend</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  {{ periodTypeLabel }} revenue over time
                </div>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="revenueChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Payment Method Breakdown -->
    <v-row no-gutters>
      <v-col cols="12" md="6" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Payment Methods</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Distribution by payment type
                </div>
              </div>
            </div>
            <div class="chart-container payment-chart">
              <canvas ref="paymentChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Order Types</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Distribution by order type
                </div>
              </div>
            </div>
            <div class="chart-container payment-chart">
              <canvas ref="orderTypeChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Sales Table -->
    <v-row no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="table-card" elevation="0" rounded="xl">
          <v-card-text class="pa-0">
            <div class="table-header pa-4">
              <span class="table-title font-weight-bold"
                >Sales Transactions</span
              >
              <span class="table-count text-caption text-medium-emphasis">
                {{ filteredOrders.length }} transactions
              </span>
            </div>
            <v-data-table
              :headers="headers"
              :items="filteredOrders"
              :loading="loading"
              :items-per-page="10"
              class="sales-table"
              item-value="id"
            >
              <template v-slot:item.receiptNumber="{ item }">
                <span class="receipt-cell font-weight-medium"
                  >#{{ item.receipt_number }}</span
                >
              </template>

              <template v-slot:item.customer_name="{ item }">
                {{ item.customer_name || "Guest" }}
              </template>

              <template v-slot:item.total="{ item }">
                <span class="amount-cell"
                  >KSh {{ (item.total || 0).toFixed(2) }}</span
                >
              </template>

              <template v-slot:item.payment_mode="{ item }">
                <v-chip
                  :color="getPaymentColor(item.payment_mode)"
                  size="x-small"
                  text-color="white"
                >
                  {{ formatPaymentMode(item.payment_mode) }}
                </v-chip>
              </template>

              <template v-slot:item.payment_status="{ item }">
                <v-chip
                  :color="getStatusColor(item.payment_status)"
                  size="x-small"
                  text-color="white"
                >
                  {{ formatStatus(item.payment_status) }}
                </v-chip>
              </template>

              <template v-slot:item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import Chart from "chart.js/auto";
import { usePosStore } from "~/stores/pos";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const store = usePosStore();
const loading = ref(false);
const periodType = ref("daily");
const dateRange = ref(new Date().toISOString().split("T")[0]);

const revenueChartCanvas = ref<HTMLCanvasElement | null>(null);
const paymentChartCanvas = ref<HTMLCanvasElement | null>(null);
const orderTypeChartCanvas = ref<HTMLCanvasElement | null>(null);

let revenueChartInstance: Chart | null = null;
let paymentChartInstance: Chart | null = null;
let orderTypeChartInstance: Chart | null = null;

// Table Headers
const headers = [
  { title: "Receipt #", key: "receiptNumber", sortable: true },
  { title: "Customer", key: "customer_name", sortable: true },
  { title: "Items", key: "total_items", sortable: true },
  { title: "Total", key: "total", sortable: true },
  { title: "Payment", key: "payment_mode", sortable: true },
  { title: "Status", key: "payment_status", sortable: true },
  { title: "Date", key: "created_at", sortable: true },
];

// Computed
const orders = computed(() => store.AllOrders || []);

const filteredOrders = computed(() => {
  let filtered = [...orders.value];

  const selectedDate = new Date(dateRange.value);

  if (periodType.value === "daily") {
    filtered = filtered.filter((order) => {
      const orderDate = new Date(order.created_at).toISOString().split("T")[0];
      return orderDate === dateRange.value;
    });
  } else if (periodType.value === "weekly") {
    const weekStart = new Date(selectedDate);
    weekStart.setDate(selectedDate.getDate() - selectedDate.getDay());
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);

    filtered = filtered.filter((order) => {
      const orderDate = new Date(order.created_at);
      return orderDate >= weekStart && orderDate <= weekEnd;
    });
  } else if (periodType.value === "monthly") {
    filtered = filtered.filter((order) => {
      const orderDate = new Date(order.created_at);
      return (
        orderDate.getMonth() === selectedDate.getMonth() &&
        orderDate.getFullYear() === selectedDate.getFullYear()
      );
    });
  }

  return filtered;
});

const totalRevenue = computed(() => {
  return filteredOrders.value.reduce(
    (sum, order) => sum + (order.total || 0),
    0
  );
});

const totalOrders = computed(() => filteredOrders.value.length);

const averageOrderValue = computed(() => {
  if (totalOrders.value === 0) return 0;
  return totalRevenue.value / totalOrders.value;
});

const totalItems = computed(() => {
  return filteredOrders.value.reduce((sum, order) => {
    const items = order.items || [];
    return (
      sum + items.reduce((itemSum, item) => itemSum + (item.quantity || 0), 0)
    );
  }, 0);
});

const dateRangeLabel = computed(() => {
  const date = new Date(dateRange.value);
  if (periodType.value === "daily") {
    return date.toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  } else if (periodType.value === "weekly") {
    const weekStart = new Date(date);
    weekStart.setDate(date.getDate() - date.getDay());
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);
    return `Week of ${weekStart.toLocaleDateString()} - ${weekEnd.toLocaleDateString()}`;
  } else {
    return date.toLocaleDateString("en-US", { month: "long", year: "numeric" });
  }
});

const periodTypeLabel = computed(() => {
  return periodType.value.charAt(0).toUpperCase() + periodType.value.slice(1);
});

// Helper Methods
const formatDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
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

const getPaymentColor = (mode: string) => {
  const colors: Record<string, string> = {
    cash: "#2D6A4F",
    mpesa: "#4A90D9",
    debt: "#E07A5F",
    card: "#6B4E71",
  };
  return colors[mode] || "#6B7280";
};

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    paid: "#2D6A4F",
    completed: "#2D6A4F",
    pending: "#F4A261",
    overdue: "#E07A5F",
    cancelled: "#6B7280",
  };
  return colors[status] || "#6B7280";
};

// Chart Methods
const updateRevenueChart = () => {
  if (revenueChartInstance) {
    revenueChartInstance.destroy();
    revenueChartInstance = null;
  }

  const ctx = revenueChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  const labels: string[] = [];
  const data: number[] = [];

  if (periodType.value === "daily") {
    // Show hourly or by hour range
    const hours = Array.from({ length: 12 }, (_, i) => {
      const h = i + 8;
      return `${h}:00`;
    });
    const hourlyData = hours.map(() => 0);

    filteredOrders.value.forEach((order) => {
      const hour = new Date(order.created_at).getHours();
      const index = hour - 8;
      if (index >= 0 && index < 12) {
        hourlyData[index] += order.total || 0;
      }
    });

    labels.push(...hours);
    data.push(...hourlyData);
  } else {
    // Weekly or Monthly
    const revenueMap = new Map();

    filteredOrders.value.forEach((order) => {
      const dateStr = new Date(order.created_at).toISOString().split("T")[0];
      revenueMap.set(
        dateStr,
        (revenueMap.get(dateStr) || 0) + (order.total || 0)
      );
    });

    const sortedDates = Array.from(revenueMap.keys()).sort();
    labels.push(
      ...sortedDates.map((d) =>
        new Date(d).toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
        })
      )
    );
    data.push(...sortedDates.map((d) => revenueMap.get(d)));
  }

  revenueChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Revenue (KSh)",
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

const updatePaymentChart = () => {
  if (paymentChartInstance) {
    paymentChartInstance.destroy();
    paymentChartInstance = null;
  }

  const ctx = paymentChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  const paymentMap = new Map();

  filteredOrders.value.forEach((order) => {
    const mode = order.payment_mode || "cash";
    paymentMap.set(mode, (paymentMap.get(mode) || 0) + 1);
  });

  const colors = {
    cash: "#2D6A4F",
    mpesa: "#4A90D9",
    debt: "#E07A5F",
    card: "#6B4E71",
  };

  const labels = Array.from(paymentMap.keys());
  const data = Array.from(paymentMap.values());
  const backgroundColors = labels.map(
    (label) => colors[label as keyof typeof colors] || "#6B7280"
  );

  paymentChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels.map((l) => formatPaymentMode(l)),
      datasets: [
        {
          data: data,
          backgroundColor: backgroundColors,
          borderWidth: 2,
          borderColor: "white",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            padding: 12,
            usePointStyle: true,
            pointStyle: "circle",
          },
        },
      },
    },
  });
};

const updateOrderTypeChart = () => {
  if (orderTypeChartInstance) {
    orderTypeChartInstance.destroy();
    orderTypeChartInstance = null;
  }

  const ctx = orderTypeChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  const typeMap = new Map();

  filteredOrders.value.forEach((order) => {
    const type = order.order_type || "takeaway";
    typeMap.set(type, (typeMap.get(type) || 0) + 1);
  });

  const colors = {
    "dine-in": "#2D6A4F",
    takeaway: "#F4A261",
    delivery: "#4A90D9",
    "order-online": "#6B4E71",
  };

  const labels = Array.from(typeMap.keys());
  const data = Array.from(typeMap.values());
  const backgroundColors = labels.map(
    (label) => colors[label as keyof typeof colors] || "#6B7280"
  );

  orderTypeChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels.map((l) => l.replace("-", " ").toUpperCase()),
      datasets: [
        {
          data: data,
          backgroundColor: backgroundColors,
          borderWidth: 2,
          borderColor: "white",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            padding: 12,
            usePointStyle: true,
            pointStyle: "circle",
          },
        },
      },
    },
  });
};

const updateCharts = () => {
  setTimeout(() => {
    updateRevenueChart();
    updatePaymentChart();
    updateOrderTypeChart();
  }, 100);
};

// Methods
const refreshData = async () => {
  loading.value = true;
  try {
    await store.getAllOrders();
    updateCharts();
  } catch (error) {
    console.error("Error refreshing data:", error);
  } finally {
    loading.value = false;
  }
};

const exportReport = () => {
  const report = {
    generated: new Date().toISOString(),
    period: {
      type: periodType.value,
      date: dateRange.value,
      label: dateRangeLabel.value,
    },
    summary: {
      totalRevenue: totalRevenue.value,
      totalOrders: totalOrders.value,
      averageOrderValue: averageOrderValue.value,
      totalItems: totalItems.value,
    },
    transactions: filteredOrders.value.map((order) => ({
      receipt: order.receiptNumber,
      customer: order.customer_name || "Guest",
      total: order.total,
      payment: order.payment_mode,
      status: order.payment_status,
      date: order.created_at,
    })),
  };

  const blob = new Blob([JSON.stringify(report, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `sales_report_${new Date().toISOString().split("T")[0]}.json`;
  link.click();
  URL.revokeObjectURL(url);
};

// Watchers
watch([periodType, dateRange], () => {
  updateCharts();
});

// Lifecycle
onMounted(async () => {
  await refreshData();
});
</script>

<style scoped>
.sales-report-container {
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

.period-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.period-toggle-group {
  background: #f8f6f2;
  border-radius: 8px;
}

.period-toggle-group :deep(.v-btn) {
  text-transform: none;
  font-weight: 500;
}

.period-toggle-group :deep(.v-btn--selected) {
  background: #2d6a4f !important;
  color: white !important;
}

.date-picker-field {
  max-width: 200px;
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

.chart-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-title {
  font-size: 16px;
  color: #1b4332;
}

.chart-subtitle {
  font-size: 12px;
  color: #6b7280;
}

.chart-container {
  height: 250px;
  position: relative;
}

.payment-chart {
  height: 200px;
}

.table-card {
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

.sales-table :deep(.v-data-table__th) {
  background: #f8f6f2;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

.receipt-cell {
  color: #1b4332;
}

.amount-cell {
  font-weight: 600;
  color: #e07a5f;
}

@media (max-width: 768px) {
  .sales-report-container {
    padding: 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .stat-value {
    font-size: 16px;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
  }

  .chart-container {
    height: 200px;
  }

  .payment-chart {
    height: 180px;
  }

  .period-toggle-group {
    width: 100%;
  }

  .period-toggle-group :deep(.v-btn) {
    flex: 1;
  }

  .date-picker-field {
    max-width: 100%;
  }

  .sales-table :deep(.v-data-table__th),
  .sales-table :deep(.v-data-table__td) {
    padding: 8px 12px !important;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }

  .stat-value {
    font-size: 14px;
  }

  .stat-label {
    font-size: 11px;
  }

  .chart-title {
    font-size: 14px;
  }

  .chart-container {
    height: 180px;
  }

  .payment-chart {
    height: 160px;
  }

  .table-title {
    font-size: 14px;
  }
}
</style>
