<!-- frontend/pages/admin/dashboard.vue -->
<template>
  <div class="dashboard-container">
    <!-- Welcome Header -->
    <v-row class="welcome-header" no-gutters>
      <v-col cols="12">
        <v-card class="welcome-card" elevation="0" rounded="xl">
          <v-card-text class="pa-6">
            <v-row align="center" no-gutters>
              <v-col cols="12" md="7">
                <div class="greeting-section">
                  <v-chip
                    class="greeting-badge mb-2"
                    color="#E07A5F"
                    size="small"
                    variant="flat"
                    label
                  >
                    {{ getTimeGreeting() }}
                  </v-chip>
                  <h1 class="greeting-title">
                    {{ authStore.userName }}
                    <span class="wave">👋</span>
                  </h1>
                  <p class="greeting-subtitle text-medium-emphasis">
                    Here's what's happening with your business today
                  </p>
                </div>
              </v-col>
              <v-col cols="12" md="5" class="text-md-right mt-4 mt-md-0">
                <v-row align="center" justify="end" no-gutters>
                  <v-col cols="auto">
                    <v-card class="date-card" elevation="0" rounded="lg">
                      <v-card-text class="pa-3">
                        <v-row align="center" no-gutters>
                          <v-col cols="auto">
                            <v-icon class="date-icon" color="#2D6A4F" size="32">
                              mdi-calendar-today
                            </v-icon>
                          </v-col>
                          <v-col class="pl-3">
                            <div class="date-day font-weight-bold">
                              {{ currentDate }}
                            </div>
                            <div
                              class="date-full text-caption text-medium-emphasis"
                            >
                              {{ currentFullDate }}
                            </div>
                          </v-col>
                        </v-row>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="auto" class="ml-2">
                    <v-btn
                      icon
                      color="#E07A5F"
                      variant="tonal"
                      size="small"
                      @click="showNotifications = !showNotifications"
                    >
                      <v-badge
                        :content="unreadNotifications"
                        color="#E07A5F"
                        offset-x="8"
                        offset-y="8"
                      >
                        <v-icon>mdi-bell</v-icon>
                      </v-badge>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Business Health Indicators -->
    <v-row class="health-indicators mt-2" no-gutters>
      <v-col cols="12">
        <v-card class="health-card" elevation="0" rounded="xl">
          <v-card-text class="pa-3">
            <v-row align="center" no-gutters>
              <v-col
                v-for="indicator in healthIndicators"
                :key="indicator.label"
                cols="6"
                sm="3"
                class="pa-1"
              >
                <div class="health-item">
                  <div
                    class="health-icon"
                    :style="{ background: indicator.color + '20' }"
                  >
                    <v-icon :color="indicator.color" size="20">{{
                      indicator.icon
                    }}</v-icon>
                  </div>
                  <div class="health-info">
                    <div
                      class="health-value"
                      :style="{ color: indicator.color }"
                    >
                      {{ indicator.value }}
                    </div>
                    <div class="health-label">{{ indicator.label }}</div>
                  </div>
                  <div class="health-status" :class="indicator.status">
                    <v-icon size="12">{{
                      indicator.status === "good"
                        ? "mdi-check-circle"
                        : "mdi-alert-circle"
                    }}</v-icon>
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Stats Grid - Enhanced -->
    <v-row class="stats-grid mt-2" no-gutters>
      <v-col cols="12" sm="6" lg="3" class="pa-2">
        <v-card
          class="stat-card"
          elevation="0"
          rounded="xl"
          hover
          to="/reports/sales"
        >
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon-wrapper"
                  style="background: linear-gradient(135deg, #2d6a4f, #1b4332)"
                >
                  <v-icon class="stat-icon" color="white" size="28"
                    >mdi-currency-usd</v-icon
                  >
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value font-weight-bold">
                  KSh {{ totalRevenue.toLocaleString() }}
                </div>
                <div class="stat-title text-caption text-medium-emphasis">
                  Total Revenue
                </div>
                <div class="stat-change" :class="revenueChangeClass">
                  <v-icon size="14">{{ revenueChangeIcon }}</v-icon>
                  <span class="text-caption">{{ revenueChangePercent }}</span>
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
          hover
          to="/reports/sales"
        >
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon-wrapper"
                  style="background: linear-gradient(135deg, #e07a5f, #d66b4a)"
                >
                  <v-icon class="stat-icon" color="white" size="28"
                    >mdi-cart-outline</v-icon
                  >
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value font-weight-bold">{{ totalOrders }}</div>
                <div class="stat-title text-caption text-medium-emphasis">
                  Total Orders
                </div>
                <div class="stat-change" :class="ordersChangeClass">
                  <v-icon size="14">{{ ordersChangeIcon }}</v-icon>
                  <span class="text-caption">{{ ordersChangePercent }}</span>
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
          hover
          to="/reports/profit"
        >
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon-wrapper"
                  style="background: linear-gradient(135deg, #f4a261, #e9c46a)"
                >
                  <v-icon class="stat-icon" color="white" size="28"
                    >mdi-chart-line</v-icon
                  >
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value font-weight-bold">
                  KSh {{ averageOrderValue.toFixed(2) }}
                </div>
                <div class="stat-title text-caption text-medium-emphasis">
                  Average Order
                </div>
                <div class="stat-change" :class="avgOrderChangeClass">
                  <v-icon size="14">{{ avgOrderChangeIcon }}</v-icon>
                  <span class="text-caption">{{ avgOrderChangePercent }}</span>
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
          hover
          to="/reports/inventory"
        >
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div
                  class="stat-icon-wrapper"
                  style="background: linear-gradient(135deg, #6b4e71, #4a3b52)"
                >
                  <v-icon class="stat-icon" color="white" size="28"
                    >mdi-package-variant</v-icon
                  >
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value font-weight-bold">
                  {{ totalProducts }}
                </div>
                <div class="stat-title text-caption text-medium-emphasis">
                  Products in Stock
                </div>
                <div class="stat-change" :class="inventoryChangeClass">
                  <v-icon size="14">{{ inventoryChangeIcon }}</v-icon>
                  <span class="text-caption">{{ inventoryChangePercent }}</span>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Extended Stats Row -->
    <v-row class="extended-stats" no-gutters>
      <v-col cols="12" sm="6" lg="2" class="pa-2">
        <v-card class="stat-card mini" elevation="0" rounded="xl">
          <v-card-text class="pa-3 text-center">
            <div class="mini-stat-value">{{ todayOrders.length }}</div>
            <div class="mini-stat-label">Today's Orders</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="2" class="pa-2">
        <v-card class="stat-card mini" elevation="0" rounded="xl">
          <v-card-text class="pa-3 text-center">
            <div class="mini-stat-value">KSh {{ todayRevenue.toFixed(0) }}</div>
            <div class="mini-stat-label">Today's Revenue</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="2" class="pa-2">
        <v-card
          class="stat-card mini"
          elevation="0"
          rounded="xl"
          @click="navigateTo('/admin/inventory/low-stock')"
          style="cursor: pointer"
        >
          <v-card-text class="pa-3 text-center">
            <div class="mini-stat-value" style="color: #f4a261">
              {{ lowStockCount }}
            </div>
            <div class="mini-stat-label">Low Stock Items</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="2" class="pa-2">
        <v-card
          class="stat-card mini"
          elevation="0"
          rounded="xl"
          @click="navigateTo('/admin/inventory/out-of-stock')"
          style="cursor: pointer"
        >
          <v-card-text class="pa-3 text-center">
            <div class="mini-stat-value" style="color: #e07a5f">
              {{ outOfStockCount }}
            </div>
            <div class="mini-stat-label">Out of Stock</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="2" class="pa-2">
        <v-card
          class="stat-card mini"
          elevation="0"
          rounded="xl"
          @click="navigateTo('/orders?filter=debt')"
          style="cursor: pointer"
        >
          <v-card-text class="pa-3 text-center">
            <div class="mini-stat-value" style="color: #e07a5f">
              {{ debtCount }}
            </div>
            <div class="mini-stat-label">Debt Orders</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="2" class="pa-2">
        <v-card class="stat-card mini" elevation="0" rounded="xl">
          <v-card-text class="pa-3 text-center">
            <div class="mini-stat-value">{{ totalItemsSold }}</div>
            <div class="mini-stat-label">Items Sold</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Daily Financial Summary -->
    <v-row class="mt-2" no-gutters>
      <v-col cols="12" class="pa-2">
        <DailyFinancialSummary :date="today" />
      </v-col>
    </v-row>

    <!-- Charts Row - Enhanced -->
    <v-row class="mt-2" no-gutters>
      <v-col cols="12" lg="8" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Revenue Overview</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  {{ revenuePeriodLabel }}
                </div>
              </div>
              <v-select
                v-model="revenuePeriod"
                :items="['7 days', '30 days', '90 days']"
                variant="outlined"
                density="compact"
                class="period-select"
                style="max-width: 120px"
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
                <div class="chart-title font-weight-bold">Payment Methods</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Today's payment distribution
                </div>
              </div>
            </div>
            <div class="chart-container payment-chart">
              <canvas ref="paymentChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Orders & Activity -->
    <v-row class="mt-2" no-gutters>
      <v-col cols="12" lg="7" class="pa-2">
        <v-card class="recent-orders-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="card-header">
              <div>
                <div class="card-title font-weight-bold">Recent Orders</div>
                <div class="card-subtitle text-caption text-medium-emphasis">
                  Latest transactions
                </div>
              </div>
              <v-btn
                variant="text"
                class="view-all-btn"
                color="#E07A5F"
                to="/orders"
              >
                View All
                <v-icon end size="18">mdi-arrow-right</v-icon>
              </v-btn>
            </div>
            <div class="orders-list">
              <!-- {{ recentOrdersData }} -->
              <div
                v-for="order in recentOrdersData"
                :key="order.id"
                class="order-row"
              >
                <v-row align="center" no-gutters>
                  <v-col cols="12" sm="4" class="order-info">
                    <div class="order-receipt font-weight-bold">
                      #{{ order.receiptNumber }}
                    </div>
                    <div class="order-meta">
                      <span
                        class="order-time text-caption text-medium-emphasis"
                        >{{ order.time }}</span
                      >
                      <v-chip
                        size="x-small"
                        :color="getOrderTypeColor(order.orderType)"
                        class="order-type-badge"
                      >
                        {{ formatOrderType(order.orderType) }}
                      </v-chip>
                    </div>
                  </v-col>
                  <v-col cols="6" sm="4" class="order-customer">
                    {{ order.customerName || "Walk-in Customer" }}
                  </v-col>
                  <v-col
                    cols="6"
                    sm="2"
                    class="order-amount text-right font-weight-bold"
                  >
                    KSh {{ order.total.toLocaleString() }}
                  </v-col>
                  <v-col
                    cols="12"
                    sm="2"
                    class="text-left text-sm-right mt-2 mt-sm-0"
                  >
                    <v-chip
                      :color="getStatusColor(order.status)"
                      size="small"
                      class="order-status"
                      text-color="white"
                    >
                      {{ formatStatus(order.status) }}
                    </v-chip>
                  </v-col>
                </v-row>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="5" class="pa-2">
        <v-card class="activity-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="card-header">
              <div>
                <div class="card-title font-weight-bold">Recent Activity</div>
                <div class="card-subtitle text-caption text-medium-emphasis">
                  System updates
                </div>
              </div>
            </div>
            <div class="activity-timeline">
              <div
                v-for="activity in recentActivities"
                :key="activity.id"
                class="activity-item"
              >
                <v-row align="center" no-gutters>
                  <v-col cols="auto">
                    <div
                      class="activity-icon"
                      :style="{ background: activity.color }"
                    >
                      <v-icon size="16" color="white">{{
                        activity.icon
                      }}</v-icon>
                    </div>
                  </v-col>
                  <v-col class="px-3">
                    <div class="activity-text font-weight-medium">
                      {{ activity.text }}
                    </div>
                    <div
                      class="activity-time text-caption text-medium-emphasis"
                    >
                      {{ activity.time }}
                    </div>
                  </v-col>
                </v-row>
              </div>
              <div
                v-if="recentActivities.length === 0"
                class="text-center pa-4"
              >
                <v-icon size="48" color="grey-lighten-1">mdi-timer-sand</v-icon>
                <div class="text-caption text-medium-emphasis mt-2">
                  No recent activity
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Actions -->
    <v-row class="mt-2" no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="quick-actions" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="quick-actions-header mb-4">
              <h3 class="font-weight-bold">Quick Actions</h3>
              <p class="text-caption text-medium-emphasis">
                Frequently used operations
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

    <!-- Expense Tracker Dialog -->
    <ExpenseTracker
      v-model="showExpenseDialog"
      @expense-recorded="handleExpenseRecorded"
    />

    <!-- Notifications Panel -->
    <v-navigation-drawer
      v-model="showNotifications"
      location="right"
      width="400"
      temporary
    >
      <v-list>
        <v-list-item>
          <v-list-item-title class="font-weight-bold"
            >Notifications</v-list-item-title
          >
          <template #append>
            <v-btn variant="text" size="small" @click="markAllRead"
              >Mark all read</v-btn
            >
          </template>
        </v-list-item>
        <v-divider />
        <v-list-item
          v-for="notif in notifications"
          :key="notif.id"
          :class="notif.read ? '' : 'unread'"
        >
          <template #prepend>
            <v-avatar size="40" :color="notif.color + '20'">
              <v-icon :color="notif.color" size="20">{{ notif.icon }}</v-icon>
            </v-avatar>
          </template>
          <v-list-item-title>{{ notif.title }}</v-list-item-title>
          <v-list-item-subtitle>{{ notif.message }}</v-list-item-subtitle>
          <template #append>
            <span class="text-caption text-medium-emphasis">{{
              notif.time
            }}</span>
          </template>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from "vue";
import { useAuthStore } from "~/stores/auth";
import { usePosStore } from "~/stores/pos";
import Chart from "chart.js/auto";
import DailyFinancialSummary from "~/components/DailyFinancialSummary.vue";
import ExpenseTracker from "~/components/ExpenseTracker.vue";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const authStore = useAuthStore();
const store = usePosStore();
const revenuePeriod = ref("7 days");
const revenueChartCanvas = ref<HTMLCanvasElement | null>(null);
const paymentChartCanvas = ref<HTMLCanvasElement | null>(null);
const showExpenseDialog = ref(false);
const showNotifications = ref(false);
const unreadNotifications = ref(3);

let revenueChartInstance: Chart | null = null;
let paymentChartInstance: Chart | null = null;

// ============ Quick Actions ============
const quickActions = [
  {
    text: "Add Product",
    icon: "mdi-plus",
    color: "linear-gradient(135deg, #2d6a4f, #1b4332)",
    action: () => navigateTo("/admin/products"),
  },
  {
    text: "View Orders",
    icon: "mdi-receipt",
    color: "linear-gradient(135deg, #e07a5f, #d66b4a)",
    action: () => navigateTo("/orders"),
  },
  {
    text: "Generate Report",
    icon: "mdi-chart-bar",
    color: "linear-gradient(135deg, #f4a261, #e9c46a)",
    action: () => navigateTo("/reports"),
  },
  {
    text: "Add Expense",
    icon: "mdi-cash-minus",
    color: "linear-gradient(135deg, #6b4e71, #4a3b52)",
    action: () => {
      showExpenseDialog.value = true;
    },
  },
  {
    text: "Manage Stock",
    icon: "mdi-warehouse",
    color: "linear-gradient(135deg, #2D6A4F, #1B4332)",
    action: () => navigateTo("/admin/inventory"),
  },
  {
    text: "View Analytics",
    icon: "mdi-chart-bar",
    color: "linear-gradient(135deg, #4A90D9, #2D6A4F)",
    action: () => navigateTo("/reports"),
  },
  {
    text: "Scan Product",
    icon: "mdi-barcode-scan",
    color: "linear-gradient(135deg, #6B4E71, #4A3B52)",
    action: () => navigateTo("/pos"),
  },
  {
    text: "View Debtors",
    icon: "mdi-account-cash",
    color: "linear-gradient(135deg, #E07A5F, #D66B4A)",
    action: () => navigateTo("/orders?filter=debt"),
  },
];

// ============ Health Indicators ============
const healthIndicators = computed(() => {
  const total = totalOrders.value;
  const revenue = totalRevenue.value;
  const debt = debtCount.value;
  const lowStock = lowStockCount.value;

  return [
    {
      label: "Revenue Health",
      value: revenue > 100000 ? "Excellent" : revenue > 50000 ? "Good" : "Fair",
      icon: "mdi-currency-usd",
      color:
        revenue > 100000 ? "#2D6A4F" : revenue > 50000 ? "#F4A261" : "#E07A5F",
      status: revenue > 100000 ? "good" : "warning",
    },
    {
      label: "Order Volume",
      value: total > 100 ? "High" : total > 50 ? "Medium" : "Low",
      icon: "mdi-cart-outline",
      color: total > 100 ? "#2D6A4F" : total > 50 ? "#F4A261" : "#E07A5F",
      status: total > 100 ? "good" : "warning",
    },
    {
      label: "Debt Level",
      value: debt === 0 ? "None" : debt <= 5 ? "Low" : "High",
      icon: "mdi-account-cash",
      color: debt === 0 ? "#2D6A4F" : debt <= 5 ? "#F4A261" : "#E07A5F",
      status: debt === 0 ? "good" : debt <= 5 ? "warning" : "danger",
    },
    {
      label: "Stock Status",
      value:
        lowStock === 0 ? "Healthy" : lowStock <= 5 ? "Caution" : "Critical",
      icon: "mdi-package-variant",
      color: lowStock === 0 ? "#2D6A4F" : lowStock <= 5 ? "#F4A261" : "#E07A5F",
      status: lowStock === 0 ? "good" : "warning",
    },
  ];
});

// ============ Data from Store ============
const allOrders = computed(() => store.AllOrders || []);
const allProducts = computed(() => store.products || []);
const AllLogs = computed(() => authStore.activityLogs || []);

// ============ Dates ============
const today = new Date().toISOString().split("T")[0];
const yesterday = new Date(Date.now() - 86400000).toISOString().split("T")[0];

// ============ Filtered Orders ============
const todayOrders = computed(() => {
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

// ============ Revenue Calculations ============
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

// ============ Order Calculations ============
const totalOrders = computed(() => allOrders.value.length);
const todayOrderCount = computed(() => todayOrders.value.length);
const yesterdayOrderCount = computed(() => yesterdayOrders.value.length);

// ============ Average Order Value ============
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

// ============ Items Sold ============
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

// ============ Inventory Stats ============
const totalProducts = computed(() => allProducts.value.length);

const lowStockCount = computed(() => {
  return allProducts.value.filter((p) => {
    const stock = p.inventory?.available || p.inventory?.quantity || 0;
    const reorder = p.inventory?.reorder_level || 10;
    return stock > 0 && stock <= reorder;
  }).length;
});

const outOfStockCount = computed(() => {
  return allProducts.value.filter((p) => {
    const stock = p.inventory?.available || p.inventory?.quantity || 0;
    return stock <= 0;
  }).length;
});

// ============ Debt Stats ============
const debtCount = computed(() => {
  return allOrders.value.filter(
    (order) =>
      order.payment_mode === "debt" && order.payment_status === "pending"
  ).length;
});

// ============ Percentage Changes ============
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

const inventoryChangeClass = computed(() =>
  inventoryChange.value.isPositive ? "positive" : "negative"
);
const inventoryChangeIcon = computed(() =>
  inventoryChange.value.isPositive ? "mdi-arrow-up" : "mdi-arrow-down"
);
const inventoryChangePercent = computed(() => inventoryChange.value.percent);

// ============ Helper Functions ============
const getTimeGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return "Good Morning";
  if (hour < 17) return "Good Afternoon";
  return "Good Evening";
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

// ============ Top Products ============
const topProducts = computed(() => {
  const productMap = new Map();

  allOrders.value.forEach((order) => {
    const items = order.items || [];
    items.forEach((item: any) => {
      const key = item.name || item.product_name;
      if (!key) return;
      if (!productMap.has(key)) {
        productMap.set(key, {
          name: key,
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

// ============ Recent Orders ============
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
      receiptNumber: order.receipt_number,
      time: new Date(order.created_at).toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
      }),
      orderType: order.order_type || order.orderType || "takeaway",
      customerName: order.customer_name || order.customerName,
      total: order.total,
      status: order.payment_status || order.order_status || "completed",
    }));
});

// ============ Revenue Chart ============
const getRevenueChartData = () => {
  let days = 7;
  if (revenuePeriod.value === "30 days") days = 30;
  if (revenuePeriod.value === "90 days") days = 90;

  const revenueMap = new Map();
  const today = new Date();

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    const dateStr = date.toISOString().split("T")[0];
    revenueMap.set(dateStr, 0);
  }

  allOrders.value.forEach((order) => {
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

  return { labels, data };
};

const revenuePeriodLabel = computed(() => {
  return revenuePeriod.value;
});

const updateRevenueChart = () => {
  nextTick(() => {
    if (revenueChartInstance) {
      revenueChartInstance.destroy();
      revenueChartInstance = null;
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
            pointBackgroundColor: "#2D6A4F",
            pointRadius: 3,
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
              label: (context) =>
                `Revenue: KSh ${context.raw.toLocaleString()}`,
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
            grid: { display: false },
            ticks: {
              maxRotation: 45,
              autoSkip: true,
              maxTicksLimit: 10,
            },
          },
        },
      },
    });
  });
};

// ============ Payment Chart ============
const updatePaymentChart = () => {
  if (paymentChartInstance) {
    paymentChartInstance.destroy();
    paymentChartInstance = null;
  }

  const ctx = paymentChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  const paymentMap = new Map();
  console.log("Today Orders:", todayOrders.value);
  todayOrders.value.forEach((order) => {
    const mode = order.payment_mode || "cash";
    console.log("Order Payment Mode:", mode);
    paymentMap.set(mode, (paymentMap.get(mode) || 0) + 1);
  });

  const colors: Record<string, string> = {
    cash: "#2D6A4F",
    mpesa: "#4A90D9",
    debt: "#E07A5F",
    card: "#6B4E71",
  };

  const labels = Array.from(paymentMap.keys());
  const data = Array.from(paymentMap.values());
  const backgroundColors = labels.map((label) => colors[label] || "#6B7280");

  paymentChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels.map((l) => l.charAt(0).toUpperCase() + l.slice(1)),
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

// ============ Activities ============
const activityMeta: Record<string, { icon: string; color: string }> = {
  user_logged_in: { icon: "mdi-login", color: "#2D6A4F" },
  user_logout: { icon: "mdi-logout", color: "#E07A5F" },
  user_registered: { icon: "mdi-account-plus", color: "#6B4E71" },
  order_created: { icon: "mdi-cart-plus", color: "#2D6A4F" },
  product_created: { icon: "mdi-coffee", color: "#E07A5F" },
  user_deleted: { icon: "mdi-account-remove", color: "#E07A5F" },
  user_status_changed: { icon: "mdi-account-cancel", color: "#E07A5F" },
  debt_payment_updated: { icon: "mdi-currency-usd", color: "#2D6A4F" },
};

const recentActivities = computed(() => {
  return [...AllLogs.value]
    .sort(
      (a: any, b: any) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
    .slice(0, 5)
    .map((log: any, index) => {
      const meta = activityMeta[log.action] || {
        icon: "mdi-information",
        color: "#6B7280",
      };
      return {
        id: log._id || log.id || index,
        text: log.message || log.action,
        time: new Date(log.created_at).toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
        }),
        icon: meta.icon,
        color: meta.color,
      };
    });
});

// ============ Notifications ============
const notifications = ref([
  {
    id: 1,
    title: "Low Stock Alert",
    message: "Sawa Soap 225g is running low (5 items left)",
    icon: "mdi-alert",
    color: "#E07A5F",
    time: "5 min ago",
    read: false,
  },
  {
    id: 2,
    title: "New Order",
    message: "Order #RCP-2026-001 placed by John Doe",
    icon: "mdi-cart-plus",
    color: "#2D6A4F",
    time: "15 min ago",
    read: false,
  },
  {
    id: 3,
    title: "Payment Received",
    message: "M-Pesa payment of KSh 750 received",
    icon: "mdi-cash",
    color: "#2D6A4F",
    time: "30 min ago",
    read: false,
  },
]);

const markAllRead = () => {
  notifications.value = notifications.value.map((n) => ({ ...n, read: true }));
  unreadNotifications.value = 0;
};

// ============ Date Formatting ============
const currentDate = new Date().toLocaleDateString("en-US", {
  weekday: "long",
  day: "numeric",
});
const currentFullDate = new Date().toLocaleDateString("en-US", {
  month: "long",
  year: "numeric",
});

// ============ Watchers ============
watch(revenuePeriod, () => {
  updateRevenueChart();
});

// ============ Actions ============
const handleExpenseRecorded = async () => {
  await store.getAllOrders();
};

// ============ Lifecycle ============
onMounted(async () => {
  await Promise.all([
    store.getAllOrders(),
    store.getAllProducts(),
    authStore.getActivityLogs(),
  ]);

  setTimeout(() => {
    updateRevenueChart();
    updatePaymentChart();
  }, 200);
});
</script>

<style scoped>
.dashboard-container {
  padding: 16px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Welcome Card */
.welcome-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f6f2 100%);
}

.greeting-title {
  font-family: "Playfair Display", serif;
  font-size: 32px;
  font-weight: 800;
  color: #1b4332;
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

/* Health Indicators */
.health-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.health-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 12px;
  background: #fafaf8;
  transition: all 0.3s ease;
}

.health-item:hover {
  background: #f0ede5;
}

.health-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.health-info {
  flex: 1;
}

.health-value {
  font-size: 13px;
  font-weight: 700;
}

.health-label {
  font-size: 10px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.health-status {
  display: flex;
  align-items: center;
}

.health-status.good {
  color: #2d6a4f;
}
.health-status.warning {
  color: #f4a261;
}
.health-status.danger {
  color: #e07a5f;
}

/* Stats Cards */
.stat-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.04);
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08) !important;
}

.stat-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 20px;
  color: #1b4332;
  line-height: 1.2;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 12px;
  margin-top: 4px;
}

.stat-change.positive {
  color: #2d6a4f;
}
.stat-change.negative {
  color: #e07a5f;
}

/* Mini Stats */
.stat-card.mini {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.mini-stat-value {
  font-size: 20px;
  font-weight: 800;
  color: #1b4332;
}

.mini-stat-label {
  font-size: 11px;
  color: #6b7280;
  margin-top: 2px;
}

/* Charts */
.chart-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.04);
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
  max-width: 120px;
}

.chart-container {
  height: 250px;
  position: relative;
}

.payment-chart {
  height: 200px;
}

/* Orders & Activity */
.recent-orders-card,
.activity-card,
.quick-actions {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}

.card-title {
  font-size: 16px;
  color: #1b4332;
}

.card-subtitle {
  font-size: 12px;
  color: #6b7280;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-row {
  padding: 12px;
  background: #f8f6f2;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.order-row:hover {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.order-receipt {
  color: #1b4332;
}

.order-type-badge {
  font-size: 10px;
  font-weight: 600;
  color: white !important;
}

.order-amount {
  color: #e07a5f;
}

.order-status {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
}

.activity-timeline {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  padding: 12px;
  background: #f8f6f2;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Quick Actions */
.quick-actions {
  background: white;
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
  height: 100%;
}

.action-card:hover {
  transform: translateY(-4px);
  background: white;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-text {
  font-size: 13px;
  text-align: center;
  color: #1b4332;
}

/* Notifications */
.unread {
  background: #f0f9f4;
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 12px;
  }

  .greeting-title {
    font-size: 24px;
  }

  .stat-value {
    font-size: 18px;
  }

  .stat-icon-wrapper {
    width: 40px;
    height: 40px;
    border-radius: 12px;
  }

  .stat-icon-wrapper .v-icon {
    font-size: 20px !important;
  }

  .chart-container {
    height: 200px;
  }

  .payment-chart {
    height: 180px;
  }

  .action-card {
    padding: 16px;
  }

  .action-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
  }

  .action-icon .v-icon {
    font-size: 20px !important;
  }

  .action-text {
    font-size: 12px;
  }

  .order-row {
    padding: 10px;
  }

  .activity-item {
    padding: 10px;
  }

  .mini-stat-value {
    font-size: 16px;
  }

  .health-item {
    padding: 6px 10px;
  }

  .health-value {
    font-size: 12px;
  }

  .health-icon {
    width: 30px;
    height: 30px;
  }

  .health-icon .v-icon {
    font-size: 16px !important;
  }
}

@media (max-width: 480px) {
  .greeting-title {
    font-size: 20px;
  }

  .stat-value {
    font-size: 16px;
  }

  .chart-container {
    height: 160px;
  }

  .payment-chart {
    height: 150px;
  }

  .stat-card.mini {
    padding: 8px;
  }

  .mini-stat-value {
    font-size: 14px;
  }

  .mini-stat-label {
    font-size: 10px;
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
}
</style>
