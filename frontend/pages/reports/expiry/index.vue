<!-- frontend/pages/reports/expiry/index.vue -->
<template>
  <div class="expiry-report-container">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#2D6A4F">mdi-calendar-clock</v-icon>
          Reports
        </div>
        <h1 class="page-title">Expiry Report</h1>
        <p class="page-subtitle">Track products nearing expiration</p>
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
                  <v-icon size="24">mdi-package-variant</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ totalProducts }}</div>
                <div class="stat-label">Total Products</div>
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
                  <v-icon size="24">mdi-clock-alert</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ expiringSoon }}</div>
                <div class="stat-label">Expiring Soon (7 days)</div>
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
                  <v-icon size="24">mdi-calendar-remove</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ expiringWithinMonth }}</div>
                <div class="stat-label">Expiring Within 30 Days</div>
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
                  <v-icon size="24">mdi-currency-usd</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">
                  KSh {{ valueAtRisk.toLocaleString() }}
                </div>
                <div class="stat-label">Value at Risk</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Expiry Timeline -->
    <v-row no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Expiry Timeline</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Products expiring over time
                </div>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="expiryChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Expiry Table -->
    <v-row no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="table-card" elevation="0" rounded="xl">
          <v-card-text class="pa-0">
            <div class="table-header pa-4">
              <span class="table-title font-weight-bold"
                >Products by Expiry</span
              >
              <div class="table-filters">
                <v-select
                  v-model="expiryFilter"
                  :items="expiryFilterOptions"
                  variant="outlined"
                  density="compact"
                  hide-details
                  class="filter-select"
                />
              </div>
            </div>
            <v-data-table
              :headers="headers"
              :items="filteredExpiryItems"
              :loading="loading"
              :items-per-page="10"
              class="expiry-table"
              item-value="id"
            >
              <template v-slot:item.name="{ item }">
                <div class="product-cell">
                  <div class="product-name font-weight-medium">
                    {{ item.name }}
                  </div>
                  <div class="product-sku text-caption text-medium-emphasis">
                    SKU: {{ item.sku }}
                  </div>
                </div>
              </template>

              <template v-slot:item.expiry_date="{ item }">
                <div class="expiry-cell">
                  <div>{{ formatDate(item.expiry_date) }}</div>
                  <div
                    class="days-remaining"
                    :class="getDaysClass(item.days_remaining)"
                  >
                    {{ item.days_remaining }} days
                  </div>
                </div>
              </template>

              <template v-slot:item.stock="{ item }">
                {{ item.stock }}
              </template>

              <template v-slot:item.value="{ item }">
                KSh {{ (item.stock * item.cost_price).toFixed(2) }}
              </template>

              <template v-slot:item.status="{ item }">
                <v-chip
                  :color="getExpiryColor(item.days_remaining)"
                  size="x-small"
                  text-color="white"
                >
                  {{ getExpiryStatus(item.days_remaining) }}
                </v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import Chart from "chart.js/auto";
import { usePosStore } from "~/stores/pos";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const store = usePosStore();
const loading = ref(false);
const expiryFilter = ref("all");

const expiryChartCanvas = ref<HTMLCanvasElement | null>(null);
let expiryChartInstance: Chart | null = null;

// Filters
const expiryFilterOptions = [
  { title: "All Products", value: "all" },
  { title: "Expiring Soon (7 days)", value: "soon" },
  { title: "Expiring Within 30 Days", value: "month" },
  { title: "Expired", value: "expired" },
];

// Table Headers
const headers = [
  { title: "Product", key: "name", sortable: true },
  { title: "Expiry Date", key: "expiry_date", sortable: true },
  { title: "Stock", key: "stock", sortable: true },
  { title: "Value", key: "value", sortable: true },
  { title: "Status", key: "status", sortable: true },
];

// Mock expiry data (since your products may not have expiry fields yet)
const mockExpiryItems = ref([]);

// Computed
const products = computed(() => store.products || []);

// Generate mock expiry data for demonstration
const generateExpiryData = () => {
  const items = [];
  const today = new Date();

  products.value.forEach((product) => {
    // Skip products without inventory
    if (!product.inventory) return;

    const stock =
      product.inventory.available || product.inventory.quantity || 0;
    if (stock <= 0) return;

    // Random expiry date (0-90 days from now)
    const daysToExpiry = Math.floor(Math.random() * 90);
    const expiryDate = new Date(today);
    expiryDate.setDate(today.getDate() + daysToExpiry);

    items.push({
      id: product.id || product._id,
      name: product.name,
      sku: product.sku || "",
      expiry_date: expiryDate.toISOString(),
      days_remaining: daysToExpiry,
      stock: stock,
      cost_price: product.pricing?.cost_price || 0,
    });
  });

  mockExpiryItems.value = items;
};

const totalProducts = computed(() => products.value.length);

const expiringSoon = computed(() => {
  return mockExpiryItems.value.filter(
    (item) => item.days_remaining <= 7 && item.days_remaining >= 0
  ).length;
});

const expiringWithinMonth = computed(() => {
  return mockExpiryItems.value.filter(
    (item) => item.days_remaining <= 30 && item.days_remaining > 7
  ).length;
});

const valueAtRisk = computed(() => {
  return mockExpiryItems.value
    .filter((item) => item.days_remaining <= 30 && item.days_remaining >= 0)
    .reduce((sum, item) => sum + item.stock * item.cost_price, 0);
});

const filteredExpiryItems = computed(() => {
  let filtered = [...mockExpiryItems.value];

  if (expiryFilter.value === "soon") {
    filtered = filtered.filter(
      (item) => item.days_remaining <= 7 && item.days_remaining >= 0
    );
  } else if (expiryFilter.value === "month") {
    filtered = filtered.filter(
      (item) => item.days_remaining <= 30 && item.days_remaining > 7
    );
  } else if (expiryFilter.value === "expired") {
    filtered = filtered.filter((item) => item.days_remaining < 0);
  }

  return filtered.sort((a, b) => a.days_remaining - b.days_remaining);
});

// Helper Methods
const formatDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

const getDaysClass = (days: number) => {
  if (days < 0) return "expired";
  if (days <= 7) return "critical";
  if (days <= 30) return "warning";
  return "normal";
};

const getExpiryColor = (days: number) => {
  if (days < 0) return "#E07A5F";
  if (days <= 7) return "#E07A5F";
  if (days <= 30) return "#F4A261";
  return "#2D6A4F";
};

const getExpiryStatus = (days: number) => {
  if (days < 0) return "Expired";
  if (days <= 7) return "Critical";
  if (days <= 30) return "Warning";
  return "Good";
};

// Chart Methods
const updateExpiryChart = () => {
  if (expiryChartInstance) {
    expiryChartInstance.destroy();
    expiryChartInstance = null;
  }

  const ctx = expiryChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  const labels = ["Expired", "0-7 Days", "8-30 Days", "31-60 Days", "60+ Days"];
  const data = [
    mockExpiryItems.value.filter((i) => i.days_remaining < 0).length,
    mockExpiryItems.value.filter(
      (i) => i.days_remaining >= 0 && i.days_remaining <= 7
    ).length,
    mockExpiryItems.value.filter(
      (i) => i.days_remaining > 7 && i.days_remaining <= 30
    ).length,
    mockExpiryItems.value.filter(
      (i) => i.days_remaining > 30 && i.days_remaining <= 60
    ).length,
    mockExpiryItems.value.filter((i) => i.days_remaining > 60).length,
  ];

  const colors = ["#E07A5F", "#E07A5F", "#F4A261", "#F4A261", "#2D6A4F"];

  expiryChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Products",
          data: data,
          backgroundColor: colors.map((c) => c + "80"),
          borderColor: colors,
          borderWidth: 2,
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
          },
        },
      },
    },
  });
};

// Methods
const refreshData = async () => {
  loading.value = true;
  try {
    await store.getAllProducts();
    generateExpiryData();
    setTimeout(updateExpiryChart, 100);
  } catch (error) {
    console.error("Error refreshing data:", error);
  } finally {
    loading.value = false;
  }
};

const exportReport = () => {
  const report = {
    generated: new Date().toISOString(),
    summary: {
      totalProducts: totalProducts.value,
      expiringSoon: expiringSoon.value,
      expiringWithinMonth: expiringWithinMonth.value,
      valueAtRisk: valueAtRisk.value,
    },
    items: mockExpiryItems.value.map((item) => ({
      name: item.name,
      sku: item.sku,
      expiryDate: item.expiry_date,
      daysRemaining: item.days_remaining,
      stock: item.stock,
      value: item.stock * item.cost_price,
      status: getExpiryStatus(item.days_remaining),
    })),
  };

  const blob = new Blob([JSON.stringify(report, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `expiry_report_${
    new Date().toISOString().split("T")[0]
  }.json`;
  link.click();
  URL.revokeObjectURL(url);
};

// Lifecycle
onMounted(async () => {
  await refreshData();
});
</script>

<style scoped>
.expiry-report-container {
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

.table-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.table-title {
  font-size: 16px;
  color: #1b4332;
}

.table-filters {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select {
  max-width: 200px;
}

.expiry-table :deep(.v-data-table__th) {
  background: #f8f6f2;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

.product-cell .product-sku {
  font-size: 11px;
}

.expiry-cell .days-remaining {
  font-size: 11px;
  font-weight: 600;
}

.days-remaining.normal {
  color: #2d6a4f;
}

.days-remaining.warning {
  color: #f4a261;
}

.days-remaining.critical {
  color: #e07a5f;
}

.days-remaining.expired {
  color: #e07a5f;
  text-decoration: line-through;
}

@media (max-width: 768px) {
  .expiry-report-container {
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

  .expiry-table :deep(.v-data-table__th),
  .expiry-table :deep(.v-data-table__td) {
    padding: 8px 12px !important;
    font-size: 12px;
  }

  .table-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-select {
    max-width: 100%;
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

  .table-title {
    font-size: 14px;
  }
}
</style>
