<!-- frontend/pages/reports/index.vue -->
<template>
  <div class="reports-container">
    <!-- Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">Analytics & Insights</div>
        <h1 class="page-title">Reports</h1>
        <p class="page-subtitle">
          Track your coffee shop performance with detailed analytics
        </p>
      </div>
      <div class="header-actions">
        <v-btn variant="outlined" class="export-btn" @click="exportReport">
          <v-icon start>mdi-download</v-icon>
          Export Report
        </v-btn>
        <v-btn class="schedule-btn" @click="showScheduleDialog = true">
          <v-icon start>mdi-calendar-clock</v-icon>
          Schedule Report
        </v-btn>
      </div>
    </div>

    <!-- Date Range Selector -->
    <div class="date-range-section">
      <div class="date-range-card">
        <div class="date-presets">
          <button
            v-for="preset in datePresets"
            :key="preset.value"
            :class="['preset-btn', { active: selectedPreset === preset.value }]"
            @click="setDatePreset(preset.value)"
          >
            {{ preset.label }}
          </button>
        </div>
        <div class="date-picker-group">
          <div class="date-picker-wrapper">
            <v-icon class="date-icon">mdi-calendar-start</v-icon>
            <input type="date" v-model="dateRange.start" class="date-input" />
          </div>
          <span class="date-separator">to</span>
          <div class="date-picker-wrapper">
            <v-icon class="date-icon">mdi-calendar-end</v-icon>
            <input type="date" v-model="dateRange.end" class="date-input" />
          </div>
          <v-btn class="apply-btn" @click="fetchReportData">
            <v-icon start>mdi-refresh</v-icon>
            Apply
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading your reports...</p>
    </div>

    <div v-else>
      <!-- Key Metrics -->
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-header">
            <div
              class="metric-icon"
              style="background: linear-gradient(135deg, #2d6a4f, #1b4332)"
            >
              <v-icon size="24" color="white">mdi-currency-usd</v-icon>
            </div>
            <div class="metric-trend" :class="revenueTrendClass">
              <v-icon size="16">{{ revenueTrendIcon }}</v-icon>
              <span>{{ revenueTrendValue }}</span>
            </div>
          </div>
          <div class="metric-value">ksh{{ totalRevenue.toLocaleString() }}</div>
          <div class="metric-title">Total Revenue</div>
          <div class="metric-subtitle">vs previous period</div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <div
              class="metric-icon"
              style="background: linear-gradient(135deg, #e07a5f, #d66b4a)"
            >
              <v-icon size="24" color="white">mdi-cart-outline</v-icon>
            </div>
            <div class="metric-trend" :class="ordersTrendClass">
              <v-icon size="16">{{ ordersTrendIcon }}</v-icon>
              <span>{{ ordersTrendValue }}</span>
            </div>
          </div>
          <div class="metric-value">{{ totalOrders }}</div>
          <div class="metric-title">Total Orders</div>
          <div class="metric-subtitle">vs previous period</div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <div
              class="metric-icon"
              style="background: linear-gradient(135deg, #f4a261, #e9c46a)"
            >
              <v-icon size="24" color="white">mdi-chart-line</v-icon>
            </div>
            <div class="metric-trend" :class="avgOrderTrendClass">
              <v-icon size="16">{{ avgOrderTrendIcon }}</v-icon>
              <span>{{ avgOrderTrendValue }}</span>
            </div>
          </div>
          <div class="metric-value">ksh{{ averageOrderValue.toFixed(2) }}</div>
          <div class="metric-title">Average Order</div>
          <div class="metric-subtitle">vs previous period</div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <div
              class="metric-icon"
              style="background: linear-gradient(135deg, #6b4e71, #4a3b52)"
            >
              <v-icon size="24" color="white">mdi-coffee</v-icon>
            </div>
            <div class="metric-trend" :class="itemsTrendClass">
              <v-icon size="16">{{ itemsTrendIcon }}</v-icon>
              <span>{{ itemsTrendValue }}</span>
            </div>
          </div>
          <div class="metric-value">{{ totalItemsSold }}</div>
          <div class="metric-title">Items Sold</div>
          <div class="metric-subtitle">vs previous period</div>
        </div>
      </div>

      <!-- Revenue Chart -->
      <div class="chart-row">
        <v-card class="chart-card" elevation="0">
          <div class="chart-header">
            <!-- <div>
              <div class="chart-title">Revenue Overview</div>
              <div class="chart-subtitle">Daily revenue trend</div>
            </div> -->
            <!-- <div class="chart-controls">
              <button
                v-for="chartType in chartTypes"
                :key="chartType.value"
                :class="[
                  'chart-type-btn',
                  { active: selectedChartType === chartType.value },
                ]"
                @click="selectedChartType = chartType.value"
              >
                {{ chartType.label }}
              </button>
            </div> -->
          </div>
          <div class="chart-container" style="height: 420px">
            <RevenueChart
              :data="dailyRevenueData"
              :labels="dailyRevenueLabels"
              :type="selectedChartType"
            />
          </div>
        </v-card>
      </div>

      <!-- Sales & Products Row -->
      <div class="two-column-row">
        <!-- Top Selling Products -->
        <v-card class="products-card" elevation="0">
          <div class="card-header">
            <div>
              <div class="card-title">Top Selling Products</div>
              <div class="card-subtitle">Best performers this period</div>
            </div>
            <select v-model="topProductsLimit" class="limit-select">
              <option :value="5">Top 5</option>
              <option :value="10">Top 10</option>
              <option :value="15">Top 15</option>
            </select>
          </div>
          <div class="products-list">
            <div
              v-for="(product, index) in topProductsData.slice(
                0,
                topProductsLimit
              )"
              :key="product.name"
              class="product-row"
            >
              <div class="product-rank">
                <div class="rank-badge" :class="getRankClass(index + 1)">
                  {{ index + 1 }}
                </div>
              </div>
              <div class="product-info">
                <div class="product-name">{{ product.name }}</div>
                <div class="product-category">{{ product.category }}</div>
              </div>
              <div class="product-stats">
                <div class="product-quantity">{{ product.quantity }} sold</div>
                <div class="product-revenue">
                  ksh {{ product.revenue.toLocaleString() }}
                </div>
              </div>
              <div class="product-progress">
                <div
                  class="progress-bar"
                  :style="{
                    width: `${product.percentage}%`,
                    background: getProgressColor(index),
                  }"
                ></div>
              </div>
            </div>
          </div>
        </v-card>

        <!-- Category Distribution -->
        <v-card class="distribution-card" elevation="0">
          <div class="card-header">
            <div>
              <div class="card-title">Sales by Category</div>
              <div class="card-subtitle">Revenue distribution</div>
            </div>
          </div>
          <div
            class="distribution-container"
            style="height: 600px; border-radius: 16px"
          >
            <ClientOnly>
              <DoughnutChart
                :data="categoryStatsData.map((c) => c.revenue)"
                :labels="categoryStatsData.map((c) => c.name)"
                :colors="categoryStatsData.map((c) => c.color)"
              />
            </ClientOnly>
          </div>
          <div
            class="category-legend"
            style="padding-top: 16px; margin-top: 16px"
          >
            <div
              v-for="category in categoryStatsData"
              :key="category.name"
              class="legend-item"
            >
              <div
                class="legend-color"
                :style="{ background: category.color }"
              ></div>
              <div class="legend-name">{{ category.name }}</div>
              <div class="legend-value">{{ category.percentage }}%</div>
              <div class="legend-amount">
                ksh {{ category.revenue.toLocaleString() }}
              </div>
            </div>
          </div>
        </v-card>
      </div>

      <!-- Hourly & Order Type Row -->
      <div class="two-column-row">
        <!-- Hourly Sales Heatmap -->
        <v-card class="hourly-card" elevation="0">
          <div class="card-header">
            <div>
              <div class="card-title">Hourly Sales</div>
              <div class="card-subtitle">Peak hours analysis</div>
            </div>
          </div>
          <div class="hourly-bars">
            <div
              v-for="hour in hourlySalesData"
              :key="hour.hour"
              class="hour-bar-wrapper"
            >
              <div
                class="hour-bar"
                :style="{
                  height: `${hour.percentage}%`,
                  background: getHourColor(hour.percentage),
                }"
              >
                <span class="hour-value">ksh{{ hour.revenue }}</span>
              </div>
              <div class="hour-label">{{ hour.hour }}</div>
            </div>
          </div>
        </v-card>

        <!-- Order Type Distribution -->
        <v-card class="ordertype-card" elevation="0">
          <div class="card-header">
            <div>
              <div class="card-title">Order Types</div>
              <div class="card-subtitle">Channel performance</div>
            </div>
          </div>
          <div class="ordertype-stats">
            <div
              v-for="type in orderTypeStatsData"
              :key="type.name"
              class="ordertype-item"
            >
              <div class="ordertype-header">
                <div class="ordertype-name">
                  <span class="ordertype-icon">{{ type.icon }}</span>
                  {{ type.name }}
                </div>
                <div class="ordertype-percentage">{{ type.percentage }}%</div>
              </div>
              <div class="ordertype-progress">
                <div
                  class="progress-bar-fill"
                  :style="{
                    width: `${type.percentage}%`,
                    background: type.color,
                  }"
                ></div>
              </div>
              <div class="ordertype-details">
                <span>{{ type.count }} orders</span>
                <span>ksh {{ type.revenue.toLocaleString() }}</span>
              </div>
            </div>
          </div>
        </v-card>
      </div>

      <!-- Detailed Sales Table -->
      <v-card class="sales-table-card" elevation="0">
        <div class="card-header">
          <div>
            <div class="card-title">Daily Sales Breakdown</div>
            <div class="card-subtitle">Detailed daily performance</div>
          </div>
          <div class="table-controls">
            <div class="search-wrapper">
              <v-icon size="16">mdi-magnify</v-icon>
              <input
                v-model="tableSearch"
                placeholder="Search..."
                class="table-search"
              />
            </div>
          </div>
        </div>
        <div class="table-container">
          <table class="sales-table">
            <thead>
              <tr>
                <th @click="sortBy('date')">
                  Date
                  <v-icon size="14">{{
                    sortKey === "date"
                      ? sortOrder === "asc"
                        ? "mdi-arrow-up"
                        : "mdi-arrow-down"
                      : "mdi-arrow-up-down"
                  }}</v-icon>
                </th>
                <th @click="sortBy('orders')">Orders</th>
                <th @click="sortBy('revenue')">Revenue</th>
                <th @click="sortBy('avgOrder')">Avg Order</th>
                <th @click="sortBy('items')">Items Sold</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="day in paginatedSalesData" :key="day.date">
                <td class="date-cell">{{ formatDate(day.date) }}</td>
                <td>{{ day.orders }}</td>
                <td class="revenue-cell">
                  ksh {{ day.revenue.toLocaleString() }}
                </td>
                <td>ksh {{ day.avgOrder.toFixed(2) }}</td>
                <td>{{ day.itemsSold }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="pagination-section">
          <div class="items-per-page">
            <span>Show</span>
            <select v-model="itemsPerPage">
              <option :value="5">5</option>
              <option :value="10">10</option>
              <option :value="20">20</option>
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

      <!-- Export Options -->
      <div class="export-options">
        <div class="export-header">
          <h3>Export Options</h3>
          <p>Download your reports in various formats</p>
        </div>
        <div class="export-buttons">
          <button class="export-option" @click="exportPDF">
            <div class="export-icon" style="background: #e07a5f20">
              <v-icon color="#E07A5F" size="28">mdi-file-pdf-box</v-icon>
            </div>
            <div class="export-info">
              <div class="export-title">PDF Report</div>
              <div class="export-desc">Download as PDF document</div>
            </div>
          </button>
          <button class="export-option" @click="exportExcel">
            <div class="export-icon" style="background: #2d6a4f20">
              <v-icon color="#2D6A4F" size="28">mdi-microsoft-excel</v-icon>
            </div>
            <div class="export-info">
              <div class="export-title">Excel Spreadsheet</div>
              <div class="export-desc">Export for data analysis</div>
            </div>
          </button>
          <button class="export-option" @click="exportCSV">
            <div class="export-icon" style="background: #f4a26120">
              <v-icon color="#F4A261" size="28">mdi-file-delimited</v-icon>
            </div>
            <div class="export-info">
              <div class="export-title">CSV File</div>
              <div class="export-desc">Compatible with any software</div>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Schedule Report Dialog -->
    <v-dialog v-model="showScheduleDialog" max-width="500">
      <v-card class="schedule-dialog">
        <div class="dialog-header">
          <h2>Schedule Report</h2>
          <v-btn icon variant="text" @click="showScheduleDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <div class="dialog-content">
          <div class="form-group">
            <label>Report Type</label>
            <select v-model="schedule.type" class="form-select">
              <option value="sales">Sales Report</option>
              <option value="products">Products Report</option>
              <option value="inventory">Inventory Report</option>
            </select>
          </div>
          <div class="form-group">
            <label>Frequency</label>
            <select v-model="schedule.frequency" class="form-select">
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
          <div class="form-group">
            <label>Recipients (Email)</label>
            <input
              type="email"
              v-model="schedule.email"
              placeholder="admin@coffee.com"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label>Format</label>
            <div class="radio-group">
              <label>
                <input type="radio" value="pdf" v-model="schedule.format" /> PDF
              </label>
              <label>
                <input type="radio" value="excel" v-model="schedule.format" />
                Excel
              </label>
            </div>
          </div>
        </div>
        <div class="dialog-actions">
          <v-btn variant="text" @click="showScheduleDialog = false"
            >Cancel</v-btn
          >
          <v-btn color="#2D6A4F" @click="scheduleReport">Schedule Report</v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Toast Notification -->
    <v-snackbar
      v-model="showToast"
      :timeout="3000"
      :color="toastColor"
      location="top"
      class="custom-toast"
    >
      <div class="toast-content text-button" style="background: transparent">
        <v-icon>{{ toastIcon }}</v-icon>
        <span>{{ toastMessage }}</span>
      </div>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { usePosStore } from "~/stores/pos";
import RevenueChart from "~/components/charts/RevenueChart.vue";
import DoughnutChart from "~/components/charts/DoughnutChart.vue";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const store = usePosStore();
const loading = ref(false);

// Date range
const selectedPreset = ref("week");
const datePresets = [
  { label: "Today", value: "today" },
  { label: "Yesterday", value: "yesterday" },
  { label: "This Week", value: "week" },
  { label: "This Month", value: "month" },
  { label: "This Year", value: "year" },
];

const dateRange = ref({
  start: new Date(new Date().setDate(new Date().getDate() - 7))
    .toISOString()
    .split("T")[0],
  end: new Date().toISOString().split("T")[0],
});

// Chart settings
const selectedChartType = ref("line");
const chartTypes = [
  { label: "Line", value: "line" },
  { label: "Bar", value: "bar" },
];

// Table settings
const itemsPerPage = ref(10);
const currentPage = ref(1);
const tableSearch = ref("");
const sortKey = ref("date");
const sortOrder = ref("desc");
const topProductsLimit = ref(5);

// Schedule dialog
const showScheduleDialog = ref(false);
const schedule = ref({
  type: "sales",
  frequency: "weekly",
  email: "",
  format: "pdf",
});

// Toast
const showToast = ref(false);
const toastMessage = ref("");
const toastColor = ref("success");
const toastIcon = ref("mdi-check-circle");

// Get orders from store
const orders = computed(() => store.AllOrders || []);
const productsCategory = computed(() => store.products || []);

// Filter orders by date range
const filteredOrders = computed(() => {
  if (!orders.value.length) return [];

  return orders.value.filter((order) => {
    if (!order.created_at) return false;
    const orderDate = new Date(order.created_at).toISOString().split("T")[0];
    return (
      orderDate >= dateRange.value.start && orderDate <= dateRange.value.end
    );
  });
});

// Previous period orders for trend calculation
const previousPeriodOrders = computed(() => {
  if (!orders.value.length) return [];

  const startDate = new Date(dateRange.value.start);
  const endDate = new Date(dateRange.value.end);
  const duration = endDate.getTime() - startDate.getTime();

  const prevStartDate = new Date(startDate.getTime() - duration);
  const prevEndDate = new Date(endDate.getTime() - duration);

  const prevStart = prevStartDate.toISOString().split("T")[0];
  const prevEnd = prevEndDate.toISOString().split("T")[0];

  return orders.value.filter((order) => {
    if (!order.created_at) return false;
    const orderDate = new Date(order.created_at).toISOString().split("T")[0];
    return orderDate >= prevStart && orderDate <= prevEnd;
  });
});

// Total Revenue
const totalRevenue = computed(() => {
  return filteredOrders.value.reduce(
    (sum, order) => sum + (order.total || 0),
    0
  );
});

const previousRevenue = computed(() => {
  return previousPeriodOrders.value.reduce(
    (sum, order) => sum + (order.total || 0),
    0
  );
});

// Total Orders
const totalOrders = computed(() => filteredOrders.value.length);

const previousOrders = computed(() => previousPeriodOrders.value.length);

// Average Order Value
const averageOrderValue = computed(() => {
  if (totalOrders.value === 0) return 0;
  return totalRevenue.value / totalOrders.value;
});

const previousAvgOrder = computed(() => {
  if (previousOrders.value === 0) return 0;
  return previousRevenue.value / previousOrders.value;
});

// Total Items Sold
const totalItemsSold = computed(() => {
  return filteredOrders.value.reduce((sum, order) => {
    const items = order.items || [];
    return (
      sum + items.reduce((itemSum, item) => itemSum + (item.quantity || 0), 0)
    );
  }, 0);
});

const previousItemsSold = computed(() => {
  return previousPeriodOrders.value.reduce((sum, order) => {
    const items = order.items || [];
    return (
      sum + items.reduce((itemSum, item) => itemSum + (item.quantity || 0), 0)
    );
  }, 0);
});

// Trend calculations
const calculateTrend = (current: number, previous: number) => {
  if (previous === 0)
    return { class: "up", icon: "mdi-arrow-up", value: "+100%" };
  const percent = ((current - previous) / previous) * 100;
  const isUp = percent >= 0;
  return {
    class: isUp ? "up" : "down",
    icon: isUp ? "mdi-arrow-up" : "mdi-arrow-down",
    value: `${isUp ? "+" : ""}${percent.toFixed(1)}%`,
  };
};

const revenueTrend = computed(() =>
  calculateTrend(totalRevenue.value, previousRevenue.value)
);
const ordersTrend = computed(() =>
  calculateTrend(totalOrders.value, previousOrders.value)
);
const avgOrderTrend = computed(() =>
  calculateTrend(averageOrderValue.value, previousAvgOrder.value)
);
const itemsTrend = computed(() =>
  calculateTrend(totalItemsSold.value, previousItemsSold.value)
);

const revenueTrendClass = computed(() => revenueTrend.value.class);
const revenueTrendIcon = computed(() => revenueTrend.value.icon);
const revenueTrendValue = computed(() => revenueTrend.value.value);

const ordersTrendClass = computed(() => ordersTrend.value.class);
const ordersTrendIcon = computed(() => ordersTrend.value.icon);
const ordersTrendValue = computed(() => ordersTrend.value.value);

const avgOrderTrendClass = computed(() => avgOrderTrend.value.class);
const avgOrderTrendIcon = computed(() => avgOrderTrend.value.icon);
const avgOrderTrendValue = computed(() => avgOrderTrend.value.value);

const itemsTrendClass = computed(() => itemsTrend.value.class);
const itemsTrendIcon = computed(() => itemsTrend.value.icon);
const itemsTrendValue = computed(() => itemsTrend.value.value);

// Daily Revenue Data for Chart
const dailyRevenueData = computed(() => {
  const dailyMap = new Map();

  filteredOrders.value.forEach((order) => {
    const date = new Date(order.created_at).toISOString().split("T")[0];
    const revenue = order.total || 0;
    dailyMap.set(date, (dailyMap.get(date) || 0) + revenue);
  });

  // Sort by date
  const sortedDates = Array.from(dailyMap.keys()).sort();
  return sortedDates.map((date) => dailyMap.get(date));
});

const dailyRevenueLabels = computed(() => {
  const dailyMap = new Map();

  filteredOrders.value.forEach((order: any) => {
    const date = new Date(order.created_at).toISOString().split("T")[0];
    dailyMap.set(date, true);
  });

  return Array.from(dailyMap.keys())
    .sort()
    .map((date) => {
      return new Date(date).toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
      });
    });
});

// Top Selling Products
const topProductsData = computed(() => {
  const productMap = new Map();

  filteredOrders.value.forEach((order) => {
    const items = order.items || [];
    const categories = productsCategory.value.reduce((map, product) => {
      map[product.name] = product.category;
      return map;
    }, {});
    items.forEach((item) => {
      const key = item.name;
      if (!productMap.has(key)) {
        productMap.set(key, {
          name: item.name,
          category: item.name ? categories[item.name] || "Unknown" : "Unknown",
          quantity: 0,
          revenue: 0,
        });
      }
      const product = productMap.get(key);
      product.quantity += item.quantity || 0;
      product.revenue +=
        (item.unitPrice || item.price || 0) * (item.quantity || 0);
    });
  });

  const products = Array.from(productMap.values());
  const maxRevenue = Math.max(...products.map((p) => p.revenue), 1);

  return products
    .sort((a, b) => b.revenue - a.revenue)
    .map((p) => ({
      ...p,
      percentage: (p.revenue / maxRevenue) * 100,
    }));
});

// Category Statistics
const categoryStatsData = computed(() => {
  const categoryMap = new Map();
  const colors = {
    coffee: "#2D6A4F",
    tea: "#6B4E71",
    snack: "#E07A5F",
  };

  filteredOrders.value.forEach((order: any) => {
    const items = order.items || [];
    const categories = productsCategory.value.reduce(
      (map: any, product: any) => {
        map[product.name] = product.category;
        return map;
      },
      {}
    );
    items.forEach((item: any) => {
      const category = categories[item.name] || "Unknown";
      if (!categoryMap.has(category)) {
        categoryMap.set(category, 0);
      }
      const revenue =
        (item.unitPrice || item.price || 0) * (item.quantity || 0);
      categoryMap.set(category, categoryMap.get(category) + revenue);
    });
  });

  const total = Array.from(categoryMap.values()).reduce((a, b) => a + b, 0);

  return Array.from(categoryMap.entries())
    .map(([name, revenue]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      revenue,
      percentage: total > 0 ? Math.round((revenue / total) * 100) : 0,
      color: colors[name as keyof typeof colors] || "#9CA3AF",
    }))
    .sort((a, b) => b.revenue - a.revenue);
});

// Order Type Statistics
const orderTypeStatsData = computed(() => {
  const typeMap = new Map();
  const icons = {
    "dine-in": "🍽️",
    "take-away": "📦",
    "order-online": "📱",
  };
  const colors = {
    "dine-in": "#2D6A4F",
    "take-away": "#F4A261",
    "order-online": "#6B4E71",
  };

  filteredOrders.value.forEach((order) => {
    const type = order.orderType || "dine-in";
    if (!typeMap.has(type)) {
      typeMap.set(type, { count: 0, revenue: 0 });
    }
    const stats = typeMap.get(type);
    stats.count++;
    stats.revenue += order.total || 0;
  });

  const totalCount = filteredOrders.value.length;
  const totalRevenue = Array.from(typeMap.values()).reduce(
    (sum, t) => sum + t.revenue,
    0
  );

  return Array.from(typeMap.entries())
    .map(([name, stats]) => ({
      name: name
        .split("-")
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
        .join(" "),
      icon: icons[name as keyof typeof icons] || "📋",
      count: stats.count,
      revenue: stats.revenue,
      percentage:
        totalCount > 0 ? Math.round((stats.count / totalCount) * 100) : 0,
      color: colors[name as keyof typeof colors] || "#9CA3AF",
    }))
    .sort((a, b) => b.revenue - a.revenue);
});

// Hourly Sales Data
const hourlySalesData = computed(() => {
  const hourMap = new Map();

  // Initialize hours from 6 AM to 10 PM
  for (let i = 6; i <= 22; i++) {
    const hourLabel = i <= 11 ? `${i} AM` : i === 12 ? `12 PM` : `${i - 12} PM`;
    hourMap.set(i, { hour: hourLabel, revenue: 0 });
  }

  filteredOrders.value.forEach((order) => {
    if (order.created_at) {
      const hour = new Date(order.created_at).getHours();
      const revenue = order.total || 0;
      if (hourMap.has(hour)) {
        const data = hourMap.get(hour);
        data.revenue += revenue;
      }
    }
  });

  const hours = Array.from(hourMap.entries())
    .map(([key, value]) => ({
      hour: value.hour,
      revenue: value.revenue,
    }))
    .sort((a, b) => {
      const hourA = parseInt(a.hour);
      const hourB = parseInt(b.hour);
      return hourA - hourB;
    });

  const maxRevenue = Math.max(...hours.map((h) => h.revenue), 1);

  return hours.map((h) => ({
    ...h,
    percentage: (h.revenue / maxRevenue) * 100,
  }));
});

// Daily Sales Data for Table
const dailySalesData = computed(() => {
  const dailyMap = new Map();

  filteredOrders.value.forEach((order) => {
    const date = new Date(order.created_at).toISOString().split("T")[0];
    if (!dailyMap.has(date)) {
      dailyMap.set(date, { orders: 0, revenue: 0, itemsSold: 0 });
    }
    const data = dailyMap.get(date);
    data.orders++;
    data.revenue += order.total || 0;

    const items = order.items || [];
    items.forEach((item) => {
      data.itemsSold += item.quantity || 0;
    });
  });

  return Array.from(dailyMap.entries())
    .map(([date, data]) => ({
      date,
      orders: data.orders,
      revenue: data.revenue,
      avgOrder: data.orders > 0 ? data.revenue / data.orders : 0,
      itemsSold: data.itemsSold,
    }))
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
});

// Filtered and sorted sales data
const filteredSalesData = computed(() => {
  let data = [...dailySalesData.value];

  if (tableSearch.value) {
    data = data.filter(
      (day) =>
        day.date.includes(tableSearch.value) ||
        day.orders.toString().includes(tableSearch.value)
    );
  }

  data.sort((a, b) => {
    let aVal = a[sortKey.value as keyof typeof a];
    let bVal = b[sortKey.value as keyof typeof b];
    if (sortKey.value === "date") {
      aVal = new Date(aVal as string).getTime();
      bVal = new Date(bVal as string).getTime();
    }
    if (sortOrder.value === "asc") {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });

  return data;
});

const paginatedSalesData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredSalesData.value.slice(start, end);
});

const totalPages = computed(() =>
  Math.ceil(filteredSalesData.value.length / itemsPerPage.value)
);

// Helper functions
const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
};

const getRankClass = (rank: number) => {
  if (rank === 1) return "gold";
  if (rank === 2) return "silver";
  if (rank === 3) return "bronze";
  return "";
};

const getProgressColor = (index: number) => {
  const colors = ["#2D6A4F", "#E07A5F", "#F4A261", "#6B4E71", "#E9C46A"];
  return colors[index % colors.length];
};

const getHourColor = (percentage: number) => {
  if (percentage > 35) return "#2D6A4F";
  if (percentage > 20) return "#F4A261";
  return "#E07A5F";
};

const setDatePreset = (preset: string) => {
  selectedPreset.value = preset;
  const today = new Date();
  let start = new Date();

  switch (preset) {
    case "today":
      start = today;
      break;
    case "yesterday":
      start = new Date(today.setDate(today.getDate() - 1));
      break;
    case "week":
      start = new Date(today.setDate(today.getDate() - 7));
      break;
    case "month":
      start = new Date(today.setMonth(today.getMonth() - 1));
      break;
    case "year":
      start = new Date(today.setFullYear(today.getFullYear() - 1));
      break;
  }

  dateRange.value.start = start.toISOString().split("T")[0];
  dateRange.value.end = new Date().toISOString().split("T")[0];
  fetchReportData();
};

const sortBy = (key: string) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    sortKey.value = key;
    sortOrder.value = "desc";
  }
};

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const fetchReportData = async () => {
  loading.value = true;
  try {
    await store.getAllOrders();
    toast("Report data updated successfully!", "success");
  } catch (error) {
    toast("Failed to load report data", "error");
  } finally {
    loading.value = false;
  }
};
const fetchProductsData = async () => {
  loading.value = true;
  try {
    await store.getAllProducts();
    toast("Product data updated successfully!", "success");
  } catch (error) {
    toast("Failed to load product data", "error");
  } finally {
    loading.value = false;
  }
};

const exportReport = () => {
  toast("Report export started!", "success");
};

const exportPDF = () => {
  toast("PDF report generated!", "success");
};

const exportExcel = () => {
  toast("Excel file downloaded!", "success");
};

const exportCSV = () => {
  toast("CSV file downloaded!", "success");
};

const scheduleReport = () => {
  showScheduleDialog.value = false;
  toast("Report scheduled successfully!", "success");
};

const toast = (message: string, type: string = "success") => {
  toastMessage.value = message;
  toastColor.value = type === "success" ? "#2D6A4F" : "#E07A5F";
  toastIcon.value =
    type === "success" ? "mdi-check-circle" : "mdi-alert-circle";
  showToast.value = true;
};

onMounted(async () => {
  await fetchReportData();
  await fetchProductsData();
});
</script>

<style scoped>
.reports-container {
  padding: 32px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
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

.header-actions {
  display: flex;
  gap: 12px;
}

.export-btn,
.schedule-btn {
  text-transform: none;
  border-radius: 40px;
}

.export-btn {
  border-color: #e5e7eb;
}

.schedule-btn {
  background: #1b4332;
  color: white;
}

/* Date Range Section */
.date-range-section {
  margin-bottom: 32px;
}

.date-range-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.date-presets {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.preset-btn {
  padding: 8px 16px;
  border-radius: 40px;
  background: #f8f6f2;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 13px;
}

.preset-btn:hover {
  background: #e5e0d5;
}

.preset-btn.active {
  background: #2d6a4f;
  color: white;
}

.date-picker-group {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.date-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8f6f2;
  padding: 8px 16px;
  border-radius: 40px;
}

.date-icon {
  color: #9ca3af;
}

.date-input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
}

.date-separator {
  color: #9ca3af;
}

.apply-btn {
  background: #2d6a4f;
  color: white;
  border-radius: 40px;
  text-transform: none;
}

/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f4f6;
  border-top-color: #2d6a4f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.metric-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 20px;
}

.metric-trend.up {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.metric-trend.down {
  background: #e07a5f20;
  color: #e07a5f;
}

.metric-value {
  font-size: 32px;
  font-weight: 800;
  color: #1b4332;
  margin-bottom: 8px;
}

.metric-title {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}

.metric-subtitle {
  font-size: 11px;
  color: #9ca3af;
}

/* Charts */
.chart-row {
  margin-bottom: 32px;
}

.chart-card {
  border-radius: 24px;
  overflow: hidden;
  padding: 24px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.chart-title {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 4px;
}

.chart-subtitle {
  font-size: 12px;
  color: #6b7280;
}

.chart-controls {
  display: flex;
  gap: 8px;
}

.chart-type-btn {
  padding: 6px 16px;
  border-radius: 20px;
  background: #f8f6f2;
  border: none;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
}

.chart-type-btn.active {
  background: #2d6a4f;
  color: white;
}

.chart-container {
  height: 350px;
  position: relative;
}

/* Two Column Layout */
.two-column-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.products-card,
.distribution-card,
.hourly-card,
.ordertype-card {
  border-radius: 24px;
  padding: 24px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 4px;
}

.card-subtitle {
  font-size: 12px;
  color: #6b7280;
}

.limit-select {
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: white;
}

/* Products List */
.products-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.product-row {
  position: relative;
  padding: 12px;
  background: #f8f6f2;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.product-row:hover {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.product-rank {
  position: absolute;
  top: 12px;
  right: 12px;
}

.rank-badge {
  width: 28px;
  height: 28px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  background: #e5e7eb;
  color: #6b7280;
}

.rank-badge.gold {
  background: linear-gradient(135deg, #ffd700, #ffa500);
  color: white;
}

.rank-badge.silver {
  background: linear-gradient(135deg, #c0c0c0, #a8a8a8);
  color: white;
}

.rank-badge.bronze {
  background: linear-gradient(135deg, #cd7f32, #b87333);
  color: white;
}

.product-name {
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 4px;
}

.product-category {
  font-size: 11px;
  color: #6b7280;
}

.product-stats {
  display: flex;
  justify-content: space-between;
  margin: 12px 0 8px;
  font-size: 13px;
}

.product-quantity {
  color: #2d6a4f;
  font-weight: 600;
}

.product-revenue {
  color: #e07a5f;
  font-weight: 600;
}

.product-progress {
  height: 4px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 1s ease;
}

/* Distribution Chart */
.distribution-container {
  height: 200px;
  margin-bottom: 20px;
}

.category-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  background: #f8f6f2;
  border-radius: 12px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 4px;
}

.legend-name {
  flex: 1;
  font-weight: 500;
  color: #1b4332;
}

.legend-value {
  font-weight: 700;
  color: #1b4332;
}

.legend-amount {
  font-weight: 600;
  color: #e07a5f;
}

/* Hourly Bars */
.hourly-bars {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 250px;
  padding: 20px 0;
}

.hour-bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  height: 100%;
}

.hour-bar {
  width: 100%;
  min-height: 4px;
  border-radius: 4px;
  position: relative;
  transition: height 0.5s ease;
  cursor: pointer;
}

.hour-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  font-weight: 600;
  color: #1b4332;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.hour-bar:hover .hour-value {
  opacity: 1;
}

.hour-label {
  font-size: 10px;
  color: #6b7280;
}

/* Order Type Stats */
.ordertype-stats {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ordertype-item {
  padding: 12px;
  background: #f8f6f2;
  border-radius: 16px;
}

.ordertype-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.ordertype-name {
  font-weight: 600;
  color: #1b4332;
  display: flex;
  align-items: center;
  gap: 8px;
}

.ordertype-icon {
  font-size: 18px;
}

.ordertype-percentage {
  font-weight: 700;
  color: #2d6a4f;
}

.ordertype-progress {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 1s ease;
}

.ordertype-details {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #6b7280;
}

/* Sales Table */
.sales-table-card {
  border-radius: 24px;
  overflow: hidden;
  margin-bottom: 32px;
  padding: 24px;
}

.table-controls {
  display: flex;
  gap: 12px;
}

.search-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8f6f2;
  padding: 6px 12px;
  border-radius: 8px;
}

.table-search {
  border: none;
  background: transparent;
  outline: none;
  font-size: 13px;
}

.table-container {
  overflow-x: auto;
}

.sales-table {
  width: 100%;
  border-collapse: collapse;
}

.sales-table th {
  text-align: left;
  padding: 12px;
  background: #f8f6f2;
  font-weight: 600;
  color: #1b4332;
  cursor: pointer;
  transition: background 0.3s ease;
}

.sales-table th:hover {
  background: #e5e0d5;
}

.sales-table td {
  padding: 12px;
  border-bottom: 1px solid #f3f4f6;
  color: #4b5563;
}

.date-cell {
  font-weight: 600;
  color: #1b4332;
}

.revenue-cell {
  font-weight: 600;
  color: #e07a5f;
}

/* Pagination */
.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  padding-top: 16px;
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
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  background: white;
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

/* Export Options */
.export-options {
  background: white;
  border-radius: 24px;
  padding: 24px;
}

.export-header {
  margin-bottom: 24px;
}

.export-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 4px;
}

.export-header p {
  font-size: 13px;
  color: #6b7280;
}

.export-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.export-option {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f8f6f2;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.export-option:hover {
  transform: translateY(-2px);
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.export-icon {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.export-info {
  flex: 1;
}

.export-title {
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 4px;
}

.export-desc {
  font-size: 11px;
  color: #6b7280;
}

/* Dialog Styles */
.schedule-dialog {
  border-radius: 32px !important;
  overflow: hidden;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
}

.dialog-header h2 {
  font-family: "Playfair Display", serif;
  font-size: 24px;
  font-weight: 700;
  color: #1b4332;
}

.dialog-content {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-select,
.form-input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
  transition: all 0.3s ease;
}

.form-select:focus,
.form-input:focus {
  border-color: #2d6a4f;
  box-shadow: 0 0 0 2px rgba(45, 106, 79, 0.1);
}

.radio-group {
  display: flex;
  gap: 16px;
}

.radio-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  cursor: pointer;
}

.dialog-actions {
  padding: 16px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Toast */
.custom-toast :deep(.v-snackbar__content) {
  padding: 0 !important;
  background: transparent !important;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Responsive */
@media (max-width: 1200px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .two-column-row {
    grid-template-columns: 1fr;
  }

  .export-buttons {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .reports-container {
    padding: 20px;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .date-picker-group {
    flex-direction: column;
    align-items: stretch;
  }

  .page-title {
    font-size: 28px;
  }
}
</style>
