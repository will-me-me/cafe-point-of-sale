<!-- frontend/pages/reports/profit/index.vue -->
<template>
  <div class="profit-report-container">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#2D6A4F">mdi-chart-timeline</v-icon>
          Reports
        </div>
        <h1 class="page-title">Profit Report</h1>
        <p class="page-subtitle">Analyze margins and profitability</p>
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
                  <v-icon size="24">mdi-cash</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">
                  KSh {{ totalCost.toLocaleString() }}
                </div>
                <div class="stat-label">Total Cost</div>
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
                  KSh {{ totalProfit.toLocaleString() }}
                </div>
                <div class="stat-label">Total Profit</div>
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
                  <v-icon size="24">mdi-percent</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ profitMargin }}%</div>
                <div class="stat-label">Profit Margin</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Profit Chart -->
    <v-row no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Profit Analysis</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Revenue vs Cost vs Profit
                </div>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="profitChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Top Products -->
    <v-row no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="table-card" elevation="0" rounded="xl">
          <v-card-text class="pa-0">
            <div class="table-header pa-4">
              <span class="table-title font-weight-bold"
                >Product Profitability</span
              >
              <span class="table-count text-caption text-medium-emphasis">
                {{ topProducts.length }} products
              </span>
            </div>
            <v-data-table
              :headers="headers"
              :items="topProducts"
              :loading="loading"
              :items-per-page="10"
              class="profit-table"
              item-value="name"
            >
              <template v-slot:item.rank="{ index }">
                <div class="rank-cell">
                  <v-chip
                    :color="getRankColor(index)"
                    size="small"
                    text-color="white"
                  >
                    #{{ index + 1 }}
                  </v-chip>
                </div>
              </template>

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

              <template v-slot:item.revenue="{ item }">
                KSh {{ item.revenue.toFixed(2) }}
              </template>

              <template v-slot:item.cost="{ item }">
                KSh {{ item.cost.toFixed(2) }}
              </template>

              <template v-slot:item.profit="{ item }">
                <span
                  :class="
                    item.profit >= 0 ? 'profit-positive' : 'profit-negative'
                  "
                >
                  KSh {{ item.profit.toFixed(2) }}
                </span>
              </template>

              <template v-slot:item.margin="{ item }">
                <v-chip
                  :color="getMarginColor(item.margin)"
                  size="x-small"
                  text-color="white"
                >
                  {{ item.margin.toFixed(1) }}%
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

const profitChartCanvas = ref<HTMLCanvasElement | null>(null);
let profitChartInstance: Chart | null = null;

// Table Headers
const headers = [
  { title: "#", key: "rank", sortable: false },
  { title: "Product", key: "name", sortable: true },
  { title: "Revenue", key: "revenue", sortable: true },
  { title: "Cost", key: "cost", sortable: true },
  { title: "Profit", key: "profit", sortable: true },
  { title: "Margin", key: "margin", sortable: true },
];

// Computed
const orders = computed(() => store.AllOrders || []);
const products = computed(() => store.products || []);

const totalRevenue = computed(() => {
  return orders.value.reduce((sum, order) => sum + (order.total || 0), 0);
});

const totalCost = computed(() => {
  // Calculate cost based on product costs
  let cost = 0;
  orders.value.forEach((order) => {
    const items = order.items || [];
    items.forEach((item: any) => {
      // Find product cost
      const product = products.value.find(
        (p) => p.id === item.product_id || p.sku === item.sku
      );
      const unitCost = product?.pricing?.cost_price || item.cost_price || 0;
      cost += unitCost * (item.quantity || 1);
    });
  });
  return cost;
});

const totalProfit = computed(() => totalRevenue.value - totalCost.value);

const profitMargin = computed(() => {
  if (totalRevenue.value === 0) return 0;
  return ((totalProfit.value / totalRevenue.value) * 100).toFixed(1);
});

const topProducts = computed(() => {
  const productMap = new Map();

  orders.value.forEach((order) => {
    const items = order.items || [];
    items.forEach((item: any) => {
      const key = item.product_id || item.sku || item.name;
      if (!key) return;

      if (!productMap.has(key)) {
        const product = products.value.find(
          (p) => p.id === item.product_id || p.sku === item.sku
        );
        productMap.set(key, {
          id: key,
          name: item.name || item.product_name || "Unknown",
          sku: item.sku || product?.sku || "",
          revenue: 0,
          cost: 0,
          quantity: 0,
          unitCost: product?.pricing?.cost_price || item.cost_price || 0,
        });
      }

      const p = productMap.get(key);
      const quantity = item.quantity || 1;
      const unitPrice = item.unit_price || item.price || 0;
      p.revenue += unitPrice * quantity;
      p.cost += p.unitCost * quantity;
      p.quantity += quantity;
    });
  });

  const productList = Array.from(productMap.values());
  return productList
    .map((p) => ({
      ...p,
      profit: p.revenue - p.cost,
      margin: p.revenue > 0 ? ((p.revenue - p.cost) / p.revenue) * 100 : 0,
    }))
    .sort((a, b) => b.profit - a.profit)
    .slice(0, 20);
});

// Helper Methods
const getRankColor = (index: number) => {
  const colors = ["#2D6A4F", "#F4A261", "#E07A5F", "#6B4E71", "#4A90D9"];
  return colors[index] || "#6B7280";
};

const getMarginColor = (margin: number) => {
  if (margin >= 30) return "#2D6A4F";
  if (margin >= 20) return "#F4A261";
  if (margin >= 10) return "#E07A5F";
  return "#6B7280";
};

// Chart Methods
const updateProfitChart = () => {
  if (profitChartInstance) {
    profitChartInstance.destroy();
    profitChartInstance = null;
  }

  const ctx = profitChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  const labels = ["Revenue", "Cost", "Profit"];
  const data = [totalRevenue.value, totalCost.value, totalProfit.value];
  const colors = ["#2D6A4F", "#E07A5F", "#F4A261"];

  profitChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Amount (KSh)",
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
        tooltip: {
          callbacks: {
            label: (context) =>
              `${context.label}: KSh ${context.raw.toLocaleString()}`,
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

// Methods
const refreshData = async () => {
  loading.value = true;
  try {
    await Promise.all([store.getAllOrders(), store.getAllProducts()]);
    setTimeout(updateProfitChart, 100);
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
      totalRevenue: totalRevenue.value,
      totalCost: totalCost.value,
      totalProfit: totalProfit.value,
      profitMargin: profitMargin.value,
    },
    topProducts: topProducts.value,
  };

  const blob = new Blob([JSON.stringify(report, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `profit_report_${
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
.profit-report-container {
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
}

.table-title {
  font-size: 16px;
  color: #1b4332;
}

.profit-table :deep(.v-data-table__th) {
  background: #f8f6f2;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

.rank-cell {
  min-width: 40px;
}

.product-cell .product-sku {
  font-size: 11px;
}

.profit-positive {
  color: #2d6a4f;
  font-weight: 600;
}

.profit-negative {
  color: #e07a5f;
  font-weight: 600;
}

@media (max-width: 768px) {
  .profit-report-container {
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

  .profit-table :deep(.v-data-table__th),
  .profit-table :deep(.v-data-table__td) {
    padding: 8px 12px !important;
    font-size: 12px;
  }

  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
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
