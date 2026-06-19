<template>
  <div class="orders-container">
    <!-- Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">Transaction History</div>
        <h1 class="page-title">Orders</h1>
        <p class="page-subtitle">View and manage all customer orders</p>
      </div>
      <div class="header-actions">
        <v-btn variant="outlined" class="export-btn" @click="exportOrders">
          <v-icon start>mdi-export</v-icon>
          Export
        </v-btn>
        <v-btn
          v-if="hasDebtOrders"
          color="#E07A5F"
          class="debt-btn"
          @click="showDebtManagement = true"
        >
          <v-icon start>mdi-account-cash</v-icon>
          Manage Debts ({{ debtCount }})
        </v-btn>
      </div>
    </div>
    <div v-if="hasDebtOrders" class="debt-overview-section">
      <div class="debt-overview-header">
        <div class="header-left">
          <v-icon color="#E07A5F" size="24">mdi-account-cash</v-icon>
          <span class="debt-title">Debt Overview</span>
          <v-chip size="small" color="#E07A5F" text-color="white">
            {{ debtCount }} Pending
          </v-chip>
        </div>
        <div class="header-right">
          <span class="total-debt-label">Total Outstanding</span>
          <span class="total-debt-amount">ksh{{ totalDebt }}</span>
        </div>
      </div>

      <div class="debt-stats-grid">
        <div class="debt-stat-card">
          <div class="stat-icon" style="background: #e07a5f20">
            <v-icon color="#E07A5F" size="20">mdi-account-group</v-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">
              {{ debtOverview.total_customers || 0 }}
            </div>
            <div class="stat-label">Customers with Debt</div>
          </div>
        </div>
        <div class="debt-stat-card">
          <div class="stat-icon" style="background: #2d6a4f20">
            <v-icon color="#2D6A4F" size="20">mdi-clock-outline</v-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">
              {{ debtOverview.average_age || 0 }} days
            </div>
            <div class="stat-label">Average Age</div>
          </div>
        </div>
        <div class="debt-stat-card">
          <div class="stat-icon" style="background: #f4a26120">
            <v-icon color="#F4A261" size="20">mdi-chart-pie</v-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ debtCount }}</div>
            <div class="stat-label">Total Debt Orders</div>
          </div>
        </div>
      </div>

      <!-- Debt Aging Breakdown -->
      <div class="debt-aging-section">
        <div class="aging-header">
          <span class="aging-title">Aging Breakdown</span>
        </div>
        <div class="aging-bars">
          <div class="aging-item">
            <span class="aging-label">0-7 Days</span>
            <div class="aging-bar">
              <div
                class="aging-fill"
                :style="{
                  width: getAgingPercentage('0-7_days') + '%',
                  background: getAgingColor('0-7_days'),
                }"
              ></div>
            </div>
            <span class="aging-amount"
              >ksh{{ debtOverview.by_age?.["0-7_days"]?.toFixed(2) || 0 }}</span
            >
          </div>
          <div class="aging-item">
            <span class="aging-label">8-14 Days</span>
            <div class="aging-bar">
              <div
                class="aging-fill"
                :style="{
                  width: getAgingPercentage('8-14_days') + '%',
                  background: getAgingColor('8-14_days'),
                }"
              ></div>
            </div>
            <span class="aging-amount"
              >ksh{{
                debtOverview.by_age?.["8-14_days"]?.toFixed(2) || 0
              }}</span
            >
          </div>
          <div class="aging-item">
            <span class="aging-label">15-30 Days</span>
            <div class="aging-bar">
              <div
                class="aging-fill"
                :style="{
                  width: getAgingPercentage('15-30_days') + '%',
                  background: getAgingColor('15-30_days'),
                }"
              ></div>
            </div>
            <span class="aging-amount"
              >ksh{{
                debtOverview.by_age?.["15-30_days"]?.toFixed(2) || 0
              }}</span
            >
          </div>
          <div class="aging-item">
            <span class="aging-label">30+ Days</span>
            <div class="aging-bar">
              <div
                class="aging-fill"
                :style="{
                  width: getAgingPercentage('30+_days') + '%',
                  background: getAgingColor('30+_days'),
                }"
              ></div>
            </div>
            <span class="aging-amount"
              >ksh{{ debtOverview.by_age?.["30+_days"]?.toFixed(2) || 0 }}</span
            >
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <div class="search-wrapper">
        <v-icon class="search-icon">mdi-magnify</v-icon>
        <input
          v-model="searchQuery"
          placeholder="Search by receipt number or customer..."
          class="search-input"
        />
      </div>
      <div class="filter-group">
        <select v-model="selectedType" class="filter-select">
          <option value="">All Types</option>
          <option value="dine-in">🍽️ Dine In</option>
          <option value="take-away">📦 Take Away</option>
          <option value="order-online">📱 Online</option>
        </select>
        <select v-model="selectedPaymentMode" class="filter-select">
          <option value="">All Payment Methods</option>
          <option value="cash">💵 Cash</option>
          <option value="mpesa">📱 M-Pesa</option>
          <option value="debt">📋 Debt</option>
        </select>
        <select v-model="selectedStatus" class="filter-select">
          <option value="">All Status</option>
          <option value="completed">✅ Completed</option>
          <option value="preparing">🔄 Preparing</option>
          <option value="pending">⏳ Pending</option>
          <option value="cancelled">❌ Cancelled</option>
        </select>
        <input type="date" v-model="dateFilter" class="date-picker" />
      </div>
    </div>

    <!-- Stats Summary -->
    <div class="stats-summary">
      <div class="summary-card">
        <div class="summary-icon" style="background: #2d6a4f20">
          <v-icon color="#2D6A4F">mdi-cart-outline</v-icon>
        </div>
        <div class="summary-info">
          <div class="summary-value">{{ filteredOrders.length }}</div>
          <div class="summary-label">Total Orders</div>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon" style="background: #e07a5f20">
          <v-icon color="#E07A5F">mdi-currency-usd</v-icon>
        </div>
        <div class="summary-info">
          <div class="summary-value">ksh{{ totalRevenue }}</div>
          <div class="summary-label">Total Revenue</div>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon" style="background: #f4a26120">
          <v-icon color="#F4A261">mdi-chart-line</v-icon>
        </div>
        <div class="summary-info">
          <div class="summary-value">ksh{{ avgOrderValue }}</div>
          <div class="summary-label">Average Order</div>
        </div>
      </div>
      <div class="summary-card" style="background: #fff3e0">
        <div class="summary-icon" style="background: #e07a5f30">
          <v-icon color="#E07A5F">mdi-account-cash</v-icon>
        </div>
        <div class="summary-info">
          <div class="summary-value">ksh{{ totalDebt }}</div>
          <div class="summary-label">Total Outstanding Debt</div>
          <div class="summary-sub">{{ debtCount }} debt orders</div>
        </div>
      </div>
    </div>

    <!-- Orders Table -->
    <v-card class="orders-table-card" elevation="0">
      <div class="table-container">
        <table class="orders-table">
          <thead>
            <tr>
              <th>Receipt #</th>
              <th>Customer</th>
              <th>Order Type</th>
              <th>Items</th>
              <th>Total</th>
              <th>Date</th>
              <th>Payment</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="order in paginatedOrders"
              :key="order.id"
              :class="{
                'debt-row':
                  order.paymentMode === 'debt' &&
                  order.paymentStatus === 'pending',
              }"
            >
              <td class="receipt-cell">{{ order.receiptNumber }}</td>
              <td>{{ order.customerName }}</td>
              <td>
                <span class="order-type-badge" :class="order.orderType">
                  {{ order.orderType }}
                </span>
              </td>
              <td>{{ order.items.length }} items</td>
              <td class="amount-cell">ksh{{ order.total }}</td>
              <td>{{ formatDate(order.created_at) }}</td>
              <td>
                <span class="payment-badge" :class="order.paymentMode">
                  <v-icon size="12" class="mr-1">
                    {{ getPaymentIcon(order.paymentMode) }}
                  </v-icon>
                  {{ order.paymentMode }}
                </span>
              </td>
              <td>
                <span
                  class="status-badge"
                  :class="order.paymentStatus || 'completed'"
                >
                  {{ order.paymentStatus || "completed" }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    @click="viewOrderDetails(order)"
                  >
                    <v-icon size="18">mdi-eye</v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    @click="printReceipt(order)"
                  >
                    <v-icon size="18">mdi-printer</v-icon>
                  </v-btn>
                  <v-btn
                    v-if="
                      order.paymentMode === 'debt' &&
                      order.paymentStatus === 'pending'
                    "
                    icon
                    size="small"
                    variant="text"
                    color="#2D6A4F"
                    @click="markDebtAsPaid(order)"
                  >
                    <v-icon size="18">mdi-check-circle</v-icon>
                  </v-btn>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination-section">
        <div class="items-per-page">
          <span>Show</span>
          <select v-model="itemsPerPage">
            <option :value="10">10</option>
            <option :value="25">25</option>
            <option :value="50">50</option>
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
    <v-dialog
      v-model="showDebtManagement"
      max-width="900"
      transition="dialog-transition"
    >
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
          <div class="debt-summary-cards">
            <div class="debt-stat-card">
              <div class="stat-icon" style="background: #e07a5f20">
                <v-icon color="#E07A5F" size="24">mdi-cash</v-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">
                  ksh{{ debtOverview.total_debt?.toFixed(2) || 0 }}
                </div>
                <div class="stat-label">Total Outstanding</div>
              </div>
            </div>
            <div class="debt-stat-card">
              <div class="stat-icon" style="background: #2d6a4f20">
                <v-icon color="#2D6A4F" size="24">mdi-account-group</v-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">
                  {{ debtOverview.total_customers || 0 }}
                </div>
                <div class="stat-label">Customers with Debt</div>
              </div>
            </div>
            <div class="debt-stat-card">
              <div class="stat-icon" style="background: #f4a26120">
                <v-icon color="#F4A261" size="24">mdi-clock-outline</v-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">
                  {{ debtOverview.average_age || 0 }} days
                </div>
                <div class="stat-label">Average Age</div>
              </div>
            </div>
          </div>

          <!-- Debt Aging Breakdown -->
          <div class="debt-aging-section">
            <div class="aging-header">
              <span class="aging-title">📊 Aging Breakdown</span>
            </div>
            <div class="aging-bars">
              <div class="aging-item">
                <span class="aging-label">0-7 Days</span>
                <div class="aging-bar">
                  <div
                    class="aging-fill"
                    :style="{
                      width: getAgingPercentage('0-7_days') + '%',
                      background: getAgingColor('0-7_days'),
                    }"
                  ></div>
                </div>
                <span class="aging-amount"
                  >ksh{{
                    debtOverview.by_age?.["0-7_days"]?.toFixed(2) || 0
                  }}</span
                >
              </div>
              <div class="aging-item">
                <span class="aging-label">8-14 Days</span>
                <div class="aging-bar">
                  <div
                    class="aging-fill"
                    :style="{
                      width: getAgingPercentage('8-14_days') + '%',
                      background: getAgingColor('8-14_days'),
                    }"
                  ></div>
                </div>
                <span class="aging-amount"
                  >ksh{{
                    debtOverview.by_age?.["8-14_days"]?.toFixed(2) || 0
                  }}</span
                >
              </div>
              <div class="aging-item">
                <span class="aging-label">15-30 Days</span>
                <div class="aging-bar">
                  <div
                    class="aging-fill"
                    :style="{
                      width: getAgingPercentage('15-30_days') + '%',
                      background: getAgingColor('15-30_days'),
                    }"
                  ></div>
                </div>
                <span class="aging-amount"
                  >ksh{{
                    debtOverview.by_age?.["15-30_days"]?.toFixed(2) || 0
                  }}</span
                >
              </div>
              <div class="aging-item">
                <span class="aging-label">30+ Days</span>
                <div class="aging-bar">
                  <div
                    class="aging-fill"
                    :style="{
                      width: getAgingPercentage('30+_days') + '%',
                      background: getAgingColor('30+_days'),
                    }"
                  ></div>
                </div>
                <span class="aging-amount"
                  >ksh{{
                    debtOverview.by_age?.["30+_days"]?.toFixed(2) || 0
                  }}</span
                >
              </div>
            </div>
          </div>

          <!-- Debt List -->
          <div class="debt-list-section">
            <div class="list-header">
              <span class="list-title">📋 All Pending Debts</span>
              <span class="list-count"
                >{{ debtOverview.debts?.length || 0 }} orders</span
              >
            </div>
            <div class="debt-list">
              <div
                v-for="debt in debtOverview.debts"
                :key="debt.id"
                class="debt-list-item"
                :class="{ overdue: debt.age_days > 7 }"
              >
                <div class="debt-item-info">
                  <div class="debt-item-customer">{{ debt.customerName }}</div>
                  <div class="debt-item-receipt">{{ debt.receiptNumber }}</div>
                  <div class="debt-item-date">
                    {{ formatDate(debt.created_at) }}
                  </div>
                </div>
                <div class="debt-item-amount">
                  ksh{{ debt.total.toFixed(2) }}
                </div>
                <div class="debt-item-age">
                  <span :class="{ 'overdue-text': debt.age_days > 7 }">
                    {{ debt.age_days }} days
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
                <v-btn
                  size="small"
                  color="#2D6A4F"
                  @click="markDebtAsPaid(debt)"
                >
                  <v-icon start size="16">mdi-check</v-icon>
                  Mark Paid
                </v-btn>
              </div>
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

    <!-- Order Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="800">
      <v-card
        class="order-details-dialog"
        :class="{ 'debt-dialog': selectedOrder?.paymentMode === 'debt' }"
      >
        <div class="dialog-header">
          <div>
            <div class="receipt-badge">Order Details</div>
            <h2>{{ selectedOrder?.receiptNumber }}</h2>
          </div>
          <v-btn icon variant="text" @click="detailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <div class="order-info-grid">
          <div class="info-card">
            <div class="info-label">Customer Name</div>
            <div class="info-value">{{ selectedOrder?.customerName }}</div>
          </div>
          <div class="info-card">
            <div class="info-label">Order Type</div>
            <div class="info-value">{{ selectedOrder?.orderType }}</div>
          </div>
          <div class="info-card">
            <div class="info-label">Table/Number</div>
            <div class="info-value">
              {{ selectedOrder?.tableNumber || "N/A" }}
            </div>
          </div>
          <div class="info-card">
            <div class="info-label">Date & Time</div>
            <div class="info-value">
              {{ formatDate(selectedOrder?.created_at) }}
            </div>
          </div>
          <div class="info-card">
            <div class="info-label">Payment Method</div>
            <div class="info-value">
              <span class="payment-badge" :class="selectedOrder?.paymentMode">
                <v-icon size="14" class="mr-1">
                  {{ getPaymentIcon(selectedOrder?.paymentMode) }}
                </v-icon>
                {{ selectedOrder?.paymentMode }}
              </span>
            </div>
          </div>
          <div class="info-card">
            <div class="info-label">Payment Status</div>
            <div class="info-value">
              <span class="status-badge" :class="selectedOrder?.paymentStatus">
                {{ selectedOrder?.paymentStatus || "completed" }}
              </span>
            </div>
          </div>
        </div>

        <!-- Debt Order Note -->
        <div
          v-if="
            selectedOrder?.paymentMode === 'debt' &&
            selectedOrder?.paymentStatus === 'pending'
          "
          class="debt-notice"
        >
          <v-icon size="24" color="#E07A5F">mdi-alert-circle</v-icon>
          <div>
            <strong>Debt Order</strong>
            <p>
              This order is recorded as debt. Please collect payment from the
              customer.
            </p>
            <v-btn
              size="small"
              color="#2D6A4F"
              @click="markDebtAsPaid(selectedOrder)"
            >
              <v-icon start size="16">mdi-check</v-icon>
              Mark as Paid
            </v-btn>
          </div>
        </div>

        <div class="items-list">
          <h3>Order Items</h3>
          <div
            v-for="item in selectedOrder?.items"
            :key="item.id"
            class="order-item-detail"
          >
            <div class="item-detail-info">
              <div class="item-detail-name">{{ item.name }}</div>
              <div class="item-detail-meta">
                <span>{{ item.size || "Regular" }}</span>
                <span>{{ item.temp || "Hot" }}</span>
              </div>
            </div>
            <div class="item-detail-qty">
              <span class="item-unit-price">ksh{{ item.price }}</span>
              x {{ item.quantity }}
            </div>
            <div class="item-detail-price">
              ksh{{ (item.price * item.quantity).toFixed(2) }}
            </div>
          </div>
        </div>

        <div class="order-summary">
          <div class="summary-row">
            <span>Subtotal</span>
            <span>ksh{{ selectedOrder?.subtotal }}</span>
          </div>
          <div class="summary-row">
            <span>Tax (10%)</span>
            <span>ksh{{ selectedOrder?.tax }}</span>
          </div>
          <div class="summary-row total">
            <span>Total</span>
            <span>ksh{{ selectedOrder?.total }}</span>
          </div>
          <div
            v-if="selectedOrder?.paymentMode === 'debt'"
            class="summary-row debt-note-row"
          >
            <span>Debt Status</span>
            <span class="status-badge" :class="selectedOrder?.paymentStatus">
              {{ selectedOrder?.paymentStatus || "pending" }}
            </span>
          </div>
        </div>

        <div class="dialog-actions">
          <v-btn variant="outlined" @click="printReceipt(selectedOrder)">
            <v-icon start>mdi-printer</v-icon>
            Print Receipt
          </v-btn>
          <v-btn
            v-if="
              selectedOrder?.paymentMode === 'debt' &&
              selectedOrder?.paymentStatus === 'pending'
            "
            color="#2D6A4F"
            @click="markDebtAsPaid(selectedOrder)"
          >
            <v-icon start>mdi-check</v-icon>
            Mark as Paid
          </v-btn>
          <v-btn color="#2D6A4F" @click="detailsDialog = false">Close</v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Debt Management Dialog -->
    <!-- <v-dialog v-model="showDebtManagement" max-width="900">
      <v-card class="debt-management-dialog">
        <div class="dialog-header">
          <div>
            <div class="receipt-badge">Debt Management</div>
            <h2>Outstanding Debts</h2>
            <p class="subtitle">Manage and track all pending debt orders</p>
          </div>
          <v-btn icon variant="text" @click="showDebtManagement = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <div class="debt-summary">
          <div class="debt-stat">
            <div class="debt-stat-value">{{ debtOrders.length }}</div>
            <div class="debt-stat-label">Pending Debts</div>
          </div>
          <div class="debt-stat">
            <div class="debt-stat-value">ksh{{ totalDebt }}</div>
            <div class="debt-stat-label">Total Outstanding</div>
          </div>
          <div class="debt-stat">
            <div class="debt-stat-value">{{ uniqueDebtCustomers.length }}</div>
            <div class="debt-stat-label">Customers with Debt</div>
          </div>
        </div>

        <div class="debt-list">
          <div v-for="order in debtOrders" :key="order.id" class="debt-item">
            <div class="debt-item-info">
              <div class="debt-customer">
                <div class="debt-customer-name">{{ order.customerName }}</div>
                <div class="debt-order-ref">{{ order.receiptNumber }}</div>
              </div>
              <div class="debt-item-details">
                <div class="debt-amount">ksh{{ order.total }}</div>
                <div class="debt-date">{{ formatDate(order.created_at) }}</div>
              </div>
            </div>
            <div class="debt-item-actions">
              <v-btn
                size="small"
                variant="text"
                @click="viewOrderDetails(order)"
              >
                <v-icon size="16">mdi-eye</v-icon>
              </v-btn>
              <v-btn
                size="small"
                color="#2D6A4F"
                @click="markDebtAsPaid(order)"
              >
                <v-icon start size="16">mdi-check</v-icon>
                Mark Paid
              </v-btn>
            </div>
          </div>
          <div v-if="debtOrders.length === 0" class="no-debts">
            <v-icon size="48" color="#E5E7EB">mdi-check-circle</v-icon>
            <p>No outstanding debts! 🎉</p>
            <span>All debt orders have been cleared.</span>
          </div>
        </div>
      </v-card>
    </v-dialog> -->

    <!-- Mark Debt as Paid Confirmation Dialog -->
    <v-dialog v-model="showPaidConfirmation" max-width="400">
      <v-card class="confirm-dialog">
        <div class="confirm-icon">
          <v-icon size="64" color="#2D6A4F">mdi-check-circle</v-icon>
        </div>
        <h3>Mark Debt as Paid?</h3>
        <p>
          Confirm that <strong>{{ selectedOrder?.customerName }}</strong> has
          paid <strong>ksh{{ selectedOrder?.total }}</strong> for order
          <strong>{{ selectedOrder?.receiptNumber }}</strong>
        </p>
        <div class="confirm-actions">
          <v-btn variant="text" @click="showPaidConfirmation = false"
            >Cancel</v-btn
          >
          <v-btn color="#2D6A4F" @click="confirmMarkAsPaid"
            >Confirm Payment</v-btn
          >
        </div>
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

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const store = usePosStore();
const searchQuery = ref("");
const selectedType = ref("");
const selectedPaymentMode = ref("");
const selectedStatus = ref("");
const dateFilter = ref("");
const itemsPerPage = ref(10);
const currentPage = ref(1);
const detailsDialog = ref(false);
// const showDebtManagement = ref(false);
// const showPaidConfirmation = ref(false);
const selectedOrder = ref(null);

const showDebtManagement = ref(false);
const showPaidConfirmation = ref(false);
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

const orders = computed(() => store.AllOrders || []);

// Debt orders filter
const debtOrders = computed(() => {
  return orders.value.filter(
    (order) => order.paymentMode === "debt" && order.paymentStatus === "pending"
  );
});
const debtList = computed(() => debtOverview.value.debts || []);

const hasDebtOrders = computed(() => debtOrders.value.length > 0);
const totalDebt = computed(() => {
  return debtOrders.value
    .reduce((sum, order) => sum + order.total, 0)
    .toFixed(2);
});
const debtCount = computed(() => debtOrders.value.length);

const uniqueDebtCustomers = computed(() => {
  const customers = new Set(debtOrders.value.map((o) => o.customerName));
  return Array.from(customers);
});

const filteredOrders = computed(() => {
  let filtered = [...orders.value];

  if (searchQuery.value) {
    filtered = filtered.filter(
      (order) =>
        order.receiptNumber
          ?.toLowerCase()
          .includes(searchQuery.value.toLowerCase()) ||
        order.customerName
          ?.toLowerCase()
          .includes(searchQuery.value.toLowerCase())
    );
  }

  if (selectedType.value) {
    filtered = filtered.filter(
      (order) => order.orderType === selectedType.value
    );
  }

  if (selectedPaymentMode.value) {
    filtered = filtered.filter(
      (order) => order.paymentMode === selectedPaymentMode.value
    );
  }

  if (selectedStatus.value) {
    filtered = filtered.filter(
      (order) => order.paymentStatus === selectedStatus.value
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
    .filter((order) => order.paymentStatus === "completed")
    .reduce((sum, order) => sum + order.total, 0)
    .toFixed(2);
});

const avgOrderValue = computed(() => {
  const completedOrders = filteredOrders.value.filter(
    (order) => order.paymentStatus === "completed"
  );
  if (completedOrders.length === 0) return "0";
  return (parseFloat(totalRevenue.value) / completedOrders.length).toFixed(2);
});

const totalPages = computed(() =>
  Math.ceil(filteredOrders.value.length / itemsPerPage.value)
);

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredOrders.value.slice(start, end);
});

const getPaymentIcon = (mode: string) => {
  const icons: Record<string, string> = {
    cash: "mdi-cash",
    mpesa: "mdi-cellphone",
    debt: "mdi-account-cash",
  };
  return icons[mode] || "mdi-help-circle";
};

const formatDate = (date) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleString();
};

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const viewOrderDetails = (order) => {
  selectedOrder.value = order;
  detailsDialog.value = true;
};

const fetchDebtOverview = async () => {
  try {
    const response = await store.getDebtOverview();
    debtOverview.value = response;
  } catch (error) {
    console.error("Error fetching debt overview:", error);
  }
};

const printReceipt = (order) => {
  // Use the receipt composable
  const { printReceipt } = useReceipt();
  printReceipt(order);
};

const markDebtAsPaid = (order) => {
  selectedOrder.value = order;
  showPaidConfirmation.value = true;
};

const confirmMarkAsPaid = async () => {
  const store = usePosStore();
  if (!selectedOrder.value) return;

  try {
    const orderId = selectedOrder.value._id ?? selectedOrder.value.id;
    await store.updateDebtOrderStatus(orderId);
    await fetchDebtOverview();
    await store.getAllOrders();

    // For demo, update locally
    const orderIndex = store.AllOrders.findIndex(
      (o) => o._id === selectedOrder.value._id
    );
    if (orderIndex !== -1) {
      store.AllOrders[orderIndex].paymentStatus = "completed";
      store.AllOrders[orderIndex].clearedAt = new Date().toISOString();
      store.AllOrders[orderIndex].clearedBy = "Cashier";
    }

    showPaidConfirmation.value = false;
    detailsDialog.value = false;
    showDebtManagement.value = false;

    snackbar.value = {
      show: true,
      text: `Debt of ksh${selectedOrder.value.total} from ${selectedOrder.value.customerName} marked as paid!`,
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

const exportOrders = () => {
  // Export orders as CSV
  const headers = [
    "Receipt #",
    "Customer",
    "Order Type",
    "Items",
    "Total",
    "Payment Method",
    "Status",
    "Date",
  ];
  const rows = filteredOrders.value.map((order) => [
    order.receiptNumber,
    order.customerName,
    order.orderType,
    order.items.length,
    order.total,
    order.paymentMode,
    order.paymentStatus,
    new Date(order.created_at).toLocaleString(),
  ]);

  let csv = headers.join(",") + "\n";
  rows.forEach((row) => {
    csv += row.join(",") + "\n";
  });

  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `orders_${new Date().toISOString().split("T")[0]}.csv`;
  link.click();
  URL.revokeObjectURL(url);
};

const refreshDebtData = () => {
  console.log("Refreshing debt data...");
  fetchDebtOverview();
};

const getAgingPercentage = (key: string) => {
  const total = debtOverview.value.total_debt || 0;
  const value =
    debtOverview.value.by_age?.[
      key as keyof typeof debtOverview.value.by_age
    ] || 0;
  return total > 0 ? (value / total) * 100 : 0;
};

const getAgingColor = (key: string) => {
  const colors: Record<string, string> = {
    "0-7_days": "#2D6A4F",
    "8-14_days": "#F4A261",
    "15-30_days": "#E07A5F",
    "30+_days": "#EF4444",
  };
  return colors[key] || "#9CA3AF";
};

onMounted(async () => {
  await fetchDebtOverview();
  await store.getAllOrders();
});
</script>

<style scoped>
.orders-container {
  padding: 32px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
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

.export-btn {
  border-color: #e5e7eb;
  border-radius: 40px;
}

.filters-section {
  background: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 24px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.search-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background: #f8f6f2;
  border-radius: 40px;
  padding: 0 16px;
  gap: 12px;
}

.search-input {
  flex: 1;
  border: none;
  padding: 12px 0;
  background: transparent;
  outline: none;
}

.filter-group {
  display: flex;
  gap: 12px;
}

.filter-select,
.date-picker {
  padding: 8px 16px;
  border-radius: 40px;
  border: 1px solid #e5e7eb;
  background: white;
  outline: none;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.summary-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.summary-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.summary-value {
  font-size: 28px;
  font-weight: 800;
  color: #1b4332;
}

.summary-label {
  font-size: 13px;
  color: #6b7280;
}

.orders-table-card {
  border-radius: 24px;
  overflow: hidden;
}

.table-container {
  overflow-x: auto;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
}

.orders-table th {
  text-align: left;
  padding: 16px 20px;
  background: #f8f6f2;
  font-weight: 600;
  color: #374151;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.orders-table td {
  padding: 16px 20px;
  border-bottom: 1px solid #f3f4f6;
  color: #4b5563;
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

.order-type-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.order-type-badge.dine-in {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.order-type-badge.take-away {
  background: #f4a26120;
  color: #f4a261;
}

.order-type-badge.order-online {
  background: #6b4e7120;
  color: #6b4e71;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.status-badge.completed {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.status-badge.preparing {
  background: #f4a26120;
  color: #f4a261;
}

.status-badge.cancelled {
  background: #e07a5f20;
  color: #e07a5f;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
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
  border-radius: 8px;
  border: 1px solid #e5e7eb;
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

/* Dialog Styles */
.order-details-dialog {
  border-radius: 32px !important;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
}

.dialog-header .receipt-badge {
  font-size: 11px;
  font-weight: 600;
  color: #e07a5f;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.dialog-header h2 {
  font-family: "Playfair Display", serif;
  font-size: 24px;
  font-weight: 700;
  color: #1b4332;
}

.order-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 24px;
}

.info-card {
  background: #f8f6f2;
  padding: 16px;
  border-radius: 16px;
}

.info-label {
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.info-value {
  font-weight: 600;
  color: #1b4332;
}

.items-list {
  padding: 0 24px;
}

.items-list h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 16px;
}

.order-item-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.item-detail-name {
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 4px;
}

.item-detail-meta {
  display: flex;
  gap: 12px;
  font-size: 11px;
  color: #6b7280;
}

.item-detail-price {
  font-weight: 600;
  color: #e07a5f;
}

.order-summary {
  background: #f8f6f2;
  margin: 24px;
  padding: 20px;
  border-radius: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
}

.summary-row.total {
  border-top: 2px solid #e5e7eb;
  margin-top: 8px;
  padding-top: 12px;
  font-size: 18px;
  font-weight: 800;
  color: #1b4332;
}

.dialog-actions {
  padding: 16px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.debt-row {
  background: #fff8f0;
  border-left: 3px solid #e07a5f;
}

.debt-row:hover {
  background: #fff3e0;
}

.payment-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.payment-badge.cash {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.payment-badge.mpesa {
  background: #6b4e7120;
  color: #6b4e71;
}

.payment-badge.debt {
  background: #e07a5f20;
  color: #e07a5f;
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

.debt-dialog {
  border: 2px solid #e07a5f;
}

.debt-notice {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  background: #fff3e0;
  border-radius: 16px;
  margin: 0 24px 16px 24px;
  border: 1px solid #e07a5f40;
}

.debt-notice p {
  margin: 4px 0;
  color: #6b7280;
  font-size: 14px;
}

.debt-notice strong {
  color: #1b4332;
  font-size: 16px;
}

.summary-sub {
  font-size: 11px;
  color: #6b7280;
  margin-top: 2px;
}

/* Debt Management Dialog */
.debt-management-dialog {
  border-radius: 32px !important;
  overflow: hidden;
}

.debt-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 16px 24px;
}

.debt-stat {
  background: #f8f6f2;
  padding: 16px;
  border-radius: 16px;
  text-align: center;
}

.debt-stat-value {
  font-size: 28px;
  font-weight: 800;
  color: #1b4332;
}

.debt-stat-label {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

.debt-list {
  padding: 0 24px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.debt-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8f6f2;
  border-radius: 16px;
  border-left: 4px solid #e07a5f;
  transition: all 0.3s ease;
}

.debt-item:hover {
  background: #f0ede5;
}

.debt-item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.debt-customer-name {
  font-weight: 700;
  color: #1b4332;
  font-size: 16px;
}

.debt-order-ref {
  font-size: 12px;
  color: #6b7280;
}

.debt-item-details {
  text-align: right;
}

.debt-amount {
  font-size: 18px;
  font-weight: 800;
  color: #e07a5f;
}

.debt-date {
  font-size: 11px;
  color: #6b7280;
}

.debt-item-actions {
  display: flex;
  gap: 8px;
}

.no-debts {
  text-align: center;
  padding: 48px;
  color: #6b7280;
}

.no-debts p {
  font-size: 18px;
  font-weight: 600;
  color: #1b4332;
  margin-top: 16px;
}

/* Confirm Dialog */
.confirm-dialog {
  text-align: center;
  padding: 32px;
  border-radius: 32px !important;
}

.confirm-icon {
  margin-bottom: 20px;
}

.confirm-dialog h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 12px;
}

.confirm-dialog p {
  color: #6b7280;
  margin-bottom: 24px;
  line-height: 1.5;
}

.confirm-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.summary-row.debt-note-row {
  border-top: 1px solid #e5e7eb;
  margin-top: 8px;
  padding-top: 12px;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 1200px) {
  .debt-summary {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .debt-item {
    flex-direction: column;
    gap: 12px;
  }

  .debt-item-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .debt-notice {
    flex-direction: column;
    text-align: center;
  }
}
.debt-overview-section {
  background: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #e07a5f20;
}

.debt-overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.debt-title {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.header-right {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.total-debt-label {
  font-size: 13px;
  color: #6b7280;
}

.total-debt-amount {
  font-size: 24px;
  font-weight: 800;
  color: #e07a5f;
}

.debt-stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.debt-stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f8f6f2;
  border-radius: 12px;
}

.debt-stat-card .stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.debt-stat-card .stat-info {
  flex: 1;
}

.debt-stat-card .stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.debt-stat-card .stat-label {
  font-size: 11px;
  color: #6b7280;
}

/* Debt Aging Section */
.debt-aging-section {
  background: #f8f6f2;
  padding: 16px;
  border-radius: 12px;
}

.aging-header {
  margin-bottom: 12px;
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

/* Debt Management Dialog */
.debt-management-dialog {
  border-radius: 32px !important;
  overflow: hidden;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0 24px;
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
}

.title-content {
  display: flex;
  align-items: center;
}

.dialog-content {
  padding: 24px;
}

.debt-summary-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.debt-list-section {
  margin-top: 24px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.list-title {
  font-weight: 600;
  color: #1b4332;
}

.list-count {
  font-size: 12px;
  color: #6b7280;
}

.debt-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 400px;
  overflow-y: auto;
}

.debt-list-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: #f8f6f2;
  border-radius: 12px;
  border-left: 3px solid #e07a5f;
}

.debt-list-item.overdue {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.debt-item-info {
  flex: 1;
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
  font-size: 10px;
  color: #9ca3af;
}

.debt-item-amount {
  font-weight: 700;
  color: #e07a5f;
  min-width: 80px;
}

.debt-item-age {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 80px;
}

.debt-item-age span {
  font-size: 12px;
  color: #6b7280;
}

.debt-item-age span.overdue-text {
  color: #ef4444;
  font-weight: 600;
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

.no-debts {
  text-align: center;
  padding: 32px;
  color: #6b7280;
}

.no-debts p {
  margin-top: 12px;
  font-size: 16px;
  font-weight: 600;
  color: #1b4332;
}

.no-debts-sub {
  font-size: 13px;
  color: #6b7280;
}

.dialog-actions {
  padding: 16px 24px 24px;
  gap: 12px;
}

/* Debt Row in Table */
.debt-row {
  background: #fff8f0;
  border-left: 3px solid #e07a5f;
}

.debt-row:hover {
  background: #fff3e0;
}

.payment-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.payment-badge.cash {
  background: #2d6a4f20;
  color: #2d6a4f;
}

.payment-badge.mpesa {
  background: #6b4e7120;
  color: #6b4e71;
}

.payment-badge.debt {
  background: #e07a5f20;
  color: #e07a5f;
}

/* Confirm Dialog */
.confirm-dialog {
  text-align: center;
  padding: 32px;
  border-radius: 32px !important;
}

.confirm-icon {
  margin-bottom: 20px;
}

.confirm-dialog h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 12px;
}

.confirm-dialog p {
  color: #6b7280;
  margin-bottom: 24px;
  line-height: 1.5;
}

.confirm-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

/* Responsive */
@media (max-width: 768px) {
  .debt-stats-grid {
    grid-template-columns: 1fr;
  }

  .debt-summary-cards {
    grid-template-columns: 1fr;
  }

  .debt-list-item {
    flex-wrap: wrap;
    gap: 8px;
  }

  .debt-overview-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .debt-item-age {
    min-width: auto;
  }

  .debt-item-amount {
    min-width: auto;
  }
}
</style>
