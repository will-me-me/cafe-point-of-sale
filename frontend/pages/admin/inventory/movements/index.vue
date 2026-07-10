<!-- pages/admin/inventory/movements/index.vue -->
<template>
  <div class="movements-container">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">
          <v-icon size="16" color="#E07A5F">mdi-swap-horizontal</v-icon>
          Inventory Management
        </div>
        <h1 class="page-title">Stock Movements</h1>
        <p class="page-subtitle">Audit trail of all inventory changes</p>
      </div>
      <div class="header-actions">
        <v-btn variant="outlined" color="#2D6A4F" @click="exportMovements">
          <v-icon start>mdi-download</v-icon>
          Export
        </v-btn>
        <v-btn color="#2D6A4F" @click="refreshMovements">
          <v-icon start>mdi-refresh</v-icon>
          Refresh
        </v-btn>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-content">
          <div class="stat-value">{{ totalMovements }}</div>
          <div class="stat-label">Total Movements</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-content">
          <div class="stat-value" style="color: #2d6a4f">{{ inMovements }}</div>
          <div class="stat-label">Stock In</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-content">
          <div class="stat-value" style="color: #e07a5f">
            {{ outMovements }}
          </div>
          <div class="stat-label">Stock Out</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-content">
          <div class="stat-value" style="color: #f4a261">{{ adjustments }}</div>
          <div class="stat-label">Adjustments</div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-wrapper">
        <v-icon class="search-icon">mdi-magnify</v-icon>
        <input
          v-model="searchQuery"
          placeholder="Search movements..."
          class="search-input"
          @input="filterMovements"
        />
      </div>
      <div class="filter-group">
        <select
          v-model="typeFilter"
          class="filter-select"
          @change="filterMovements"
        >
          <option value="">All Types</option>
          <option value="purchase">Purchase</option>
          <option value="sale">Sale</option>
          <option value="transfer">Transfer</option>
          <option value="adjustment">Adjustment</option>
          <option value="damage">Damage</option>
          <option value="expired">Expired</option>
          <option value="returned">Returned</option>
        </select>
        <input
          type="date"
          v-model="dateFrom"
          class="filter-date"
          @change="filterMovements"
        />
        <span class="date-separator">to</span>
        <input
          type="date"
          v-model="dateTo"
          class="filter-date"
          @change="filterMovements"
        />
        <v-btn
          color="#2D6A4F"
          variant="tonal"
          size="small"
          @click="resetFilters"
        >
          Reset
        </v-btn>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-grid">
      <v-skeleton-loader
        v-for="n in 6"
        :key="n"
        type="table"
        class="movement-skeleton"
      />
    </div>

    <!-- Movements Table -->
    <div v-else>
      <v-card class="movements-table-card" elevation="0" rounded="xl">
        <v-card-text class="pa-0">
          <v-table class="movements-table">
            <thead>
              <tr>
                <th>Date & Time</th>
                <th>Product</th>
                <th>Type</th>
                <th class="text-center">Quantity</th>
                <th class="text-center">User</th>
                <th>Reason</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="movement in filteredMovements"
                :key="movement.id || movement._id"
              >
                <td>
                  <div class="date-time">
                    <div class="date">
                      {{ formatDate(movement.created_at) }}
                    </div>
                    <div class="time">
                      {{ formatTime(movement.created_at) }}
                    </div>
                  </div>
                </td>
                <td>
                  <div class="product-info">
                    <div class="product-name">
                      {{ movement.product_name || movement.product_id }}
                    </div>
                    <div class="product-sku" v-if="movement.sku">
                      SKU: {{ movement.sku }}
                    </div>
                  </div>
                </td>
                <td>
                  <v-chip
                    :color="getTypeColor(movement.type)"
                    size="small"
                    text-color="white"
                  >
                    <v-icon start size="14">{{
                      getTypeIcon(movement.type)
                    }}</v-icon>
                    {{ movement.type }}
                  </v-chip>
                </td>
                <td class="text-center">
                  <span
                    :class="movement.quantity > 0 ? 'positive' : 'negative'"
                  >
                    {{ movement.quantity > 0 ? "+" : ""
                    }}{{ movement.quantity }}
                  </span>
                </td>
                <td class="text-center">
                  {{ movement.created_by || "System" }}
                </td>
                <td>
                  <div class="reason-text">{{ movement.reason || "-" }}</div>
                  <div v-if="movement.notes" class="notes-text">
                    <v-icon size="12">mdi-note-text</v-icon>
                    {{ movement.notes }}
                  </div>
                </td>
                <td class="text-center">
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    color="#2D6A4F"
                    @click="viewMovement(movement)"
                  >
                    <v-icon size="18">mdi-eye</v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>

        <v-divider></v-divider>

        <!-- Pagination -->
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            :total-visible="5"
            @update:model-value="filterMovements"
          />
          <span class="pagination-info">
            Showing {{ (currentPage - 1) * pageSize + 1 }} -
            {{ Math.min(currentPage * pageSize, filteredMovements.length) }}
            of {{ filteredMovements.length }}
          </span>
        </v-card-actions>
      </v-card>
    </div>

    <!-- Movement Detail Dialog -->
    <v-dialog v-model="detailDialog.show" max-width="600">
      <v-card class="detail-dialog">
        <div class="dialog-header">
          <h3>Movement Details</h3>
          <v-btn icon variant="text" @click="detailDialog.show = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <v-card-text>
          <div v-if="detailDialog.movement" class="detail-content">
            <div class="detail-row">
              <span class="detail-label">Date & Time</span>
              <span class="detail-value">{{
                formatFullDate(detailDialog.movement.created_at)
              }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Product</span>
              <span class="detail-value">{{
                detailDialog.movement.product_name ||
                detailDialog.movement.product_id
              }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Type</span>
              <span class="detail-value">
                <v-chip
                  :color="getTypeColor(detailDialog.movement.type)"
                  size="small"
                  text-color="white"
                >
                  {{ detailDialog.movement.type }}
                </v-chip>
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Quantity</span>
              <span
                class="detail-value"
                :class="
                  detailDialog.movement.quantity > 0 ? 'positive' : 'negative'
                "
              >
                {{ detailDialog.movement.quantity > 0 ? "+" : ""
                }}{{ detailDialog.movement.quantity }}
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">User</span>
              <span class="detail-value">{{
                detailDialog.movement.created_by || "System"
              }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Reason</span>
              <span class="detail-value">{{
                detailDialog.movement.reason || "-"
              }}</span>
            </div>
            <div class="detail-row" v-if="detailDialog.movement.notes">
              <span class="detail-label">Notes</span>
              <span class="detail-value">{{
                detailDialog.movement.notes
              }}</span>
            </div>
            <div class="detail-row" v-if="detailDialog.movement.reference_id">
              <span class="detail-label">Reference</span>
              <span class="detail-value">{{
                detailDialog.movement.reference_id
              }}</span>
            </div>
          </div>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="detailDialog.show = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

// State
const movements = ref([]);
const loading = ref(true);
const searchQuery = ref("");
const typeFilter = ref("");
const dateFrom = ref("");
const dateTo = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const detailDialog = ref({
  show: false,
  movement: null,
});

// Computed
const totalMovements = computed(() => movements.value.length);

const inMovements = computed(
  () => movements.value.filter((m) => m.quantity > 0).length
);

const outMovements = computed(
  () => movements.value.filter((m) => m.quantity < 0).length
);

const adjustments = computed(
  () =>
    movements.value.filter(
      (m) =>
        m.type === "adjustment" || m.type === "damage" || m.type === "expired"
    ).length
);

const filteredMovements = computed(() => {
  let filtered = [...movements.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (m) =>
        (m.product_name && m.product_name.toLowerCase().includes(query)) ||
        (m.sku && m.sku.toLowerCase().includes(query)) ||
        (m.reason && m.reason.toLowerCase().includes(query))
    );
  }

  if (typeFilter.value) {
    filtered = filtered.filter((m) => m.type === typeFilter.value);
  }

  if (dateFrom.value) {
    filtered = filtered.filter(
      (m) => new Date(m.created_at) >= new Date(dateFrom.value)
    );
  }

  if (dateTo.value) {
    filtered = filtered.filter(
      (m) => new Date(m.created_at) <= new Date(dateTo.value + "T23:59:59")
    );
  }

  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filtered.slice(start, end);
});

const totalPages = computed(() =>
  Math.ceil(filteredMovements.value.length / pageSize.value)
);

// Methods
const formatDate = (date: string) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

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
    second: "2-digit",
  });
};

const getTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    purchase: "#2D6A4F",
    sale: "#E07A5F",
    transfer: "#4A90D9",
    adjustment: "#F4A261",
    damage: "#E76F51",
    expired: "#6B7280",
    returned: "#2D6A4F",
  };
  return colors[type] || "#6B7280";
};

const getTypeIcon = (type: string) => {
  const icons: Record<string, string> = {
    purchase: "mdi-arrow-up",
    sale: "mdi-arrow-down",
    transfer: "mdi-swap-horizontal",
    adjustment: "mdi-tune",
    damage: "mdi-alert",
    expired: "mdi-calendar-remove",
    returned: "mdi-undo",
  };
  return icons[type] || "mdi-circle";
};

const filterMovements = () => {
  // Computed handles filtering
};

const resetFilters = () => {
  searchQuery.value = "";
  typeFilter.value = "";
  dateFrom.value = "";
  dateTo.value = "";
  currentPage.value = 1;
};

const viewMovement = (movement: any) => {
  detailDialog.value = {
    show: true,
    movement: movement,
  };
};

const refreshMovements = async () => {
  loading.value = true;
  try {
    // TODO: API Call
    // movements.value = await $fetch('/api/v1/inventory/movements');

    // Mock data
    movements.value = [
      {
        id: "1",
        product_id: "PROD-001",
        product_name: "Pishori Rice 90kg Sack",
        sku: "PISHORI-90KG",
        type: "purchase",
        quantity: 90,
        created_at: "2026-07-03T10:30:00Z",
        created_by: "John Doe",
        reason: "Received new stock",
        notes: "PO #PO-2026-001",
        reference_id: "PO-2026-001",
      },
      {
        id: "2",
        product_id: "PROD-002",
        product_name: "Tuzo Milk 500ml",
        sku: "TUZO-MILK-500ML",
        type: "sale",
        quantity: -5,
        created_at: "2026-07-03T11:45:00Z",
        created_by: "Jane Smith",
        reason: "Customer purchase",
        notes: "Order #ORD-2026-001",
        reference_id: "ORD-2026-001",
      },
      {
        id: "3",
        product_id: "PROD-003",
        product_name: "Sawa Soap 225g",
        sku: "SAWA-SOAP-225G",
        type: "adjustment",
        quantity: -2,
        created_at: "2026-07-03T09:15:00Z",
        created_by: "Admin",
        reason: "Physical count adjustment",
        notes: "Stock discrepancy found during inventory",
      },
    ];
  } catch (error) {
    console.error("Error loading movements:", error);
  } finally {
    loading.value = false;
  }
};

const exportMovements = () => {
  console.log("Exporting movements...");
};

onMounted(() => {
  refreshMovements();
});
</script>

<style scoped>
.movements-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Reuse styles from inventory page */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 16px 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-value {
  font-size: 24px;
  font-weight: 800;
  color: #1b4332;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

.page-badge {
  font-size: 12px;
  font-weight: 600;
  color: #e07a5f;
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

.header-actions {
  display: flex;
  gap: 12px;
}

.filters-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-wrapper {
  flex: 1;
  min-width: 200px;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 40px;
  padding: 0 16px;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.search-icon {
  color: #9ca3af;
}

.search-input {
  flex: 1;
  border: none;
  padding: 12px 0;
  font-size: 14px;
  outline: none;
  background: transparent;
}

.filter-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-select {
  padding: 10px 16px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
  cursor: pointer;
  font-size: 14px;
  min-width: 140px;
}

.filter-date {
  padding: 10px 16px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
  font-size: 14px;
}

.date-separator {
  color: #6b7280;
  font-size: 14px;
}

.movements-table-card {
  background: white;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.movements-table {
  width: 100%;
  border-collapse: collapse;
}

.movements-table th {
  background: #f8f6f2;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
  padding: 16px 20px;
  text-align: left;
}

.movements-table td {
  padding: 16px 20px;
  border-bottom: 1px solid #f3f4f6;
}

.movements-table tr:hover td {
  background: #fafaf8;
}

.date-time {
  display: flex;
  flex-direction: column;
}

.date {
  font-weight: 500;
  color: #1b4332;
}

.time {
  font-size: 12px;
  color: #6b7280;
}

.product-info {
  display: flex;
  flex-direction: column;
}

.product-name {
  font-weight: 500;
  color: #1b4332;
}

.product-sku {
  font-size: 11px;
  color: #6b7280;
}

.positive {
  color: #2d6a4f;
  font-weight: 600;
}

.negative {
  color: #e07a5f;
  font-weight: 600;
}

.reason-text {
  font-size: 13px;
  color: #374151;
}

.notes-text {
  font-size: 11px;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 2px;
}

.detail-dialog {
  border-radius: 24px !important;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  color: #6b7280;
  font-weight: 500;
}

.detail-value {
  font-weight: 500;
  color: #1b4332;
}

/* Responsive */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .movements-container {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-title {
    font-size: 24px;
  }

  .header-actions {
    flex-direction: column;
  }

  .header-actions .v-btn {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .stat-value {
    font-size: 18px;
  }

  .filters-bar {
    flex-direction: column;
  }

  .search-wrapper {
    width: 100%;
  }

  .filter-group {
    width: 100%;
    flex-direction: column;
  }

  .filter-select,
  .filter-date {
    width: 100%;
    min-width: unset;
  }

  .movements-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }

  .movements-table th,
  .movements-table td {
    padding: 12px 16px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .dialog-actions {
    flex-direction: column;
  }

  .dialog-actions .v-btn {
    width: 100%;
  }

  .detail-row {
    flex-direction: column;
    gap: 4px;
  }
}
</style>
