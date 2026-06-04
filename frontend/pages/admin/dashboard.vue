<!-- frontend/pages/admin/dashboard.vue -->
<template>
  <div class="dashboard-container">
    <!-- Welcome Header -->
    <div class="welcome-header">
      <div class="header-content">
        <div class="greeting-section">
          <div class="greeting-badge">Welcome Back</div>
          <h1 class="greeting-title">
            {{ authStore.userName }}
            <span class="wave">👋</span>
          </h1>
          <p class="greeting-subtitle">
            Here's what's happening with your coffee shop today
          </p>
        </div>
        <div class="date-section">
          <div class="date-card">
            <v-icon class="date-icon">mdi-calendar-today</v-icon>
            <div class="date-info">
              <div class="date-day">{{ currentDate }}</div>
              <div class="date-full">{{ currentFullDate }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card">
        <div
          class="stat-icon-wrapper"
          style="background: linear-gradient(135deg, #2d6a4f, #1b4332)"
        >
          <v-icon class="stat-icon" size="28">mdi-currency-usd</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">ksh{{ totalRevenue.toLocaleString() }}</div>
          <div class="stat-title">Total Revenue</div>
          <div class="stat-change" :class="revenueChangeClass">
            <v-icon size="14">{{ revenueChangeIcon }}</v-icon>
            <span>{{ revenueChangePercent }} from yesterday</span>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div
          class="stat-icon-wrapper"
          style="background: linear-gradient(135deg, #e07a5f, #d66b4a)"
        >
          <v-icon class="stat-icon" size="28">mdi-cart-outline</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ totalOrders }}</div>
          <div class="stat-title">Total Orders</div>
          <div class="stat-change" :class="ordersChangeClass">
            <v-icon size="14">{{ ordersChangeIcon }}</v-icon>
            <span>{{ ordersChangePercent }} from yesterday</span>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div
          class="stat-icon-wrapper"
          style="background: linear-gradient(135deg, #f4a261, #e9c46a)"
        >
          <v-icon class="stat-icon" size="28">mdi-chart-line</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">ksh{{ averageOrderValue.toFixed(2) }}</div>
          <div class="stat-title">Average Order</div>
          <div class="stat-change" :class="avgOrderChangeClass">
            <v-icon size="14">{{ avgOrderChangeIcon }}</v-icon>
            <span>{{ avgOrderChangePercent }} from yesterday</span>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div
          class="stat-icon-wrapper"
          style="background: linear-gradient(135deg, #6b4e71, #4a3b52)"
        >
          <v-icon class="stat-icon" size="28">mdi-coffee</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ totalItemsSold }}</div>
          <div class="stat-title">Items Sold</div>
          <div class="stat-change" :class="itemsChangeClass">
            <v-icon size="14">{{ itemsChangeIcon }}</v-icon>
            <span>{{ itemsChangePercent }} from yesterday</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-row">
      <v-card class="chart-card" elevation="0">
        <div class="chart-header">
          <div>
            <div class="chart-title">Revenue Overview</div>
            <div class="chart-subtitle">Last 7 days performance</div>
          </div>
          <v-select
            v-model="revenuePeriod"
            :items="['7 days', '30 days', '90 days']"
            variant="outlined"
            density="compact"
            class="period-select"
            @update:model-value="updateRevenueChart"
          />
        </div>
        <div class="chart-container">
          <!-- <revenue-chart :data="getRevenueChartData()" /> -->
          <canvas ref="revenueChartCanvas"></canvas>
        </div>
      </v-card>

      <v-card class="chart-card" elevation="0">
        <div class="chart-header">
          <div>
            <div class="chart-title">Popular Items</div>
            <div class="chart-subtitle">Best selling products</div>
          </div>
          <v-icon class="chart-menu-icon">mdi-dots-horizontal</v-icon>
        </div>
        <div class="popular-items">
          <div
            v-for="item in topProducts"
            :key="item.name"
            class="popular-item"
          >
            <div class="item-rank">{{ item.rank }}</div>
            <div class="item-info">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-category">{{ item.category }}</div>
            </div>
            <div class="item-stats">
              <div class="item-sales">{{ item.quantity }} sold</div>
              <div class="item-revenue">
                ksh{{ item.revenue.toLocaleString() }}
              </div>
            </div>
            <div class="item-progress">
              <div
                class="progress-bar"
                :style="{ width: `${item.percentage}%` }"
              ></div>
            </div>
          </div>
        </div>
      </v-card>
    </div>

    <!-- Recent Orders & Activity -->
    <div class="activity-row">
      <v-card class="recent-orders-card" elevation="0">
        <div class="card-header">
          <div>
            <div class="card-title">Recent Orders</div>
            <div class="card-subtitle">Latest transactions</div>
          </div>
          <v-btn variant="text" class="view-all-btn" to="/orders">
            View All
            <v-icon end size="18">mdi-arrow-right</v-icon>
          </v-btn>
        </div>
        <div class="orders-list">
          <div
            v-for="order in recentOrdersData"
            :key="order.id"
            class="order-row"
          >
            <div class="order-info">
              <div class="order-receipt">#{{ order.receiptNumber }}</div>
              <div class="order-meta">
                <span class="order-time">{{ order.time }}</span>
                <span class="order-type-badge" :class="order.orderType">
                  {{ order.orderType }}
                </span>
              </div>
            </div>
            <div class="order-customer">{{ order.customerName }}</div>
            <div class="order-amount">
              ksh{{ order.total.toLocaleString() }}
            </div>
            <v-chip
              :color="order.status === 'completed' ? '#2D6A4F' : '#E07A5F'"
              size="small"
              class="order-status"
            >
              {{ order.status }}
            </v-chip>
          </div>
        </div>
      </v-card>

      <v-card class="activity-card" elevation="0">
        <div class="card-header">
          <div>
            <div class="card-title">Recent Activity</div>
            <div class="card-subtitle">System updates</div>
          </div>
        </div>
        <div class="activity-timeline">
          <div
            v-for="activity in recentActivities"
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-icon" :style="{ background: activity.color }">
              <v-icon size="16">{{ activity.icon }}</v-icon>
            </div>
            <div class="activity-content">
              <div class="activity-text">{{ activity.text }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </v-card>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <div class="quick-actions-header">
        <h3>Quick Actions</h3>
        <p>Frequently used operations</p>
      </div>
      <div class="actions-grid">
        <div class="action-card" @click="openAddProduct">
          <div
            class="action-icon"
            style="background: linear-gradient(135deg, #2d6a4f, #1b4332)"
          >
            <v-icon size="24" color="white">mdi-plus</v-icon>
          </div>
          <div class="action-text">Add Product</div>
        </div>
        <div class="action-card" @click="viewOrders">
          <div
            class="action-icon"
            style="background: linear-gradient(135deg, #e07a5f, #d66b4a)"
          >
            <v-icon size="24" color="white">mdi-receipt</v-icon>
          </div>
          <div class="action-text">View Orders</div>
        </div>
        <div class="action-card" @click="generateReport">
          <div
            class="action-icon"
            style="background: linear-gradient(135deg, #f4a261, #e9c46a)"
          >
            <v-icon size="24" color="white">mdi-chart-bar</v-icon>
          </div>
          <div class="action-text">Generate Report</div>
        </div>
        <div class="action-card" @click="manageUsers">
          <div
            class="action-icon"
            style="background: linear-gradient(135deg, #6b4e71, #4a3b52)"
          >
            <v-icon size="24" color="white">mdi-account-group</v-icon>
          </div>
          <div class="action-text">Manage Users</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "~/stores/auth";
import { usePosStore } from "~/stores/pos";
import Chart from "chart.js/auto";
import RevenueChart from "~/components/charts/RevenueChart.vue";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const authStore = useAuthStore();
const store = usePosStore();
const revenuePeriod = ref("7 days");
let revenueChartInstance: Chart | null = null;
const revenueChartCanvas = ref<HTMLCanvasElement | null>(null);

// Get all orders from store
const allOrders = computed(() => store.AllOrders || []);

// Today's date
const today = new Date().toISOString().split("T")[0];
const yesterday = new Date(Date.now() - 86400000).toISOString().split("T")[0];

// Filter orders for today
const todayOrders = computed(() => {
  return allOrders.value.filter((order) => {
    const orderDate = new Date(order.created_at).toISOString().split("T")[0];
    return orderDate === today;
  });
});

// Filter orders for yesterday
const yesterdayOrders = computed(() => {
  return allOrders.value.filter((order) => {
    const orderDate = new Date(order.created_at).toISOString().split("T")[0];
    return orderDate === yesterday;
  });
});

// Total Revenue
const totalRevenue = computed(() => {
  return allOrders.value.reduce((sum, order) => sum + (order.total || 0), 0);
});

const todayRevenue = computed(() => {
  return todayOrders.value.reduce((sum, order) => sum + (order.total || 0), 0);
});

const yesterdayRevenue = computed(() => {
  return yesterdayOrders.value.reduce(
    (sum, order) => sum + (order.total || 0),
    0
  );
});

// Total Orders
const totalOrders = computed(() => allOrders.value.length);

const todayOrderCount = computed(() => todayOrders.value.length);
const yesterdayOrderCount = computed(() => yesterdayOrders.value.length);

// Average Order Value
const averageOrderValue = computed(() => {
  if (totalOrders.value === 0) return 0;
  return totalRevenue.value / totalOrders.value;
});

const todayAvgOrder = computed(() => {
  if (todayOrderCount.value === 0) return 0;
  return todayRevenue.value / todayOrderCount.value;
});

const yesterdayAvgOrder = computed(() => {
  if (yesterdayOrderCount.value === 0) return 0;
  return yesterdayRevenue.value / yesterdayOrderCount.value;
});

// Total Items Sold
const totalItemsSold = computed(() => {
  return allOrders.value.reduce((sum, order) => {
    const items = order.items || [];
    return (
      sum + items.reduce((itemSum, item) => itemSum + (item.quantity || 0), 0)
    );
  }, 0);
});

const todayItemsSold = computed(() => {
  return todayOrders.value.reduce((sum, order) => {
    const items = order.items || [];
    return (
      sum + items.reduce((itemSum, item) => itemSum + (item.quantity || 0), 0)
    );
  }, 0);
});

const yesterdayItemsSold = computed(() => {
  return yesterdayOrders.value.reduce((sum, order) => {
    const items = order.items || [];
    return (
      sum + items.reduce((itemSum, item) => itemSum + (item.quantity || 0), 0)
    );
  }, 0);
});

// Calculate percentage changes
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
  calculateChange(todayOrderCount.value, yesterdayOrderCount.value)
);
const avgOrderChange = computed(() =>
  calculateChange(todayAvgOrder.value, yesterdayAvgOrder.value)
);
const itemsChange = computed(() =>
  calculateChange(todayItemsSold.value, yesterdayItemsSold.value)
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

const itemsChangeClass = computed(() =>
  itemsChange.value.isPositive ? "positive" : "negative"
);
const itemsChangeIcon = computed(() =>
  itemsChange.value.isPositive ? "mdi-arrow-up" : "mdi-arrow-down"
);
const itemsChangePercent = computed(() => itemsChange.value.percent);

// Top Products
const topProducts = computed(() => {
  const productMap = new Map();

  allOrders.value.forEach((order) => {
    const items = order.items || [];
    items.forEach((item) => {
      const key = item.name;
      if (!productMap.has(key)) {
        productMap.set(key, {
          name: item.name,
          category: item.category || "Unknown",
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
    .slice(0, 5)
    .map((p, index) => ({
      ...p,
      rank: index + 1,
      percentage: (p.revenue / maxRevenue) * 100,
    }));
});

// Recent Orders
const recentOrdersData = computed(() => {
  return allOrders.value
    .slice()
    .sort(
      (a, b) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
    .slice(0, 5)
    .map((order: any) => ({
      id: order._id,
      receiptNumber: order.receiptNumber,
      time: new Date(order.created_at).toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
      }),
      orderType: order.orderType,
      customerName: order.customerName,
      total: order.total,
      status: "completed",
    }));
});

// Revenue Chart Data
const getRevenueChartData = () => {
  let days = 7;
  if (revenuePeriod.value === "30 days") days = 30;
  if (revenuePeriod.value === "90 days") days = 90;

  const revenueMap = new Map();
  const today = new Date();

  // Initialize last 'days' days with zero
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    const dateStr = date.toISOString().split("T")[0];
    revenueMap.set(dateStr, 0);
  }

  // Aggregate revenue by date
  allOrders.value.forEach((order) => {
    const orderDate = new Date(order.created_at).toISOString().split("T")[0];
    if (revenueMap.has(orderDate)) {
      revenueMap.set(orderDate, revenueMap.get(orderDate) + (order.total || 0));
    }
  });

  const labels = Array.from(revenueMap.keys()).map((date) => {
    return new Date(date).toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
    });
  });

  const data = Array.from(revenueMap.values());

  return { labels, data };
};

const updateRevenueChart = () => {
  if (revenueChartInstance) {
    revenueChartInstance.destroy();
  }

  const ctx = revenueChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  const { labels, data } = getRevenueChartData();

  revenueChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Revenue",
          data: data,
          borderColor: "#2D6A4F",
          backgroundColor: "rgba(45, 106, 79, 0.1)",
          tension: 0.4,
          fill: true,
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
            label: (context) => {
              return `Revenue: ksh${context.raw.toLocaleString()}`;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => "ksh" + value.toLocaleString(),
          },
        },
      },
    },
  });
};

// Recent Activities (based on actual orders)
const recentActivities = computed(() => {
  const activities = [];

  // Add order activities
  allOrders.value.slice(0, 5).forEach((order, index) => {
    const time = new Date(order.created_at);
    const now = new Date();
    const diffMs = now.getTime() - time.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);

    let timeAgo = "";
    if (diffMins < 1) timeAgo = "Just now";
    else if (diffMins < 60) timeAgo = `${diffMins} min ago`;
    else if (diffHours < 24)
      timeAgo = `${diffHours} hour${diffHours > 1 ? "s" : ""} ago`;
    else timeAgo = time.toLocaleDateString();

    activities.push({
      id: `order-${order._id}`,
      text: `New order #${order.receiptNumber} placed by ${order.customerName}`,
      time: timeAgo,
      icon: "mdi-cart-plus",
      color: "#2D6A4F",
    });
  });

  return activities.slice(0, 4);
});

// Date formatting
const currentDate = new Date().toLocaleDateString("en-US", {
  weekday: "long",
  day: "numeric",
});
const currentFullDate = new Date().toLocaleDateString("en-US", {
  month: "long",
  year: "numeric",
});

// Chart initialization
const initRevenueChart = () => {
  updateRevenueChart();
};

// Watch for revenue period changes
watch(revenuePeriod, () => {
  updateRevenueChart();
});

// Actions
const openAddProduct = () => {
  navigateTo("/admin/products");
};

const viewOrders = () => {
  navigateTo("/orders");
};

const generateReport = () => {
  navigateTo("/reports");
};

const manageUsers = () => {
  navigateTo("/admin/users");
};

// Load data on mount
onMounted(async () => {
  await store.getAllOrders();
  await store.getAllProducts();
  initRevenueChart();
});
</script>

<style scoped>
/* All existing styles remain the same */
.dashboard-container {
  padding: 32px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Welcome Header */
.welcome-header {
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 20px;
}

.greeting-badge {
  font-size: 12px;
  font-weight: 600;
  color: #e07a5f;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 12px;
}

.greeting-title {
  font-family: "Playfair Display", serif;
  font-size: 36px;
  font-weight: 800;
  color: #1b4332;
  margin-bottom: 8px;
}

.wave {
  display: inline-block;
  animation: wave 1s ease-in-out infinite;
}

@keyframes wave {
  0%,
  100% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(20deg);
  }
}

.greeting-subtitle {
  color: #6b7280;
  font-size: 14px;
}

.date-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 24px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.date-icon {
  color: #2d6a4f;
  font-size: 28px;
}

.date-info {
  text-align: right;
}

.date-day {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.date-full {
  font-size: 12px;
  color: #6b7280;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.stat-icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon {
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 800;
  color: #1b4332;
  margin-bottom: 4px;
}

.stat-title {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 8px;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.stat-change.positive {
  color: #2d6a4f;
}

.stat-change.negative {
  color: #e07a5f;
}

/* Charts Row */
.charts-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
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

.period-select {
  width: 120px;
}

.chart-container {
  height: 300px;
  position: relative;
}

/* Popular Items */
.popular-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.popular-item {
  position: relative;
  padding: 12px;
  background: #f8f6f2;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.popular-item:hover {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.item-rank {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 24px;
  font-weight: 800;
  color: rgba(0, 0, 0, 0.05);
}

.item-info {
  margin-bottom: 8px;
}

.item-name {
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 4px;
}

.item-category {
  font-size: 11px;
  color: #6b7280;
}

.item-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
}

.item-sales {
  color: #2d6a4f;
  font-weight: 600;
}

.item-revenue {
  color: #e07a5f;
  font-weight: 600;
}

.item-progress {
  height: 4px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #2d6a4f, #1b4332);
  border-radius: 4px;
  transition: width 1s ease;
}

/* Activity Row */
.activity-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.recent-orders-card,
.activity-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
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

.view-all-btn {
  text-transform: none;
  color: #e07a5f;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8f6f2;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.order-row:hover {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.order-receipt {
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 4px;
}

.order-meta {
  display: flex;
  gap: 8px;
  align-items: center;
}

.order-time {
  font-size: 11px;
  color: #6b7280;
}

.order-type-badge {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 20px;
  font-weight: 600;
}

.order-type-badge.dine-in {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.order-type-badge.take-away {
  background: #f4a26120;
  color: #f4a261;
}

.order-type-badge.online {
  background: #6b4e7120;
  color: #6b4e71;
}

.order-customer {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.order-amount {
  font-weight: 700;
  color: #e07a5f;
}

.order-status {
  text-transform: uppercase;
  font-size: 10px;
  font-weight: 600;
}

/* Activity Timeline */
.activity-timeline {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: #f8f6f2;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 14px;
  font-weight: 500;
  color: #1b4332;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 11px;
  color: #6b7280;
}

/* Quick Actions */
.quick-actions {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.quick-actions-header {
  margin-bottom: 24px;
}

.quick-actions-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 4px;
}

.quick-actions-header p {
  font-size: 12px;
  color: #6b7280;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px;
  background: #f8f6f2;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-card:hover {
  transform: translateY(-4px);
  background: white;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-text {
  font-weight: 600;
  color: #1b4332;
}

/* Responsive */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row,
  .activity-row {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 20px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .greeting-title {
    font-size: 28px;
  }
}
</style>
