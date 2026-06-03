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
      <div class="stat-card" v-for="stat in stats" :key="stat.title">
        <div class="stat-icon-wrapper" :style="{ background: stat.gradient }">
          <v-icon class="stat-icon" size="28">{{ stat.icon }}</v-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-title">{{ stat.title }}</div>
          <div class="stat-change" :class="stat.changeType">
            <v-icon size="14">{{ stat.changeIcon }}</v-icon>
            <span>{{ stat.change }} from yesterday</span>
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
          />
        </div>
        <div class="chart-container">
          <canvas ref="revenueChart"></canvas>
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
            v-for="item in popularItems"
            :key="item.name"
            class="popular-item"
          >
            <div class="item-rank">{{ item.rank }}</div>
            <div class="item-info">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-category">{{ item.category }}</div>
            </div>
            <div class="item-stats">
              <div class="item-sales">{{ item.sales }} sold</div>
              <div class="item-revenue">${{ item.revenue }}</div>
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
          <div v-for="order in recentOrders" :key="order.id" class="order-row">
            <div class="order-info">
              <div class="order-receipt">{{ order.receiptNumber }}</div>
              <div class="order-meta">
                <span class="order-time">{{ order.time }}</span>
                <span class="order-type-badge" :class="order.orderType">
                  {{ order.orderType }}
                </span>
              </div>
            </div>
            <div class="order-customer">{{ order.customerName }}</div>
            <div class="order-amount">${{ order.total }}</div>
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
            v-for="activity in activities"
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
import { ref, onMounted } from "vue";
import { useAuthStore } from "~/stores/auth";
// import Chart from "chart.js/auto";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const authStore = useAuthStore();
const revenuePeriod = ref("7 days");
const revenueChart = ref(null);

// Stats data
const stats = ref([
  {
    title: "Total Revenue",
    value: "$12,426",
    icon: "mdi-currency-usd",
    gradient: "linear-gradient(135deg, #2D6A4F, #1B4332)",
    change: "+12.5%",
    changeType: "positive",
    changeIcon: "mdi-arrow-up",
  },
  {
    title: "Total Orders",
    value: "1,234",
    icon: "mdi-cart-outline",
    gradient: "linear-gradient(135deg, #E07A5F, #D66B4A)",
    change: "+8.2%",
    changeType: "positive",
    changeIcon: "mdi-arrow-up",
  },
  {
    title: "Average Order",
    value: "$45.20",
    icon: "mdi-chart-line",
    gradient: "linear-gradient(135deg, #F4A261, #E9C46A)",
    change: "-2.4%",
    changeType: "negative",
    changeIcon: "mdi-arrow-down",
  },
  {
    title: "Active Users",
    value: "24",
    icon: "mdi-account-group",
    gradient: "linear-gradient(135deg, #6B4E71, #4A3B52)",
    change: "+5%",
    changeType: "positive",
    changeIcon: "mdi-arrow-up",
  },
]);

// Popular items
const popularItems = ref([
  {
    rank: 1,
    name: "Caramel Macchiato",
    category: "Coffee",
    sales: 234,
    revenue: 936,
    percentage: 100,
  },
  {
    rank: 2,
    name: "Croissant",
    category: "Snack",
    sales: 198,
    revenue: 693,
    percentage: 85,
  },
  {
    rank: 3,
    name: "Matcha Latte",
    category: "Tea",
    sales: 167,
    revenue: 751,
    percentage: 71,
  },
  {
    rank: 4,
    name: "Blueberry Muffin",
    category: "Snack",
    sales: 145,
    revenue: 435,
    percentage: 62,
  },
  {
    rank: 5,
    name: "Iced Americano",
    category: "Coffee",
    sales: 128,
    revenue: 512,
    percentage: 55,
  },
]);

// Recent orders
const recentOrders = ref([
  {
    id: 1,
    receiptNumber: "#RCP-12345",
    time: "2 min ago",
    customerName: "John Smith",
    orderType: "dine-in",
    total: 42.5,
    status: "completed",
  },
  {
    id: 2,
    receiptNumber: "#RCP-12346",
    time: "15 min ago",
    customerName: "Emma Wilson",
    orderType: "take-away",
    total: 28.75,
    status: "completed",
  },
  {
    id: 3,
    receiptNumber: "#RCP-12347",
    time: "32 min ago",
    customerName: "Michael Brown",
    orderType: "online",
    total: 53.2,
    status: "preparing",
  },
  {
    id: 4,
    receiptNumber: "#RCP-12348",
    time: "1 hour ago",
    customerName: "Sarah Johnson",
    orderType: "dine-in",
    total: 34.9,
    status: "completed",
  },
]);

// Activities
const activities = ref([
  {
    id: 1,
    text: "New order #RCP-12345 placed",
    time: "2 min ago",
    icon: "mdi-cart-plus",
    color: "#2D6A4F",
  },
  {
    id: 2,
    text: 'Product "Caramel Macchiato" added',
    time: "15 min ago",
    icon: "mdi-coffee",
    color: "#E07A5F",
  },
  {
    id: 3,
    text: "Cashier Sarah logged in",
    time: "32 min ago",
    icon: "mdi-account-check",
    color: "#F4A261",
  },
  {
    id: 4,
    text: "Daily sales report generated",
    time: "1 hour ago",
    icon: "mdi-chart-line",
    color: "#6B4E71",
  },
]);

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
onMounted(() => {
  const ctx = document.getElementById("revenueChart")?.getContext("2d");
  if (ctx) {
    new Chart(ctx, {
      type: "line",
      data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
          {
            label: "Revenue",
            data: [1250, 1420, 1380, 1650, 1890, 2100, 1950],
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
        },
      },
    });
  }
});

// Actions
const openAddProduct = () => {
  // Open add product dialog or navigate
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
</script>

<style scoped>
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
