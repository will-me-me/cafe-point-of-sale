<!-- pages/orders/index.vue -->
<template>
  <div class="orders-container">
    <!-- Page Header -->
    <v-row class="page-header" no-gutters>
      <v-col cols="12" md="8">
        <div class="page-badge">Transaction History</div>
        <h1 class="page-title">Orders</h1>
        <p class="page-subtitle">View and manage all customer orders</p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right mt-4 mt-md-0">
        <v-btn variant="outlined" class="export-btn" @click="exportOrders">
          <v-icon start>mdi-export</v-icon>
          Export
        </v-btn>
        <v-btn
          v-if="hasDebtOrders"
          color="#E07A5F"
          class="debt-btn ml-2"
          @click="showDebtManagement = true"
        >
          <v-icon start>mdi-account-cash</v-icon>
          Manage Debts ({{ debtCount }})
        </v-btn>
      </v-col>
    </v-row>

    <!-- Debt Overview Section -->
    <v-row v-if="hasDebtOrders" no-gutters>
      <v-col cols="12">
        <v-card class="debt-overview-card mb-4" elevation="0" rounded="xl">
          <v-card-text class="pa-4">
            <v-row align="center" no-gutters>
              <v-col cols="12" md="6">
                <div class="debt-overview-header">
                  <v-icon color="#E07A5F" size="24">mdi-account-cash</v-icon>
                  <span class="debt-title">Debt Overview</span>
                  <v-chip size="small" color="#E07A5F" text-color="white">
                    {{ debtCount }} Pending
                  </v-chip>
                </div>
              </v-col>
              <v-col cols="12" md="6" class="text-md-right mt-2 mt-md-0">
                <span class="total-debt-label">Total Outstanding</span>
                <span class="total-debt-amount">KSh {{ totalDebt }}</span>
              </v-col>
            </v-row>

            <v-row class="debt-stats-grid mt-2" no-gutters>
              <v-col cols="12" sm="4" class="pa-1">
                <v-card class="debt-stat-card" elevation="0" rounded="lg">
                  <v-card-text class="pa-3">
                    <v-row align="center" no-gutters>
                      <v-col cols="auto">
                        <div class="stat-icon" style="background: #e07a5f20">
                          <v-icon color="#E07A5F" size="20"
                            >mdi-account-group</v-icon
                          >
                        </div>
                      </v-col>
                      <v-col class="pl-3">
                        <div class="stat-value">
                          {{ debtOverview.total_customers || 0 }}
                        </div>
                        <div class="stat-label">Customers with Debt</div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" sm="4" class="pa-1">
                <v-card class="debt-stat-card" elevation="0" rounded="lg">
                  <v-card-text class="pa-3">
                    <v-row align="center" no-gutters>
                      <v-col cols="auto">
                        <div class="stat-icon" style="background: #2d6a4f20">
                          <v-icon color="#2D6A4F" size="20"
                            >mdi-clock-outline</v-icon
                          >
                        </div>
                      </v-col>
                      <v-col class="pl-3">
                        <div class="stat-value">
                          {{ debtOverview.average_age || 0 }} days
                        </div>
                        <div class="stat-label">Average Age</div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" sm="4" class="pa-1">
                <v-card class="debt-stat-card" elevation="0" rounded="lg">
                  <v-card-text class="pa-3">
                    <v-row align="center" no-gutters>
                      <v-col cols="auto">
                        <div class="stat-icon" style="background: #f4a26120">
                          <v-icon color="#F4A261" size="20"
                            >mdi-chart-pie</v-icon
                          >
                        </div>
                      </v-col>
                      <v-col class="pl-3">
                        <div class="stat-value">{{ debtCount }}</div>
                        <div class="stat-label">Total Debt Orders</div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Debt Aging Breakdown -->
            <v-card class="debt-aging-card mt-3" elevation="0" rounded="lg">
              <v-card-text class="pa-3">
                <div class="aging-header mb-2">
                  <span class="aging-title">Aging Breakdown</span>
                </div>
                <div class="aging-bars">
                  <div
                    v-for="(item, key) in agingData"
                    :key="key"
                    class="aging-item"
                  >
                    <span class="aging-label">{{ item.label }}</span>
                    <div class="aging-bar">
                      <div
                        class="aging-fill"
                        :style="{
                          width: getAgingPercentage(key) + '%',
                          background: item.color,
                        }"
                      ></div>
                    </div>
                    <span class="aging-amount"
                      >KSh {{ getAgingAmount(key) }}</span
                    >
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Filters Section -->
    <v-card class="filters-card mb-4" elevation="0" rounded="xl">
      <v-card-text class="pa-4">
        <v-row no-gutters>
          <v-col cols="12" md="5" class="pr-md-4">
            <div class="search-wrapper">
              <v-icon class="search-icon">mdi-magnify</v-icon>
              <input
                v-model="searchQuery"
                placeholder="Search by receipt number or customer..."
                class="search-input"
              />
            </div>
          </v-col>
          <v-col cols="12" md="7">
            <v-row no-gutters class="filter-group">
              <v-col cols="6" sm="3" class="pr-1">
                <select v-model="selectedType" class="filter-select">
                  <option value="">All Types</option>
                  <option value="dine-in">🍽️ Dine In</option>
                  <option value="takeaway">📦 Take Away</option>
                  <option value="delivery">🚚 Delivery</option>
                </select>
              </v-col>
              <v-col cols="6" sm="3" class="px-1">
                <select v-model="selectedPaymentMode" class="filter-select">
                  <option value="">All Payment</option>
                  <option value="cash">💵 Cash</option>
                  <option value="mpesa">📱 M-Pesa</option>
                  <option value="debt">📋 Debt</option>
                </select>
              </v-col>
              <v-col cols="6" sm="3" class="px-1">
                <select v-model="selectedStatus" class="filter-select">
                  <option value="">All Status</option>
                  <option value="paid">✅ Paid</option>
                  <option value="pending">⏳ Pending</option>
                  <option value="overdue">⚠️ Overdue</option>
                </select>
              </v-col>
              <v-col cols="6" sm="3" class="pl-1">
                <input type="date" v-model="dateFilter" class="date-picker" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Stats Summary -->
    <v-row class="stats-summary" no-gutters>
      <v-col cols="12" sm="6" lg="3" class="pa-1">
        <v-card class="summary-card" elevation="0" rounded="lg">
          <v-card-text class="pa-3">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div class="summary-icon" style="background: #2d6a4f20">
                  <v-icon color="#2D6A4F">mdi-cart-outline</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="summary-value">{{ filteredOrders.length }}</div>
                <div class="summary-label">Total Orders</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3" class="pa-1">
        <v-card class="summary-card" elevation="0" rounded="lg">
          <v-card-text class="pa-3">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div class="summary-icon" style="background: #e07a5f20">
                  <v-icon color="#E07A5F">mdi-currency-usd</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="summary-value">KSh {{ totalRevenue }}</div>
                <div class="summary-label">Total Revenue</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3" class="pa-1">
        <v-card class="summary-card" elevation="0" rounded="lg">
          <v-card-text class="pa-3">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div class="summary-icon" style="background: #f4a26120">
                  <v-icon color="#F4A261">mdi-chart-line</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="summary-value">KSh {{ avgOrderValue }}</div>
                <div class="summary-label">Average Order</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3" class="pa-1">
        <v-card class="summary-card debt-summary" elevation="0" rounded="lg">
          <v-card-text class="pa-3">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <div class="summary-icon" style="background: #e07a5f30">
                  <v-icon color="#E07A5F">mdi-account-cash</v-icon>
                </div>
              </v-col>
              <v-col class="pl-3">
                <div class="summary-value">KSh {{ totalDebt }}</div>
                <div class="summary-label">Total Outstanding Debt</div>
                <div class="summary-sub">{{ debtCount }} debt orders</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Orders Table -->
    <v-card class="orders-table-card" elevation="0" rounded="xl">
      <v-data-table
        :headers="headers"
        :items="paginatedOrders"
        :loading="loading"
        :items-per-page="itemsPerPage"
        :page="currentPage"
        @update:page="currentPage = $event"
        @update:items-per-page="itemsPerPage = $event"
        class="orders-table"
        item-value="id"
        :items-length="filteredOrders.length"
      >
        <template v-slot:item.receiptNumber="{ item }">
          <span class="receipt-cell">{{ item.receiptNumber }}</span>
        </template>

        <template v-slot:item.customer_name="{ item }">
          <div class="customer-cell">
            <div class="customer-name">{{ item.customer_name || "Guest" }}</div>
            <div v-if="item.customer_phone" class="customer-phone">
              {{ item.customer_phone }}
            </div>
          </div>
        </template>

        <template v-slot:item.order_type="{ item }">
          <v-chip
            :color="getOrderTypeColor(item.order_type)"
            size="small"
            text-color="white"
          >
            {{ formatOrderType(item.order_type) }}
          </v-chip>
        </template>

        <template v-slot:item.items="{ item }">
          <span>{{ item.items?.length || 0 }} items</span>
        </template>

        <template v-slot:item.total="{ item }">
          <span class="amount-cell"
            >KSh {{ (item.total || 0).toFixed(2) }}</span
          >
        </template>

        <template v-slot:item.created_at="{ item }">
          <div class="date-cell">
            <div>{{ formatDate(item.created_at) }}</div>
            <div class="date-time">{{ formatTime(item.created_at) }}</div>
          </div>
        </template>

        <template v-slot:item.payment_mode="{ item }">
          <v-chip
            :color="getPaymentColor(item.payment_mode)"
            size="small"
            text-color="white"
          >
            <v-icon start size="14">{{
              getPaymentIcon(item.payment_mode)
            }}</v-icon>
            {{ formatPaymentMode(item.payment_mode) }}
          </v-chip>
        </template>

        <template v-slot:item.payment_status="{ item }">
          <v-chip
            :color="getStatusColor(item.payment_status)"
            size="small"
            text-color="white"
          >
            {{ formatStatus(item.payment_status) }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            size="small"
            variant="text"
            @click="viewOrderDetails(item)"
          >
            <v-icon size="18">mdi-eye</v-icon>
          </v-btn>
          <v-btn icon size="small" variant="text" @click="printReceipt(item)">
            <v-icon size="18">mdi-printer</v-icon>
          </v-btn>
          <v-btn
            v-if="
              item.payment_mode === 'debt' && item.payment_status === 'pending'
            "
            icon
            size="small"
            variant="text"
            color="#2D6A4F"
            @click="markDebtAsPaid(item)"
          >
            <v-icon size="18">mdi-check-circle</v-icon>
          </v-btn>
        </template>

        <template v-slot:bottom>
          <div class="pagination-section">
            <div class="items-per-page">
              <span>Show</span>
              <select v-model="itemsPerPage" class="items-per-page-select">
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
              <span>entries</span>
            </div>
            <div class="pagination-info">
              Showing {{ (currentPage - 1) * itemsPerPage + 1 }} -
              {{ Math.min(currentPage * itemsPerPage, filteredOrders.length) }}
              of {{ filteredOrders.length }}
            </div>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Order Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="800">
      <v-card
        class="order-details-dialog"
        :class="{ 'debt-dialog': selectedOrder?.payment_mode === 'debt' }"
      >
        <v-card-title class="dialog-header">
          <div>
            <div class="receipt-badge">Order Details</div>
            <h2>{{ selectedOrder?.receipt_number || "N/A" }}</h2>
          </div>
          <v-btn icon variant="text" @click="detailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <!-- Order Info Grid -->
          <v-row class="order-info-grid" no-gutters>
            <v-col cols="12" sm="6" class="pa-1">
              <v-card class="info-card" elevation="0" rounded="lg">
                <v-card-text>
                  <div class="info-label">Customer Name</div>
                  <div class="info-value">
                    {{ selectedOrder?.customer_name || "Guest" }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" class="pa-1">
              <v-card class="info-card" elevation="0" rounded="lg">
                <v-card-text>
                  <div class="info-label">Order Type</div>
                  <div class="info-value">
                    {{ formatOrderType(selectedOrder?.order_type) }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" class="pa-1">
              <v-card class="info-card" elevation="0" rounded="lg">
                <v-card-text>
                  <div class="info-label">Table/Number</div>
                  <div class="info-value">
                    {{ selectedOrder?.table_number || "N/A" }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" class="pa-1">
              <v-card class="info-card" elevation="0" rounded="lg">
                <v-card-text>
                  <div class="info-label">Date & Time</div>
                  <div class="info-value">
                    {{ formatFullDate(selectedOrder?.created_at) }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" class="pa-1">
              <v-card class="info-card" elevation="0" rounded="lg">
                <v-card-text>
                  <div class="info-label">Payment Method</div>
                  <div class="info-value">
                    <v-chip
                      :color="getPaymentColor(selectedOrder?.payment_mode)"
                      size="small"
                      text-color="white"
                    >
                      <v-icon start size="14">{{
                        getPaymentIcon(selectedOrder?.payment_mode)
                      }}</v-icon>
                      {{ formatPaymentMode(selectedOrder?.payment_mode) }}
                    </v-chip>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" class="pa-1">
              <v-card class="info-card" elevation="0" rounded="lg">
                <v-card-text>
                  <div class="info-label">Payment Status</div>
                  <div class="info-value">
                    <v-chip
                      :color="getStatusColor(selectedOrder?.payment_status)"
                      size="small"
                      text-color="white"
                    >
                      {{ formatStatus(selectedOrder?.payment_status) }}
                    </v-chip>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Debt Notice -->
          <v-card
            v-if="
              selectedOrder?.payment_mode === 'debt' &&
              selectedOrder?.payment_status === 'pending'
            "
            class="debt-notice mt-2"
            color="#FFF3E0"
            rounded="lg"
          >
            <v-card-text>
              <v-row align="center" no-gutters>
                <v-col cols="auto">
                  <v-icon size="32" color="#E07A5F">mdi-alert-circle</v-icon>
                </v-col>
                <v-col class="pl-3">
                  <div class="font-weight-bold">Debt Order</div>
                  <p class="mb-1">
                    This order is recorded as debt. Please collect payment from
                    the customer.
                  </p>
                  <v-btn
                    size="small"
                    color="#2D6A4F"
                    @click="markDebtAsPaid(selectedOrder)"
                  >
                    <v-icon start size="16">mdi-check</v-icon>
                    Mark as Paid
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Items List -->
          <div class="items-list mt-4">
            <h3>Order Items</h3>
            <v-list>
              <v-list-item
                v-for="(item, index) in selectedOrder?.items"
                :key="index"
                class="order-item-detail"
              >
                <template #prepend>
                  <v-icon color="#2D6A4F">mdi-food</v-icon>
                </template>
                <v-list-item-title class="item-detail-name">
                  {{ item.name || item.product_name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  <span class="item-unit-price"
                    >KSh
                    {{ (item.unit_price || item.price || 0).toFixed(2) }}</span
                  >
                  × {{ item.quantity || 1 }}
                </v-list-item-subtitle>
                <template #append>
                  <span class="item-detail-price">
                    KSh
                    {{
                      (
                        (item.unit_price || item.price || 0) *
                        (item.quantity || 1)
                      ).toFixed(2)
                    }}
                  </span>
                </template>
              </v-list-item>
            </v-list>
          </div>

          <!-- Order Summary -->
          <v-card class="order-summary mt-4" elevation="0" rounded="lg">
            <v-card-text>
              <v-row>
                <v-col cols="6" class="text-left font-weight-medium"
                  >Subtotal</v-col
                >
                <v-col cols="6" class="text-right"
                  >KSh {{ (selectedOrder?.subtotal || 0).toFixed(2) }}</v-col
                >
                <v-col cols="6" class="text-left font-weight-medium">Tax</v-col>
                <v-col cols="6" class="text-right"
                  >KSh {{ (selectedOrder?.tax || 0).toFixed(2) }}</v-col
                >
                <v-col cols="12" class="pa-0">
                  <v-divider class="my-2"></v-divider>
                </v-col>
                <v-col cols="6" class="text-left font-weight-bold text-h6"
                  >Total</v-col
                >
                <v-col
                  cols="6"
                  class="text-right font-weight-bold text-h6 text-error"
                >
                  KSh {{ (selectedOrder?.total || 0).toFixed(2) }}
                </v-col>
                <v-col
                  v-if="selectedOrder?.payment_mode === 'debt'"
                  cols="12"
                  class="pa-0"
                >
                  <v-divider class="my-2"></v-divider>
                </v-col>
                <v-col
                  v-if="selectedOrder?.payment_mode === 'debt'"
                  cols="6"
                  class="text-left font-weight-medium"
                >
                  Debt Status
                </v-col>
                <v-col
                  v-if="selectedOrder?.payment_mode === 'debt'"
                  cols="6"
                  class="text-right"
                >
                  <v-chip
                    :color="getStatusColor(selectedOrder?.payment_status)"
                    size="small"
                    text-color="white"
                  >
                    {{ formatStatus(selectedOrder?.payment_status) }}
                  </v-chip>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="outlined" @click="printReceipt(selectedOrder)">
            <v-icon start>mdi-printer</v-icon>
            Print Receipt
          </v-btn>
          <v-btn
            v-if="
              selectedOrder?.payment_mode === 'debt' &&
              selectedOrder?.payment_status === 'pending'
            "
            color="#2D6A4F"
            @click="markDebtAsPaid(selectedOrder)"
          >
            <v-icon start>mdi-check</v-icon>
            Mark as Paid
          </v-btn>
          <v-btn color="#2D6A4F" @click="detailsDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Debt Management Dialog -->
    <v-dialog v-model="showDebtManagement" max-width="900" scrollable>
      <v-card class="debt-management-dialog">
        <v-card-title class="dialog-header">
          <div class="title-content">
            <v-icon size="28" color="#E07A5F" class="mr-3"
              >mdi-account-cash</v-icon
            >
            <span>Debt Management</span>
            <v-chip
              size="small"
              color="#E07A5F"
              text-color="white"
              class="ml-3"
            >
              {{ debtCount }} Pending
            </v-chip>
          </div>
          <v-btn icon variant="text" @click="showDebtManagement = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="dialog-content">
          <!-- Debt Summary Cards -->
          <v-row class="debt-summary-cards" no-gutters>
            <v-col cols="12" sm="4" class="pa-1">
              <v-card class="debt-stat-card" elevation="0" rounded="lg">
                <v-card-text class="pa-3">
                  <v-row align="center" no-gutters>
                    <v-col cols="auto">
                      <div class="stat-icon" style="background: #e07a5f20">
                        <v-icon color="#E07A5F" size="24">mdi-cash</v-icon>
                      </div>
                    </v-col>
                    <v-col class="pl-3">
                      <div class="stat-value">
                        KSh {{ (debtOverview.total_debt || 0).toFixed(2) }}
                      </div>
                      <div class="stat-label">Total Outstanding</div>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="4" class="pa-1">
              <v-card class="debt-stat-card" elevation="0" rounded="lg">
                <v-card-text class="pa-3">
                  <v-row align="center" no-gutters>
                    <v-col cols="auto">
                      <div class="stat-icon" style="background: #2d6a4f20">
                        <v-icon color="#2D6A4F" size="24"
                          >mdi-account-group</v-icon
                        >
                      </div>
                    </v-col>
                    <v-col class="pl-3">
                      <div class="stat-value">
                        {{ debtOverview.total_customers || 0 }}
                      </div>
                      <div class="stat-label">Customers with Debt</div>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="4" class="pa-1">
              <v-card class="debt-stat-card" elevation="0" rounded="lg">
                <v-card-text class="pa-3">
                  <v-row align="center" no-gutters>
                    <v-col cols="auto">
                      <div class="stat-icon" style="background: #f4a26120">
                        <v-icon color="#F4A261" size="24"
                          >mdi-clock-outline</v-icon
                        >
                      </div>
                    </v-col>
                    <v-col class="pl-3">
                      <div class="stat-value">
                        {{ debtOverview.average_age || 0 }} days
                      </div>
                      <div class="stat-label">Average Age</div>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Aging Breakdown -->
          <v-card class="debt-aging-card mt-2" elevation="0" rounded="lg">
            <v-card-text class="pa-3">
              <div class="aging-header mb-2">
                <span class="aging-title">📊 Aging Breakdown</span>
              </div>
              <div class="aging-bars">
                <div
                  v-for="(item, key) in agingData"
                  :key="key"
                  class="aging-item"
                >
                  <span class="aging-label">{{ item.label }}</span>
                  <div class="aging-bar">
                    <div
                      class="aging-fill"
                      :style="{
                        width: getAgingPercentage(key) + '%',
                        background: item.color,
                      }"
                    ></div>
                  </div>
                  <span class="aging-amount"
                    >KSh {{ getAgingAmount(key) }}</span
                  >
                </div>
              </div>
            </v-card-text>
          </v-card>

          <!-- Debt List -->
          <div class="debt-list-section mt-4">
            <div class="list-header">
              <span class="list-title">📋 All Pending Debts </span>
              <span class="list-count">
                {{ debtOverview.debts?.length || 0 }} orders</span
              >
            </div>
            <div class="debt-list">
              <v-card
                v-for="debt in debtOverview.debts"
                :key="debt.id"
                class="debt-list-item"
                :class="{ overdue: debt.age_days > 7 }"
                elevation="0"
                rounded="lg"
              >
                <v-card-text class="pa-3">
                  <v-row align="center" no-gutters>
                    <v-col cols="12" sm="4">
                      <div class="debt-item-customer">
                        {{ debt.customerName || "Guest" }}
                      </div>
                      <div class="debt-item-receipt">
                        {{ debt.receiptNumber }}
                      </div>
                    </v-col>
                    <v-col cols="6" sm="3" class="text-left text-sm-center">
                      <div class="debt-item-date">
                        {{ formatDate(debt.created_at) }}
                      </div>
                    </v-col>
                    <v-col cols="6" sm="2" class="text-right text-sm-center">
                      <div class="debt-item-amount">
                        KSh {{ (debt.total || 0).toFixed(2) }}
                      </div>
                    </v-col>
                    <v-col cols="6" sm="2" class="text-left text-sm-center">
                      <div class="debt-item-age">
                        <span :class="{ 'overdue-text': debt.age_days > 7 }">
                          {{ debt.age_days || 0 }} days
                        </span>
                        <v-chip
                          v-if="debt.age_days > 7"
                          size="x-small"
                          color="#EF4444"
                          text-color="white"
                        >
                          Overdue
                        </v-chip>
                      </div>
                    </v-col>
                    <v-col cols="6" sm="1" class="text-right">
                      <v-btn
                        size="small"
                        color="#2D6A4F"
                        @click="markDebtAsPaid(debt)"
                      >
                        <v-icon start size="16">mdi-check</v-icon>
                        Pay
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              <div v-if="!debtOverview.debts?.length" class="no-debts">
                <v-icon size="48" color="#E5E7EB">mdi-check-circle</v-icon>
                <p>No outstanding debts! 🎉</p>
                <span class="no-debts-sub"
                  >All debt orders have been cleared.</span
                >
              </div>
            </div>
          </div>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="showDebtManagement = false"
            >Close</v-btn
          >
          <v-btn color="#E07A5F" variant="outlined" @click="refreshDebtData">
            <v-icon start>mdi-refresh</v-icon>
            Refresh
          </v-btn>
          <v-btn color="#2D6A4F" @click="exportDebtReport">
            <v-icon start>mdi-export</v-icon>
            Export Debt Report
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Mark Debt as Paid Confirmation Dialog -->
    <v-dialog v-model="showPaidConfirmation" max-width="400">
      <v-card class="confirm-dialog text-center pa-6">
        <v-icon size="64" color="#2D6A4F">mdi-check-circle</v-icon>
        <h3 class="mt-4">Mark Debt as Paid?</h3>
        <p class="mt-2 text-medium-emphasis">
          Confirm that
          <strong>{{ selectedOrder?.customer_name || "Guest" }}</strong> has
          paid
          <strong>KSh {{ (selectedOrder?.total || 0).toFixed(2) }}</strong> for
          order
          <strong>{{ selectedOrder?.receiptNumber }}</strong>
        </p>
        <v-btn variant="text" @click="showPaidConfirmation = false" class="mr-2"
          >Cancel</v-btn
        >
        <v-btn color="#2D6A4F" @click="confirmMarkAsPaid"
          >Confirm Payment</v-btn
        >
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :timeout="3000"
      :color="snackbar.color"
      location="top"
      class="custom-snackbar"
    >
      <v-icon start>{{ snackbar.icon }}</v-icon>
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" icon="mdi-close" @click="snackbar.show = false" />
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { usePosStore } from "~/stores/pos";
import { useReceipt } from "~/composables/useReceipt";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const store = usePosStore();
const receipt = useReceipt();

// State
const loading = ref(false);
const searchQuery = ref("");
const selectedType = ref("");
const selectedPaymentMode = ref("");
const selectedStatus = ref("");
const dateFilter = ref("");
const itemsPerPage = ref(10);
const currentPage = ref(1);
const detailsDialog = ref(false);
const showDebtManagement = ref(false);
const showPaidConfirmation = ref(false);
const selectedOrder = ref(null);

const debtOverview = ref({
  total_debt: 0,
  total_customers: 0,
  average_age: 0,
  by_age: {
    "0-7_days": 0,
    "8-14_days": 0,
    "15-30_days": 0,
    "30+_days": 0,
  },
  debts: [],
});

const snackbar = ref({
  show: false,
  text: "",
  color: "success",
  icon: "mdi-check-circle",
});

// Table Headers
const headers = [
  { title: "Receipt #", key: "receipt_number", sortable: true },
  { title: "Customer", key: "customer_name", sortable: true },
  { title: "Order Type", key: "order_type", sortable: true },
  { title: "Items", key: "items", sortable: true },
  { title: "Total", key: "total", sortable: true },
  { title: "Date", key: "created_at", sortable: true },
  { title: "Payment", key: "payment_mode", sortable: true },
  { title: "Status", key: "payment_status", sortable: true },
  { title: "Actions", key: "actions", sortable: false },
];

// Computed
const orders = computed(() => store.AllOrders || []);

const debtOrders = computed(() => {
  return orders.value.filter(
    (order) =>
      order.payment_mode === "debt" && order.payment_status === "pending"
  );
});

const hasDebtOrders = computed(() => debtOrders.value.length > 0);
const debtCount = computed(() => debtOrders.value.length);

const totalDebt = computed(() => {
  return debtOrders.value
    .reduce((sum, order) => sum + (order.total || 0), 0)
    .toFixed(2);
});

const filteredOrders = computed(() => {
  let filtered = [...orders.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (order) =>
        order.receiptNumber?.toLowerCase().includes(query) ||
        order.customer_name?.toLowerCase().includes(query) ||
        order.customer_phone?.includes(query)
    );
  }

  if (selectedType.value) {
    filtered = filtered.filter(
      (order) => order.order_type === selectedType.value
    );
  }

  if (selectedPaymentMode.value) {
    filtered = filtered.filter(
      (order) => order.payment_mode === selectedPaymentMode.value
    );
  }

  if (selectedStatus.value) {
    filtered = filtered.filter(
      (order) => order.payment_status === selectedStatus.value
    );
  }

  if (dateFilter.value) {
    filtered = filtered.filter((order) => {
      const orderDate = new Date(order.created_at).toISOString().split("T")[0];
      return orderDate === dateFilter.value;
    });
  }

  return filtered;
});

const totalRevenue = computed(() => {
  return filteredOrders.value
    .filter(
      (order) =>
        order.payment_status === "paid" || order.payment_status === "completed"
    )
    .reduce((sum, order) => sum + (order.total || 0), 0)
    .toFixed(2);
});

const avgOrderValue = computed(() => {
  const completedOrders = filteredOrders.value.filter(
    (order) =>
      order.payment_status === "paid" || order.payment_status === "completed"
  );
  if (completedOrders.length === 0) return "0.00";
  return (parseFloat(totalRevenue.value) / completedOrders.length).toFixed(2);
});

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredOrders.value.slice(start, end);
});

// Aging Data
const agingData = {
  "0-7_days": { label: "0-7 Days", color: "#2D6A4F" },
  "8-14_days": { label: "8-14 Days", color: "#F4A261" },
  "15-30_days": { label: "15-30 Days", color: "#E07A5F" },
  "30+_days": { label: "30+ Days", color: "#EF4444" },
};

// Helper Methods
const formatDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const formatTime = (date: string) => {
  if (!date) return "";
  return new Date(date).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatFullDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
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
    partial: "Partial",
    refunded: "Refunded",
  };
  return statuses[status] || status || "N/A";
};

const getPaymentIcon = (mode: string) => {
  const icons: Record<string, string> = {
    cash: "mdi-cash",
    mpesa: "mdi-cellphone",
    debt: "mdi-account-cash",
    card: "mdi-credit-card",
  };
  return icons[mode] || "mdi-help-circle";
};

const getOrderTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    "dine-in": "#2D6A4F",
    takeaway: "#F4A261",
    delivery: "#4A90D9",
    "order-online": "#6B4E71",
  };
  return colors[type] || "#6B7280";
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
    partial: "#F4A261",
    refunded: "#6B7280",
  };
  return colors[status] || "#6B7280";
};

const getAgingPercentage = (key: string) => {
  const total = debtOverview.value.total_debt || 0;
  const value =
    debtOverview.value.by_age?.[
      key as keyof typeof debtOverview.value.by_age
    ] || 0;
  return total > 0 ? (value / total) * 100 : 0;
};

const getAgingAmount = (key: string) => {
  return (
    debtOverview.value.by_age?.[
      key as keyof typeof debtOverview.value.by_age
    ] || 0
  ).toFixed(2);
};

// Actions
const viewOrderDetails = (order: any) => {
  selectedOrder.value = order;
  detailsDialog.value = true;
};

const printReceipt = (order: any) => {
  if (order) {
    receipt.printReceipt(order);
  }
};

const markDebtAsPaid = (order: any) => {
  selectedOrder.value = order;
  showPaidConfirmation.value = true;
};

const confirmMarkAsPaid = async () => {
  if (!selectedOrder.value) return;

  try {
    const orderId = selectedOrder.value._id ?? selectedOrder.value.id;
    await store.updateDebtOrderStatus(orderId);
    await fetchDebtOverview();
    await store.getAllOrders();

    // Update local state
    const orderIndex = store.AllOrders.findIndex(
      (o) => o._id === selectedOrder.value._id
    );
    if (orderIndex !== -1) {
      store.AllOrders[orderIndex].payment_status = "paid";
    }

    showPaidConfirmation.value = false;
    detailsDialog.value = false;
    showDebtManagement.value = false;

    snackbar.value = {
      show: true,
      text: `Debt of KSh ${(selectedOrder.value.total || 0).toFixed(2)} from ${
        selectedOrder.value.customer_name || "Guest"
      } marked as paid!`,
      color: "success",
      icon: "mdi-check-circle",
    };

    selectedOrder.value = null;
  } catch (error) {
    console.error("Error marking debt as paid:", error);
    snackbar.value = {
      show: true,
      text: "Failed to mark debt as paid. Please try again.",
      color: "error",
      icon: "mdi-alert-circle",
    };
  }
};

const fetchDebtOverview = async () => {
  try {
    const response = await store.getDebtOverview();
    debtOverview.value = response;
  } catch (error) {
    console.error("Error fetching debt overview:", error);
  }
};

const refreshDebtData = () => {
  fetchDebtOverview();
};

const exportOrders = () => {
  // Export orders as CSV
  const headers = [
    "Receipt #",
    "Customer",
    "Phone",
    "Order Type",
    "Items",
    "Total",
    "Payment Method",
    "Status",
    "Date",
  ];

  const rows = filteredOrders.value.map((order) => [
    order.receiptNumber || "",
    order.customer_name || "Guest",
    order.customer_phone || "",
    formatOrderType(order.order_type),
    order.items?.length || 0,
    (order.total || 0).toFixed(2),
    formatPaymentMode(order.payment_mode),
    formatStatus(order.payment_status),
    formatFullDate(order.created_at),
  ]);

  let csv = headers.join(",") + "\n";
  rows.forEach((row) => {
    csv += row.map((item) => `"${item}"`).join(",") + "\n";
  });

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `orders_${new Date().toISOString().split("T")[0]}.csv`;
  link.click();
  URL.revokeObjectURL(url);
};

const exportDebtReport = () => {
  const headers = [
    "Customer",
    "Receipt #",
    "Amount",
    "Date",
    "Age (days)",
    "Status",
  ];

  const rows = (debtOverview.value.debts || []).map((debt: any) => [
    debt.customerName || "Guest",
    debt.receiptNumber || "",
    (debt.total || 0).toFixed(2),
    formatDate(debt.created_at),
    debt.age_days || 0,
    debt.age_days > 7 ? "Overdue" : "Current",
  ]);

  let csv = headers.join(",") + "\n";
  rows.forEach((row) => {
    csv += row.map((item) => `"${item}"`).join(",") + "\n";
  });

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `debt_report_${new Date().toISOString().split("T")[0]}.csv`;
  link.click();
  URL.revokeObjectURL(url);
};

// Lifecycle
onMounted(async () => {
  loading.value = true;
  try {
    await store.getAllOrders();
    await fetchDebtOverview();
  } catch (error) {
    console.error("Error loading orders:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.orders-container {
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
  color: #e07a5f;
  text-transform: uppercase;
  letter-spacing: 2px;
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
}

.export-btn {
  border-color: #e5e7eb;
  border-radius: 40px;
}

.debt-btn {
  text-transform: none;
  border-radius: 40px;
  background: #fff3e0;
  color: #e07a5f;
}

.debt-btn:hover {
  background: #ffe8cc;
}

/* Debt Overview */
.debt-overview-card {
  background: white;
  border: 1px solid #e07a5f20;
}

.debt-overview-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.debt-title {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.total-debt-label {
  font-size: 13px;
  color: #6b7280;
  margin-right: 8px;
}

.total-debt-amount {
  font-size: 24px;
  font-weight: 800;
  color: #e07a5f;
}

.debt-stat-card {
  background: #f8f6f2;
}

.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.stat-label {
  font-size: 11px;
  color: #6b7280;
}

/* Aging */
.debt-aging-card {
  background: #f8f6f2;
}

.aging-title {
  font-weight: 600;
  color: #1b4332;
  font-size: 14px;
}

.aging-bars {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.aging-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.aging-label {
  font-size: 12px;
  color: #6b7280;
  min-width: 60px;
}

.aging-bar {
  flex: 1;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.aging-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.aging-amount {
  font-size: 12px;
  font-weight: 600;
  color: #1b4332;
  min-width: 80px;
  text-align: right;
}

/* Filters */
.filters-card {
  background: white;
}

.search-wrapper {
  display: flex;
  align-items: center;
  background: #f8f6f2;
  border-radius: 40px;
  padding: 0 16px;
  gap: 12px;
  height: 44px;
}

.search-input {
  flex: 1;
  border: none;
  padding: 12px 0;
  background: transparent;
  outline: none;
  font-size: 14px;
}

.search-icon {
  color: #9ca3af;
}

.filter-group {
  display: flex;
  gap: 8px;
  height: 44px;
}

.filter-select,
.date-picker {
  padding: 8px 12px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
  width: 100%;
  height: 44px;
  font-size: 13px;
}

/* Stats */
.stats-summary {
  margin-bottom: 16px;
}

.summary-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.summary-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.summary-value {
  font-size: 20px;
  font-weight: 800;
  color: #1b4332;
}

.summary-label {
  font-size: 12px;
  color: #6b7280;
}

.summary-sub {
  font-size: 10px;
  color: #6b7280;
  margin-top: 2px;
}

.debt-summary {
  border-color: #e07a5f30;
}

/* Table */
.orders-table-card {
  background: white;
  border: 1px solid #f3f4f6;
}

.orders-table :deep(.v-data-table__th) {
  background: #f8f6f2;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

.receipt-cell {
  font-weight: 600;
  color: #1b4332;
  font-family: monospace;
}

.amount-cell {
  font-weight: 600;
  color: #e07a5f;
}

.customer-cell .customer-name {
  font-weight: 500;
}

.customer-cell .customer-phone {
  font-size: 11px;
  color: #6b7280;
}

.date-cell .date-time {
  font-size: 11px;
  color: #6b7280;
}

.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-top: 1px solid #f3f4f6;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #6b7280;
}

.items-per-page-select {
  padding: 4px 8px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: white;
}

.pagination-info {
  font-size: 13px;
  color: #6b7280;
}

/* Dialogs */
.order-details-dialog {
  border-radius: 24px !important;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f3f4f6;
}

.receipt-badge {
  font-size: 11px;
  font-weight: 600;
  color: #e07a5f;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.dialog-header h2 {
  font-family: "Playfair Display", serif;
  font-size: 22px;
  font-weight: 700;
  color: #1b4332;
  margin: 0;
}

.info-card {
  background: #f8f6f2;
}

.info-label {
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-weight: 600;
  color: #1b4332;
}

.debt-notice {
  border: 1px solid #e07a5f40;
}

.debt-notice p {
  margin: 4px 0;
  color: #6b7280;
  font-size: 14px;
}

.items-list h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 12px;
}

.order-item-detail {
  border-bottom: 1px solid #f3f4f6;
}

.item-unit-price {
  font-size: 12px;
  color: #6b7280;
}

.item-detail-price {
  font-weight: 600;
  color: #e07a5f;
}

.order-summary {
  background: #f8f6f2;
}

.debt-dialog {
  border: 2px solid #e07a5f;
}

/* Debt Management Dialog */
.debt-management-dialog {
  border-radius: 24px !important;
}

.dialog-content {
  padding: 16px 24px;
}

.debt-summary-cards {
  margin-bottom: 16px;
}

.debt-list-item {
  border-left: 3px solid #e07a5f;
  margin-bottom: 8px;
}

.debt-list-item.overdue {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.debt-item-customer {
  font-weight: 600;
  color: #1b4332;
}

.debt-item-receipt {
  font-size: 11px;
  color: #6b7280;
}

.debt-item-date {
  font-size: 12px;
  color: #6b7280;
}

.debt-item-amount {
  font-weight: 700;
  color: #e07a5f;
}

.debt-item-age span {
  font-size: 12px;
  color: #6b7280;
}

.debt-item-age span.overdue-text {
  color: #ef4444;
  font-weight: 600;
}

.no-debts {
  text-align: center;
  padding: 32px;
}

.no-debts p {
  margin-top: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #1b4332;
}

.no-debts-sub {
  font-size: 13px;
  color: #6b7280;
}

/* Confirm Dialog */
.confirm-dialog {
  border-radius: 24px !important;
}

.confirm-dialog p {
  color: #6b7280;
  line-height: 1.5;
}

.dialog-actions {
  padding: 16px 24px;
  border-top: 1px solid #f3f4f6;
  gap: 8px;
}

/* Responsive */
@media (max-width: 768px) {
  .orders-container {
    padding: 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .debt-overview-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-right {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .filter-group {
    flex-wrap: wrap;
    height: auto;
    gap: 4px;
  }

  .filter-select,
  .date-picker {
    height: 38px;
    font-size: 12px;
  }

  .search-wrapper {
    height: 38px;
    margin-bottom: 8px;
  }

  .stats-summary .v-col {
    padding: 2px !important;
  }

  .summary-value {
    font-size: 16px;
  }

  .summary-icon {
    width: 36px;
    height: 36px;
  }

  .summary-icon .v-icon {
    font-size: 18px !important;
  }

  .orders-table :deep(.v-data-table__th),
  .orders-table :deep(.v-data-table__td) {
    padding: 8px 12px !important;
    font-size: 12px;
  }

  .pagination-section {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }

  .order-info-grid .v-col {
    padding: 2px !important;
  }

  .debt-summary-cards .v-col {
    padding: 2px !important;
  }

  .debt-list-item .v-col {
    padding: 2px !important;
  }

  .dialog-actions {
    flex-wrap: wrap;
  }

  .dialog-actions .v-btn {
    flex: 1;
    min-width: 100px;
  }

  .aging-item {
    flex-wrap: wrap;
    gap: 4px;
  }

  .aging-label {
    min-width: 50px;
    font-size: 11px;
  }

  .aging-amount {
    min-width: 60px;
    font-size: 11px;
  }

  .debt-item-age {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .confirm-dialog {
    padding: 16px !important;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }

  .total-debt-amount {
    font-size: 18px;
  }

  .stat-value {
    font-size: 14px;
  }

  .summary-value {
    font-size: 14px;
  }

  .debt-stat-card .stat-value {
    font-size: 16px;
  }

  .debt-item-customer {
    font-size: 14px;
  }

  .debt-item-amount {
    font-size: 14px;
  }

  .orders-table :deep(.v-data-table__th),
  .orders-table :deep(.v-data-table__td) {
    padding: 6px 8px !important;
    font-size: 11px;
  }

  .dialog-header h2 {
    font-size: 18px;
  }

  .order-item-detail {
    flex-wrap: wrap;
  }
}
</style>
