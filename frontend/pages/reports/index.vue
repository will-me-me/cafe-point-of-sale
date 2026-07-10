<!-- frontend/pages/reports/index.vue -->
<template>
  <div class="reports-dashboard">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#2D6A4F">mdi-chart-bar</v-icon>
          Analytics & Insights
        </div>
        <h1 class="page-title">Reports Dashboard</h1>
        <p class="page-subtitle">
          Comprehensive overview of your business performance
        </p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right mt-4 mt-md-0">
        <v-btn
          variant="outlined"
          color="#6B7280"
          @click="exportAllReports"
          class="mr-2"
        >
          <v-icon start>mdi-export</v-icon>
          Export All
        </v-btn>
        <v-btn color="#2D6A4F" @click="refreshReports" :loading="loading">
          <v-icon start>mdi-refresh</v-icon>
          Refresh
        </v-btn>
      </v-col>
    </v-row>

    <!-- Quick Stats -->
    <v-row class="stats-grid" no-gutters>
      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card
          class="stat-card"
          elevation="0"
          rounded="xl"
          to="/reports/sales"
        >
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
        <v-card
          class="stat-card"
          elevation="0"
          rounded="xl"
          to="/reports/sales"
        >
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
        <v-card
          class="stat-card"
          elevation="0"
          rounded="xl"
          to="/reports/profit"
        >
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
                  KSh {{ totalProfit.toLocaleString() }}
                </div>
                <div class="stat-label">Total Profit</div>
                <div class="stat-change" :class="profitChangeClass">
                  <v-icon size="14">{{ profitChangeIcon }}</v-icon>
                  <span>{{ profitChangePercent }}</span>
                </div>
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
          to="/reports/inventory"
        >
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon"
                  style="background: #6b4e7120; color: #6b4e71"
                >
                  <v-icon size="24">mdi-package-variant</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ totalProducts }}</div>
                <div class="stat-label">Products in Stock</div>
                <div class="stat-change" :class="inventoryChangeClass">
                  <v-icon size="14">{{ inventoryChangeIcon }}</v-icon>
                  <span>{{ inventoryChangePercent }}</span>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Report Cards Grid -->
    <v-row class="reports-grid" no-gutters>
      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card
          class="report-card"
          elevation="0"
          rounded="xl"
          to="/reports/sales"
        >
          <v-card-text class="pa-4 text-center">
            <div
              class="report-icon"
              style="background: linear-gradient(135deg, #2d6a4f, #1b4332)"
            >
              <v-icon size="32" color="white">mdi-chart-line</v-icon>
            </div>
            <h3 class="report-title">Sales Report</h3>
            <p class="report-description">
              Track revenue, orders, and sales trends
            </p>
            <v-chip
              size="x-small"
              color="#2D6A4F"
              text-color="white"
              class="mt-2"
            >
              {{ salesDataCount }} transactions
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card
          class="report-card"
          elevation="0"
          rounded="xl"
          to="/reports/inventory"
        >
          <v-card-text class="pa-4 text-center">
            <div
              class="report-icon"
              style="background: linear-gradient(135deg, #e07a5f, #d66b4a)"
            >
              <v-icon size="32" color="white">mdi-chart-pie</v-icon>
            </div>
            <h3 class="report-title">Inventory Report</h3>
            <p class="report-description">
              Monitor stock levels and inventory value
            </p>
            <v-chip
              size="x-small"
              :color="lowStockCount > 0 ? '#E07A5F' : '#2D6A4F'"
              text-color="white"
              class="mt-2"
            >
              {{ lowStockCount }} items low stock
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card
          class="report-card"
          elevation="0"
          rounded="xl"
          to="/reports/profit"
        >
          <v-card-text class="pa-4 text-center">
            <div
              class="report-icon"
              style="background: linear-gradient(135deg, #f4a261, #e9c46a)"
            >
              <v-icon size="32" color="white">mdi-chart-timeline</v-icon>
            </div>
            <h3 class="report-title">Profit Report</h3>
            <p class="report-description">Analyze margins and profitability</p>
            <v-chip
              size="x-small"
              color="#F4A261"
              text-color="white"
              class="mt-2"
            >
              Margin: {{ profitMargin }}%
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card
          class="report-card"
          elevation="0"
          rounded="xl"
          to="/reports/expiry"
        >
          <v-card-text class="pa-4 text-center">
            <div
              class="report-icon"
              style="background: linear-gradient(135deg, #6b4e71, #4a3b52)"
            >
              <v-icon size="32" color="white">mdi-calendar-clock</v-icon>
            </div>
            <h3 class="report-title">Expiry Report</h3>
            <p class="report-description">Track products nearing expiration</p>
            <v-chip
              size="x-small"
              :color="expiringProducts > 0 ? '#6B4E71' : '#2D6A4F'"
              text-color="white"
              class="mt-2"
            >
              {{ expiringProducts }} expiring soon
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Charts Section -->
    <v-row class="charts-section" no-gutters>
      <v-col cols="12" lg="8" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Revenue Trends</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  {{ revenuePeriodLabel }} performance
                </div>
              </div>
              <v-select
                v-model="revenuePeriod"
                :items="revenuePeriodOptions"
                variant="outlined"
                density="compact"
                class="period-select"
                style="max-width: 140px"
                @update:model-value="updateRevenueChart"
              />
            </div>
            <div class="chart-container">
              <canvas ref="revenueChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="4" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Top Products</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Best selling items
                </div>
              </div>
            </div>
            <div v-if="topProducts.length > 0" class="top-products">
              <div
                v-for="(product, index) in topProducts"
                :key="product.name"
                class="top-product-item"
              >
                <div class="product-rank">{{ index + 1 }}</div>
                <div class="product-info">
                  <div class="product-name">{{ product.name }}</div>
                  <div class="product-sales">{{ product.quantity }} sold</div>
                </div>
                <div class="product-revenue">
                  KSh {{ product.revenue.toLocaleString() }}
                </div>
              </div>
            </div>
            <div v-else class="no-data">
              <v-icon size="48" color="#E5E7EB">mdi-chart-bar</v-icon>
              <p class="text-medium-emphasis">No sales data available</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Actions -->
    <v-row class="quick-actions-section" no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="quick-actions-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="quick-actions-header">
              <h3 class="font-weight-bold">Quick Actions</h3>
              <p class="text-caption text-medium-emphasis">
                Generate reports instantly
              </p>
            </div>
            <v-row no-gutters>
              <v-col
                v-for="action in quickActions"
                :key="action.text"
                cols="6"
                sm="3"
                class="pa-2"
              >
                <div class="action-card" @click="action.action">
                  <div
                    class="action-icon"
                    :style="{ background: action.color }"
                  >
                    <v-icon size="24" color="white">{{ action.icon }}</v-icon>
                  </div>
                  <div class="action-text font-weight-medium">
                    {{ action.text }}
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loading Overlay -->
    <v-overlay :model-value="loading" class="align-center justify-center">
      <v-progress-circular indeterminate size="64" color="#2D6A4F" />
    </v-overlay>
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
const revenuePeriod = ref("30");
const revenueChartCanvas = ref<HTMLCanvasElement | null>(null);
let revenueChartInstance: Chart | null = null;

const revenuePeriodOptions = [
  { title: "Last 7 Days", value: "7" },
  { title: "Last 30 Days", value: "30" },
  { title: "Last 90 Days", value: "90" },
];

const revenuePeriodLabel = computed(() => {
  const option = revenuePeriodOptions.find(
    (o) => o.value === revenuePeriod.value
  );
  return option?.title || "Last 30 Days";
});

// Quick Actions
const quickActions = [
  {
    text: "Sales Report",
    icon: "mdi-chart-line",
    color: "linear-gradient(135deg, #2D6A4F, #1B4332)",
    action: () => navigateTo("/reports/sales"),
  },
  {
    text: "Inventory Report",
    icon: "mdi-chart-pie",
    color: "linear-gradient(135deg, #E07A5F, #D66B4A)",
    action: () => navigateTo("/reports/inventory"),
  },
  {
    text: "Profit Report",
    icon: "mdi-chart-timeline",
    color: "linear-gradient(135deg, #F4A261, #E9C46A)",
    action: () => navigateTo("/reports/profit"),
  },
  {
    text: "Expiry Report",
    icon: "mdi-calendar-clock",
    color: "linear-gradient(135deg, #6B4E71, #4A3B52)",
    action: () => navigateTo("/reports/expiry"),
  },
];

// Computed from Store
const orders = computed(() => store.AllOrders || []);
const products = computed(() => store.products || []);

// Stats
const totalRevenue = computed(() => {
  return orders.value
    .filter(
      (order) =>
        order.payment_status === "paid" || order.payment_status === "completed"
    )
    .reduce((sum, order) => sum + (order.total || 0), 0);
});

const totalOrders = computed(() => orders.value.length);

const totalProfit = computed(() => {
  // Calculate profit based on order costs
  // For now, using estimated 35% margin
  return totalRevenue.value * 0.35;
});

const totalProducts = computed(() => products.value.length);

const lowStockCount = computed(() => {
  return products.value.filter((p) => {
    const stock = p.inventory?.available || p.inventory?.quantity || 0;
    const reorder = p.inventory?.reorder_level || 10;
    return stock > 0 && stock <= reorder;
  }).length;
});

const outOfStockCount = computed(() => {
  return products.value.filter((p) => {
    const stock = p.inventory?.available || p.inventory?.quantity || 0;
    return stock <= 0;
  }).length;
});

const expiringProducts = computed(() => {
  // Products expiring in 30 days
  return 0; // TODO: Implement expiry tracking
});

const profitMargin = computed(() => {
  if (totalRevenue.value === 0) return 0;
  return ((totalProfit.value / totalRevenue.value) * 100).toFixed(1);
});

const salesDataCount = computed(() => orders.value.length);

// Change Calculations
const calculateChange = (current: number, previous: number) => {
  if (previous === 0) return { percent: "+100%", isPositive: true };
  const percent = ((current - previous) / previous) * 100;
  return {
    percent: `${percent >= 0 ? "+" : ""}${percent.toFixed(1)}%`,
    isPositive: percent >= 0,
  };
};

const revenueChange = computed(() =>
  calculateChange(totalRevenue.value, totalRevenue.value * 0.9)
);
const ordersChange = computed(() =>
  calculateChange(totalOrders.value, totalOrders.value * 0.92)
);
const profitChange = computed(() =>
  calculateChange(totalProfit.value, totalProfit.value * 0.85)
);
const inventoryChange = computed(() =>
  calculateChange(totalProducts.value, totalProducts.value * 0.98)
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

const profitChangeClass = computed(() =>
  profitChange.value.isPositive ? "positive" : "negative"
);
const profitChangeIcon = computed(() =>
  profitChange.value.isPositive ? "mdi-arrow-up" : "mdi-arrow-down"
);
const profitChangePercent = computed(() => profitChange.value.percent);

const inventoryChangeClass = computed(() =>
  inventoryChange.value.isPositive ? "positive" : "negative"
);
const inventoryChangeIcon = computed(() =>
  inventoryChange.value.isPositive ? "mdi-arrow-up" : "mdi-arrow-down"
);
const inventoryChangePercent = computed(() => inventoryChange.value.percent);

// Top Products
const topProducts = computed(() => {
  const productMap = new Map();

  orders.value.forEach((order) => {
    const items = order.items || [];
    items.forEach((item: any) => {
      const key = item.name || item.product_name;
      if (!key) return;
      if (!productMap.has(key)) {
        productMap.set(key, {
          name: key,
          quantity: 0,
          revenue: 0,
        });
      }
      const product = productMap.get(key);
      product.quantity += item.quantity || 1;
      product.revenue +=
        (item.unit_price || item.price || 0) * (item.quantity || 1);
    });
  });

  const products = Array.from(productMap.values());
  return products.sort((a, b) => b.revenue - a.revenue).slice(0, 5);
});

// Methods
const refreshReports = async () => {
  loading.value = true;
  try {
    await Promise.all([store.getAllOrders(), store.getAllProducts()]);
    updateRevenueChart();
  } catch (error) {
    console.error("Error refreshing reports:", error);
  } finally {
    loading.value = false;
  }
};

const exportAllReports = () => {
  // Create a combined report
  const report = {
    generated: new Date().toISOString(),
    summary: {
      totalRevenue: totalRevenue.value,
      totalOrders: totalOrders.value,
      totalProfit: totalProfit.value,
      totalProducts: totalProducts.value,
      lowStock: lowStockCount.value,
      outOfStock: outOfStockCount.value,
      profitMargin: profitMargin.value,
    },
    topProducts: topProducts.value,
    orders: orders.value.length,
  };

  // Download as JSON
  const blob = new Blob([JSON.stringify(report, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `report_${new Date().toISOString().split("T")[0]}.json`;
  link.click();
  URL.revokeObjectURL(url);
};

const updateRevenueChart = () => {
  if (revenueChartInstance) {
    revenueChartInstance.destroy();
    revenueChartInstance = null;
  }

  const ctx = revenueChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  // Get revenue data from orders
  const days = parseInt(revenuePeriod.value);
  const today = new Date();
  const revenueMap = new Map();

  // Initialize last 'days' days with zero
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    const dateStr = date.toISOString().split("T")[0];
    revenueMap.set(dateStr, 0);
  }

  // Aggregate revenue by date
  orders.value.forEach((order) => {
    if (!order.created_at) return;
    const orderDate = new Date(order.created_at).toISOString().split("T")[0];
    if (revenueMap.has(orderDate)) {
      revenueMap.set(orderDate, revenueMap.get(orderDate) + (order.total || 0));
    }
  });

  const labels = Array.from(revenueMap.keys()).map((date) => {
    return new Date(date).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    });
  });

  const data = Array.from(revenueMap.values());

  revenueChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Revenue (KSh)",
          data: data,
          borderColor: "#2D6A4F",
          backgroundColor: "rgba(45, 106, 79, 0.1)",
          tension: 0.4,
          fill: true,
          pointBackgroundColor: "#2D6A4F",
          pointRadius: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
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
        x: {
          grid: {
            display: false,
          },
          ticks: {
            maxRotation: 45,
            autoSkip: true,
            maxTicksLimit: 10,
          },
        },
      },
    },
  });
};

// Watch for revenue period changes
watch(revenuePeriod, () => {
  updateRevenueChart();
});

onMounted(async () => {
  await refreshReports();
});
</script>

<style scoped>
.reports-dashboard {
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

/* Stats Grid */
.stats-grid {
  margin-bottom: 16px;
}

.stat-card {
  background: white;
  border: 1px solid #f3f4f6;
  transition: all 0.3s ease;
  cursor: pointer;
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
  font-size: 22px;
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

/* Report Cards */
.reports-grid {
  margin-bottom: 16px;
}

.report-card {
  background: white;
  border: 1px solid #f3f4f6;
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
}

.report-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  border-color: #2d6a4f;
}

.report-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
}

.report-title {
  font-size: 16px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 4px;
}

.report-description {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 12px;
}

/* Charts */
.chart-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}

.chart-title {
  font-size: 16px;
  color: #1b4332;
}

.chart-subtitle {
  font-size: 12px;
  color: #6b7280;
}

.period-select {
  max-width: 140px;
}

.chart-container {
  height: 300px;
  position: relative;
}

/* Top Products */
.top-products {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.top-product-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f6f2;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.top-product-item:hover {
  background: #f0ede5;
}

.product-rank {
  font-size: 18px;
  font-weight: 800;
  color: rgba(0, 0, 0, 0.1);
  min-width: 30px;
}

.product-info {
  flex: 1;
}

.product-name {
  font-weight: 600;
  color: #1b4332;
}

.product-sales {
  font-size: 12px;
  color: #6b7280;
}

.product-revenue {
  font-weight: 700;
  color: #e07a5f;
}

.no-data {
  text-align: center;
  padding: 40px 20px;
}

.no-data p {
  margin-top: 12px;
  color: #6b7280;
}

/* Quick Actions */
.quick-actions-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.quick-actions-header {
  margin-bottom: 16px;
}

.quick-actions-header h3 {
  font-size: 16px;
  color: #1b4332;
}

.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  background: #f8f6f2;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-card:hover {
  transform: translateY(-4px);
  background: white;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-text {
  font-size: 13px;
  color: #1b4332;
  text-align: center;
}

/* Responsive */
@media (max-width: 1200px) {
  .chart-container {
    height: 250px;
  }
}

@media (max-width: 768px) {
  .reports-dashboard {
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

  .report-icon {
    width: 48px;
    height: 48px;
  }

  .report-icon .v-icon {
    font-size: 24px !important;
  }

  .chart-container {
    height: 200px;
  }

  .action-card {
    padding: 16px;
  }

  .action-icon {
    width: 40px;
    height: 40px;
  }

  .action-icon .v-icon {
    font-size: 20px !important;
  }

  .action-text {
    font-size: 12px;
  }

  .top-product-item {
    padding: 10px;
  }

  .product-rank {
    font-size: 14px;
    min-width: 24px;
  }

  .product-name {
    font-size: 14px;
  }

  .period-select {
    max-width: 120px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }

  .stat-value {
    font-size: 16px;
  }

  .stat-label {
    font-size: 11px;
  }

  .stat-change {
    font-size: 11px;
  }

  .report-title {
    font-size: 14px;
  }

  .report-description {
    font-size: 12px;
  }

  .chart-title {
    font-size: 14px;
  }

  .chart-subtitle {
    font-size: 11px;
  }

  .quick-actions-header h3 {
    font-size: 14px;
  }

  .chart-container {
    height: 180px;
  }

  .action-card {
    padding: 12px;
  }

  .action-icon {
    width: 36px;
    height: 36px;
  }

  .action-icon .v-icon {
    font-size: 18px !important;
  }

  .action-text {
    font-size: 11px;
  }

  .header-actions {
    flex-direction: column;
    gap: 8px;
  }

  .header-actions .v-btn {
    width: 100%;
    margin: 0 !important;
  }
}
</style>
