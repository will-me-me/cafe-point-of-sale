<!-- frontend/pages/reports/inventory/index.vue -->
<template>
  <div class="inventory-report-container">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#2D6A4F">mdi-chart-pie</v-icon>
          Reports
        </div>
        <h1 class="page-title">Inventory Report</h1>
        <p class="page-subtitle">
          Monitor stock levels and inventory valuation
        </p>
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
                  style="background: #e07a5f20; color: #e07a5f"
                >
                  <v-icon size="24">mdi-currency-usd</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">
                  KSh {{ inventoryValue.toLocaleString() }}
                </div>
                <div class="stat-label">Total Inventory Value</div>
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
                  <v-icon size="24">mdi-alert</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ lowStockCount }}</div>
                <div class="stat-label">Low Stock Items</div>
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
                  <v-icon size="24">mdi-close-circle</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="stat-value">{{ outOfStockCount }}</div>
                <div class="stat-label">Out of Stock</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Inventory Value Chart -->
    <v-row no-gutters>
      <v-col cols="12" lg="8" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">
                  Stock Distribution
                </div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Inventory by product type
                </div>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="inventoryChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" lg="4" class="pa-2">
        <v-card class="chart-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <div class="chart-header">
              <div>
                <div class="chart-title font-weight-bold">Stock Status</div>
                <div class="chart-subtitle text-caption text-medium-emphasis">
                  Current stock levels
                </div>
              </div>
            </div>
            <div class="chart-container stock-status-chart">
              <canvas ref="stockStatusChartCanvas"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Inventory Table -->
    <v-row no-gutters>
      <v-col cols="12" class="pa-2">
        <v-card class="table-card" elevation="0" rounded="xl">
          <v-card-text class="pa-0">
            <div class="table-header pa-4">
              <span class="table-title font-weight-bold">Inventory Items</span>
              <div class="table-filters">
                <v-text-field
                  v-model="searchQuery"
                  placeholder="Search products..."
                  variant="outlined"
                  density="compact"
                  hide-details
                  class="search-field"
                  prepend-inner-icon="mdi-magnify"
                />
                <v-select
                  v-model="stockFilter"
                  :items="stockFilterOptions"
                  variant="outlined"
                  density="compact"
                  hide-details
                  class="filter-select"
                />
              </div>
            </div>
            <v-data-table
              :headers="headers"
              :items="filteredInventory"
              :loading="loading"
              :items-per-page="10"
              class="inventory-table"
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

              <template v-slot:item.inventory="{ item }">
                <div class="stock-cell">
                  <span :class="getStockClass(item)">
                    {{ getStock(item) }}
                  </span>
                  <div class="stock-bar">
                    <div
                      class="stock-bar-fill"
                      :style="{ width: getStockPercentage(item) + '%' }"
                      :class="getStockBarClass(item)"
                    ></div>
                  </div>
                </div>
              </template>

              <template v-slot:item.cost_price="{ item }">
                KSh {{ item.pricing?.cost_price || 0 }}
              </template>

              <template v-slot:item.total_value="{ item }">
                KSh
                {{ getStock(item) * (item.pricing?.cost_price || 0) }}
              </template>

              <template v-slot:item.status="{ item }">
                <v-chip
                  :color="getStatusColor(item)"
                  size="x-small"
                  text-color="white"
                >
                  {{ getStatusText(item) }}
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
const searchQuery = ref("");
const stockFilter = ref("");

const inventoryChartCanvas = ref<HTMLCanvasElement | null>(null);
const stockStatusChartCanvas = ref<HTMLCanvasElement | null>(null);

let inventoryChartInstance: Chart | null = null;
let stockStatusChartInstance: Chart | null = null;

// Filters
const stockFilterOptions = [
  { title: "All Items", value: "" },
  { title: "In Stock", value: "in_stock" },
  { title: "Low Stock", value: "low_stock" },
  { title: "Out of Stock", value: "out_of_stock" },
];

// Table Headers
const headers = [
  { title: "Product", key: "name", sortable: true },
  { title: "Stock", key: "inventory", sortable: true },
  { title: "Cost Price", key: "cost_price", sortable: true },
  { title: "Total Value", key: "total_value", sortable: true },
  { title: "Status", key: "status", sortable: true },
];

// Computed
const products = computed(() => store.products || []);

const getStock = (item: any) => {
  return item.inventory?.available || item.inventory?.quantity || 0;
};

const getStockPercentage = (item: any) => {
  const stock = getStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  return Math.min((stock / reorder) * 100, 100);
};

const totalProducts = computed(() => products.value.length);

const inventoryValue = computed(() => {
  return products.value.reduce((sum, item) => {
    const stock = getStock(item);
    const cost = item.pricing?.cost_price || 0;
    return sum + stock * cost;
  }, 0);
});

const lowStockCount = computed(() => {
  return products.value.filter((item) => {
    const stock = getStock(item);
    const reorder = item.inventory?.reorder_level || 10;
    return stock > 0 && stock <= reorder;
  }).length;
});

const outOfStockCount = computed(() => {
  return products.value.filter((item) => getStock(item) <= 0).length;
});

const filteredInventory = computed(() => {
  let filtered = [...products.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (item) =>
        item.name.toLowerCase().includes(query) ||
        item.sku.toLowerCase().includes(query)
    );
  }

  if (stockFilter.value) {
    filtered = filtered.filter((item) => {
      const stock = getStock(item);
      const reorder = item.inventory?.reorder_level || 10;
      if (stockFilter.value === "in_stock") return stock > reorder;
      if (stockFilter.value === "low_stock")
        return stock > 0 && stock <= reorder;
      if (stockFilter.value === "out_of_stock") return stock <= 0;
      return true;
    });
  }

  return filtered;
});

// Helper Methods
const getStockClass = (item: any) => {
  const stock = getStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  if (stock <= 0) return "stock-out";
  if (stock <= reorder) return "stock-low";
  return "stock-ok";
};

const getStockBarClass = (item: any) => {
  const percentage = getStockPercentage(item);
  if (percentage <= 25) return "danger";
  if (percentage <= 50) return "warning";
  return "normal";
};

const getStatusColor = (item: any) => {
  const stock = getStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  if (stock <= 0) return "#E07A5F";
  if (stock <= reorder) return "#F4A261";
  return "#2D6A4F";
};

const getStatusText = (item: any) => {
  const stock = getStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  if (stock <= 0) return "Out of Stock";
  if (stock <= reorder) return "Low Stock";
  return "In Stock";
};

// Chart Methods
const updateInventoryChart = () => {
  if (inventoryChartInstance) {
    inventoryChartInstance.destroy();
    inventoryChartInstance = null;
  }

  const ctx = inventoryChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  // Group by category or use tags
  const categoryMap = new Map();

  products.value.forEach((item) => {
    const category = item.category_id || item.tags?.[0] || "Uncategorized";
    const stock = getStock(item);
    const cost = item.pricing?.cost_price || 0;
    const value = stock * cost;

    categoryMap.set(category, (categoryMap.get(category) || 0) + value);
  });

  const sorted = Array.from(categoryMap.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8);

  const colors = [
    "#2D6A4F",
    "#E07A5F",
    "#F4A261",
    "#6B4E71",
    "#4A90D9",
    "#E9C46A",
    "#2A9D8F",
    "#E76F51",
  ];

  inventoryChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: sorted.map(([key]) => key),
      datasets: [
        {
          label: "Inventory Value (KSh)",
          data: sorted.map(([, value]) => value),
          backgroundColor: colors.slice(0, sorted.length),
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
            callback: (value) => "KSh " + value.toLocaleString(),
          },
        },
      },
    },
  });
};

const updateStockStatusChart = () => {
  if (stockStatusChartInstance) {
    stockStatusChartInstance.destroy();
    stockStatusChartInstance = null;
  }

  const ctx = stockStatusChartCanvas.value?.getContext("2d");
  if (!ctx) return;

  const inStock = products.value.filter((item) => {
    const stock = getStock(item);
    const reorder = item.inventory?.reorder_level || 10;
    return stock > reorder;
  }).length;

  const lowStock = products.value.filter((item) => {
    const stock = getStock(item);
    const reorder = item.inventory?.reorder_level || 10;
    return stock > 0 && stock <= reorder;
  }).length;

  const outStock = products.value.filter((item) => getStock(item) <= 0).length;

  stockStatusChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["In Stock", "Low Stock", "Out of Stock"],
      datasets: [
        {
          data: [inStock, lowStock, outStock],
          backgroundColor: ["#2D6A4F", "#F4A261", "#E07A5F"],
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
    updateInventoryChart();
    updateStockStatusChart();
  }, 100);
};

// Methods
const refreshData = async () => {
  loading.value = true;
  try {
    await store.getAllProducts();
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
    summary: {
      totalProducts: totalProducts.value,
      inventoryValue: inventoryValue.value,
      lowStock: lowStockCount.value,
      outOfStock: outOfStockCount.value,
    },
    items: products.value.map((item) => ({
      name: item.name,
      sku: item.sku,
      stock: getStock(item),
      costPrice: item.pricing?.cost_price || 0,
      totalValue: getStock(item) * (item.pricing?.cost_price || 0),
      status: getStatusText(item),
    })),
  };

  const blob = new Blob([JSON.stringify(report, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `inventory_report_${
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
.inventory-report-container {
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

.stock-status-chart {
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

.search-field {
  max-width: 250px;
}

.filter-select {
  max-width: 150px;
}

.inventory-table :deep(.v-data-table__th) {
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

.stock-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stock-ok {
  color: #2d6a4f;
  font-weight: 600;
}

.stock-low {
  color: #f4a261;
  font-weight: 600;
}

.stock-out {
  color: #e07a5f;
  font-weight: 600;
}

.stock-bar {
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
  width: 100px;
}

.stock-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

.stock-bar-fill.normal {
  background: #2d6a4f;
}

.stock-bar-fill.warning {
  background: #f4a261;
}

.stock-bar-fill.danger {
  background: #e07a5f;
}

@media (max-width: 768px) {
  .inventory-report-container {
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

  .stock-status-chart {
    height: 180px;
  }

  .table-header {
    flex-direction: column;
    align-items: stretch;
  }

  .table-filters {
    flex-direction: column;
  }

  .search-field,
  .filter-select {
    max-width: 100%;
  }

  .inventory-table :deep(.v-data-table__th),
  .inventory-table :deep(.v-data-table__td) {
    padding: 8px 12px !important;
    font-size: 12px;
  }

  .stock-bar {
    width: 60px;
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

  .stock-status-chart {
    height: 160px;
  }

  .table-title {
    font-size: 14px;
  }
}
</style>
