<!-- frontend/pages/admin/expenses/index.vue -->
<template>
  <div class="expenses-dashboard">
    <!-- Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">Financial Management</div>
        <h1 class="page-title">Expense Dashboard</h1>
        <p class="page-subtitle">
          Track, analyze and manage your business expenses
        </p>
      </div>
      <div class="header-actions">
        <v-btn
          color="#E07A5F"
          class="add-expense-btn"
          @click="OpenExpeseDialog"
        >
          <v-icon start>mdi-plus</v-icon>
          Add Expense
        </v-btn>
        <v-btn
          variant="outlined"
          class="export-btn"
          @click="exportExpenseReport"
        >
          <v-icon start>mdi-export</v-icon>
          Export
        </v-btn>
      </div>
    </div>

    <!-- Period Selector -->
    <div class="period-selector">
      <v-btn-toggle
        v-model="selectedPeriod"
        color="#2D6A4F"
        group
        mandatory
        class="period-toggle"
      >
        <v-btn value="day" class="period-btn">
          <v-icon start size="18">mdi-calendar-today</v-icon>
          Today
        </v-btn>
        <v-btn value="week" class="period-btn">
          <v-icon start size="18">mdi-calendar-week</v-icon>
          This Week
        </v-btn>
        <v-btn value="month" class="period-btn">
          <v-icon start size="18">mdi-calendar-month</v-icon>
          This Month
        </v-btn>
        <v-btn value="year" class="period-btn">
          <v-icon start size="18">mdi-calendar-year</v-icon>
          This Year
        </v-btn>
        <v-btn value="custom" class="period-btn">
          <v-icon start size="18">mdi-calendar-range</v-icon>
          Custom
        </v-btn>
      </v-btn-toggle>

      <!-- Custom Date Range -->
      <div v-if="selectedPeriod === 'custom'" class="custom-date-range">
        <v-text-field
          v-model="customStartDate"
          type="date"
          label="Start Date"
          variant="outlined"
          density="comfortable"
          hide-details
          class="date-field"
        />
        <span class="date-separator">to</span>
        <v-text-field
          v-model="customEndDate"
          type="date"
          label="End Date"
          variant="outlined"
          density="comfortable"
          hide-details
          class="date-field"
        />
        <v-btn color="#2D6A4F" @click="applyCustomRange" class="apply-btn">
          Apply
        </v-btn>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="summary-grid">
      <div class="summary-card total">
        <div class="card-icon" style="background: #2d6a4f20">
          <v-icon color="#2D6A4F" size="28">mdi-cash-multiple</v-icon>
        </div>
        <div class="card-content">
          <div class="card-label">Total Expenses</div>
          <div class="card-value">ksh{{ totalExpenses.toFixed(2) }}</div>
          <div class="card-change" :class="expenseChangeClass">
            <v-icon size="16">{{ expenseChangeIcon }}</v-icon>
            <span>{{ expenseChangePercent }} from previous period</span>
          </div>
        </div>
      </div>

      <div class="summary-card average">
        <div class="card-icon" style="background: #e07a5f20">
          <v-icon color="#E07A5F" size="28">mdi-chart-line</v-icon>
        </div>
        <div class="card-content">
          <div class="card-label">Daily Average</div>
          <div class="card-value">ksh{{ dailyAverage.toFixed(2) }}</div>
          <div class="card-sub">{{ periodDays }} days tracked</div>
        </div>
      </div>

      <div class="summary-card highest">
        <div class="card-icon" style="background: #f4a26120">
          <v-icon color="#F4A261" size="28">mdi-arrow-up</v-icon>
        </div>
        <div class="card-content">
          <div class="card-label">Highest Day</div>
          <div class="card-value">
            ksh{{ highestDay?.amount?.toFixed(2) || 0 }}
          </div>
          <div class="card-sub">{{ highestDay?.date || "N/A" }}</div>
        </div>
      </div>

      <div class="summary-card count">
        <div class="card-icon" style="background: #6b4e7120">
          <v-icon color="#6B4E71" size="28">mdi-receipt</v-icon>
        </div>
        <div class="card-content">
          <div class="card-label">Total Transactions</div>
          <div class="card-value">{{ expenseCount }}</div>
          <div class="card-sub">expenses recorded</div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-row">
      <!-- Expense Trend Chart -->
      <v-card class="chart-card" elevation="0">
        <div class="chart-header">
          <div>
            <div class="chart-title">Expense Trend</div>
            <div class="chart-subtitle">Daily expense pattern</div>
          </div>
          <v-select
            v-model="chartView"
            :items="['Line', 'Bar']"
            variant="outlined"
            density="compact"
            class="chart-view-select"
          />
        </div>
        <div class="chart-container">
          <canvas ref="trendChart"></canvas>
        </div>
      </v-card>

      <!-- Category Breakdown -->
      <v-card class="chart-card" elevation="0">
        <div class="chart-header">
          <div>
            <div class="chart-title">Category Breakdown</div>
            <div class="chart-subtitle">Where your money goes</div>
          </div>
        </div>
        <div class="chart-container small">
          <ClientOnly>
            <canvas ref="categoryChart"> </canvas>
          </ClientOnly>
        </div>
        <div class="category-legend">
          <div
            v-for="category in categoryBreakdown"
            :key="category.name"
            class="legend-item"
          >
            <div
              class="legend-color"
              :style="{ background: category.color }"
            ></div>
            <div class="legend-name">{{ category.name }}</div>
            <div class="legend-amount">ksh{{ category.amount.toFixed(2) }}</div>
            <div class="legend-percentage">
              {{ category.percentage.toFixed(2) }}%
            </div>
          </div>
        </div>
      </v-card>
    </div>

    <!-- Top Expense Categories -->
    <div class="categories-section">
      <v-card class="categories-card" elevation="0">
        <div class="card-header">
          <div>
            <div class="card-title">💰 Top Expense Categories</div>
            <div class="card-subtitle">Where most of your money is going</div>
          </div>
          <v-btn
            variant="text"
            class="view-all-btn"
            @click="showAllCategories = !showAllCategories"
          >
            {{ showAllCategories ? "Show Less" : "View All" }}
          </v-btn>
        </div>

        <div class="categories-grid">
          <div
            v-for="(category, index) in displayCategories"
            :key="category.name"
            class="category-item"
            :class="{ 'top-category': index < 3 }"
          >
            <div class="category-rank">
              <div class="rank-badge" :class="getRankClass(index + 1)">
                {{ index + 1 }}
              </div>
            </div>
            <div class="category-info">
              <div class="category-name">{{ category.name }}</div>
              <div class="category-transactions">
                {{ category.count }} transactions
              </div>
            </div>
            <div class="category-amount">
              ksh{{ category.amount.toFixed(2) }}
            </div>
            <div class="category-progress">
              <div
                class="progress-bar"
                :style="{
                  width: `${category.percentage}%`,
                  background: getCategoryColor(index),
                }"
              ></div>
            </div>
          </div>
        </div>
      </v-card>
    </div>

    <!-- Recent Expenses Table -->
    <v-card class="expenses-table-card" elevation="0">
      <div class="card-header">
        <div>
          <div class="card-title">📋 Recent Expenses</div>
          <div class="card-subtitle">Latest expense transactions</div>
        </div>
        <div class="table-controls">
          <div class="search-wrapper">
            <v-icon size="16">mdi-magnify</v-icon>
            <input
              v-model="tableSearch"
              placeholder="Search expenses..."
              class="table-search"
            />
          </div>
          <v-select
            v-model="categoryFilter"
            :items="categoryFilterOptions"
            variant="outlined"
            density="compact"
            placeholder="Filter by category"
            class="category-filter"
          />
        </div>
      </div>

      <div class="table-container">
        <table class="expenses-table">
          <thead>
            <tr>
              <th @click="sortBy('date')">
                Date
                <v-icon size="14">{{ getSortIcon("date") }}</v-icon>
              </th>
              <th @click="sortBy('description')">
                Description
                <v-icon size="14">{{ getSortIcon("description") }}</v-icon>
              </th>
              <th @click="sortBy('category')">
                Category
                <v-icon size="14">{{ getSortIcon("category") }}</v-icon>
              </th>
              <th @click="sortBy('amount')">
                Amount
                <v-icon size="14">{{ getSortIcon("amount") }}</v-icon>
              </th>
              <th @click="sortBy('payment_method')">
                Payment
                <v-icon size="14">{{ getSortIcon("payment_method") }}</v-icon>
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="expense in paginatedExpenses" :key="expense.id">
              <td class="date-cell">{{ formatDate(expense.date) }}</td>
              <td class="desc-cell">{{ expense.description }}</td>
              <td>
                <span
                  class="category-badge"
                  :style="{
                    background: getCategoryColorByName(expense.category) + '20',
                    color: getCategoryColorByName(expense.category),
                  }"
                >
                  {{ formatCategoryName(expense.category) }}
                </span>
              </td>
              <td class="amount-cell">ksh{{ expense.amount.toFixed(2) }}</td>
              <td>
                <span class="payment-badge" :class="expense.payment_method">
                  {{ expense.payment_method }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    @click="viewExpenseDetails(expense)"
                  >
                    <v-icon size="18">mdi-eye</v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    color="#E07A5F"
                    @click="deleteExpense(expense)"
                  >
                    <v-icon size="18">mdi-delete</v-icon>
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
            <option :value="5">5</option>
            <option :value="10">10</option>
            <option :value="20">20</option>
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

    <!-- Add Expense Dialog -->
    <v-dialog
      v-model="showExpenseDialog"
      max-width="600"
      transition="dialog-transition"
    >
      <v-card class="expense-dialog">
        <v-card-title class="dialog-header">
          <div class="title-content">
            <v-icon size="28" color="#E07A5F" class="mr-3"
              >mdi-cash-minus</v-icon
            >
            <span>Record Expense</span>
          </div>
          <v-btn icon variant="text" @click="showExpenseDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="dialog-content">
          <v-form ref="expenseForm" v-model="isValid">
            <v-row>
              <v-col cols="12" md="8">
                <v-text-field
                  v-model="expenseFormData.description"
                  label="Expense Description"
                  placeholder="e.g., Coffee beans purchase"
                  variant="outlined"
                  :rules="[rules.required]"
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="expenseFormData.amount"
                  label="Amount"
                  type="number"
                  placeholder="0.00"
                  prefix="KSH"
                  variant="outlined"
                  :rules="[rules.required, rules.positive]"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="expenseFormData.category"
                  label="Category"
                  :items="expenseCategories"
                  variant="outlined"
                  :rules="[rules.required]"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="expenseFormData.payment_method"
                  label="Payment Method"
                  :items="paymentMethods"
                  variant="outlined"
                  :rules="[rules.required]"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12">
                <v-file-input
                  v-model="expenseFormData.receipt"
                  label="Attach Receipt (Optional)"
                  accept="image/*,.pdf"
                  variant="outlined"
                  prepend-inner-icon="mdi-receipt"
                />
              </v-col>
            </v-row>

            <v-textarea
              v-model="expenseFormData.notes"
              label="Notes"
              placeholder="Additional details..."
              variant="outlined"
              rows="2"
            />
          </v-form>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="showExpenseDialog = false"
            >Cancel</v-btn
          >
          <v-btn
            color="#E07A5F"
            :disabled="!isValid"
            :loading="saving"
            @click="submitExpense"
            class="save-btn"
          >
            <v-icon start>mdi-plus</v-icon>
            Record Expense
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Expense Details Dialog -->
    <v-dialog v-model="showDetailsDialog" max-width="500">
      <v-card class="details-dialog">
        <v-card-title class="dialog-header">
          <span>Expense Details</span>
          <v-btn icon variant="text" @click="showDetailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text v-if="selectedExpense" class="dialog-content">
          <div class="detail-row">
            <span class="detail-label">Description</span>
            <span class="detail-value">{{ selectedExpense.description }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Amount</span>
            <span class="detail-value amount"
              >ksh{{ selectedExpense.amount.toFixed(2) }}</span
            >
          </div>
          <div class="detail-row">
            <span class="detail-label">Category</span>
            <span class="detail-value">
              <span
                class="category-badge"
                :style="{
                  background:
                    getCategoryColorByName(selectedExpense.category) + '20',
                  color: getCategoryColorByName(selectedExpense.category),
                }"
              >
                {{ formatCategoryName(selectedExpense.category) }}
              </span>
            </span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Payment Method</span>
            <span class="detail-value">
              <span
                class="payment-badge"
                :class="selectedExpense.payment_method"
              >
                {{ selectedExpense.payment_method }}
              </span>
            </span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Date</span>
            <span class="detail-value">{{
              formatDate(selectedExpense.date)
            }}</span>
          </div>
          <div v-if="selectedExpense.notes" class="detail-row">
            <span class="detail-label">Notes</span>
            <span class="detail-value">{{ selectedExpense.notes }}</span>
          </div>
          <div v-if="selectedExpense.receipt_url" class="detail-row">
            <span class="detail-label">Receipt</span>
            <a
              :href="selectedExpense.receipt_url"
              target="_blank"
              class="receipt-link"
            >
              <v-icon size="16">mdi-file-document</v-icon>
              View Receipt
            </a>
          </div>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="showDetailsDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card class="confirm-dialog">
        <div class="confirm-icon">
          <v-icon size="64" color="#E07A5F">mdi-alert-circle</v-icon>
        </div>
        <h3>Delete Expense?</h3>
        <p>
          Are you sure you want to delete this expense of
          <strong>ksh{{ selectedExpense?.amount?.toFixed(2) }}</strong
          >? This action cannot be undone.
        </p>
        <div class="confirm-actions">
          <v-btn variant="text" @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn color="#E07A5F" @click="confirmDelete">Delete</v-btn>
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
import { ref, computed, onMounted, watch, nextTick } from "vue";
import Chart from "chart.js/auto";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

// ===== STATE =====
const selectedPeriod = ref("month");
const customStartDate = ref("");
const customEndDate = ref("");
const chartView = ref("Line");
const tableSearch = ref("");
const categoryFilter = ref("");
const itemsPerPage = ref(10);
const currentPage = ref(1);
const showAllCategories = ref(false);
const showExpenseDialog = ref(false);
const showDetailsDialog = ref(false);
const showDeleteDialog = ref(false);
const selectedExpense = ref(null);
const isValid = ref(false);
const saving = ref(false);
const expenseForm = ref(null);

// Chart refs
const trendChart = ref(null);
const categoryChart = ref(null);
let trendChartInstance: Chart | null = null;
let categoryChartInstance: Chart | null = null;

// ===== EXPENSE DATA =====
const expenses = ref([]);
const expenseSummary = ref({
  total: 0,
  dailyAverage: 0,
  periodDays: 0,
  highestDay: null,
  count: 0,
  categoryBreakdown: [],
  dailyData: [],
});

// ===== EXPENSE CATEGORIES =====
const expenseCategories = [
  { title: "☕ Coffee Beans", value: "inventory" },
  { title: "🥛 Milk & Syrups", value: "inventory" },
  { title: "🧴 Supplies (Cups, Lids)", value: "supplies" },
  { title: "💡 Utilities", value: "utilities" },
  { title: "🏠 Rent", value: "rent" },
  { title: "👨‍🍳 Salaries", value: "salaries" },
  { title: "🔧 Maintenance", value: "maintenance" },
  { title: "📢 Marketing", value: "marketing" },
  { title: "📦 Other", value: "miscellaneous" },
];

const paymentMethods = [
  { title: "💵 Cash", value: "cash" },
  { title: "📱 M-Pesa", value: "mpesa" },
  { title: "🏦 Bank Transfer", value: "bank" },
];

const categoryColors: Record<string, string> = {
  inventory: "#2D6A4F",
  supplies: "#E07A5F",
  utilities: "#F4A261",
  rent: "#6B4E71",
  salaries: "#E9C46A",
  maintenance: "#4A90D9",
  marketing: "#E74C3C",
  miscellaneous: "#95A5A6",
};

const categoryFilterOptions = computed(() => {
  const options = [{ title: "All Categories", value: "" }];
  const uniqueCategories = [...new Set(expenses.value.map((e) => e.category))];
  uniqueCategories.forEach((cat) => {
    options.push({ title: formatCategoryName(cat), value: cat });
  });
  return options;
});

// ===== RULES =====
const rules = {
  required: (v: any) => !!v || "This field is required",
  positive: (v: number) => v > 0 || "Amount must be positive",
};

// ===== COMPUTED =====
const periodDays = computed(() => expenseSummary.value.periodDays || 0);
const totalExpenses = computed(() => expenseSummary.value.total || 0);
const dailyAverage = computed(() => expenseSummary.value.dailyAverage || 0);
const highestDay = computed(() => expenseSummary.value.highestDay);
const expenseCount = computed(() => expenseSummary.value.count || 0);
const categoryBreakdown = computed(
  () => expenseSummary.value.categoryBreakdown || []
);

// Filtered expenses
const filteredExpenses = computed(() => {
  let filtered = [...expenses.value];

  if (tableSearch.value) {
    filtered = filtered.filter(
      (e) =>
        e.description.toLowerCase().includes(tableSearch.value.toLowerCase()) ||
        e.category.toLowerCase().includes(tableSearch.value.toLowerCase())
    );
  }

  if (categoryFilter.value) {
    filtered = filtered.filter((e) => e.category === categoryFilter.value);
  }

  return filtered;
});

const paginatedExpenses = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredExpenses.value.slice(start, end);
});

const totalPages = computed(() =>
  Math.ceil(filteredExpenses.value.length / itemsPerPage.value)
);

const displayCategories = computed(() => {
  const categories = [...categoryBreakdown.value];
  if (showAllCategories.value) {
    return categories;
  }
  return categories.slice(0, 5);
});

// Trend data for chart
const trendData = computed(() => {
  const data = expenseSummary.value.dailyData || [];
  return {
    labels: data.map((d) => d.date),
    values: data.map((d) => d.amount),
  };
});

// Expense change calculations
const expenseChange = computed(() => {
  // Calculate change from previous period
  const currentTotal = totalExpenses.value;
  // This would need previous period data - simplified for demo
  return { percent: "+12.5%", isPositive: true };
});

const expenseChangeClass = computed(() =>
  expenseChange.value.isPositive ? "positive" : "negative"
);
const expenseChangeIcon = computed(() =>
  expenseChange.value.isPositive ? "mdi-arrow-up" : "mdi-arrow-down"
);
const expenseChangePercent = computed(() => expenseChange.value.percent);

// ===== FORM =====
const expenseFormData = ref({
  description: "",
  amount: "",
  category: "",
  paymentMethod: "",
  receipt: null,
  notes: "",
});

// ===== METHODS =====

// Fetch expenses
const fetchExpenses = async () => {
  try {
    const params = new URLSearchParams();

    if (selectedPeriod.value === "custom") {
      if (customStartDate.value)
        params.append("start_date", customStartDate.value);
      if (customEndDate.value) params.append("end_date", customEndDate.value);
    } else {
      // Add period logic
    }

    const response = await $fetch(
      `http://127.0.0.1:8000/expenses/?${params.toString()}`,

      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
        },
      }
    );
    expenses.value = response;
    calculateSummary();
  } catch (error) {
    console.error("Failed to fetch expenses:", error);
    showSnackbar("Failed to load expenses", "error");
  }
};

// Calculate expense summary
const calculateSummary = async () => {
  if (!expenses.value.length) {
    expenseSummary.value = {
      total: 0,
      dailyAverage: 0,
      periodDays: 0,
      highestDay: null,
      count: 0,
      categoryBreakdown: [],
      dailyData: [],
    };
    return;
  }

  // Total expenses
  const total = expenses.value.reduce((sum, e) => sum + e.amount, 0);

  // Category breakdown
  const categoryMap = new Map();
  expenses.value.forEach((e) => {
    if (!categoryMap.has(e.category)) {
      categoryMap.set(e.category, { amount: 0, count: 0 });
    }
    const data = categoryMap.get(e.category);
    data.amount += e.amount;
    data.count += 1;
  });

  const categoryBreakdown = Array.from(categoryMap.entries())
    .map(([name, data]) => ({
      name: formatCategoryName(name),
      amount: data.amount,
      count: data.count,
      percentage: (data.amount / total) * 100,
      color: categoryColors[name] || "#95A5A6",
    }))
    .sort((a, b) => b.amount - a.amount);

  // Daily data for chart
  const dailyMap = new Map();
  expenses.value.forEach((e) => {
    const date = new Date(e.date).toISOString().split("T")[0];
    if (!dailyMap.has(date)) {
      dailyMap.set(date, 0);
    }
    dailyMap.set(date, dailyMap.get(date) + e.amount);
  });

  const dailyData = Array.from(dailyMap.entries())
    .map(([date, amount]) => ({ date, amount }))
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  // Highest day
  const highestDay = dailyData.reduce(
    (max, d) => (d.amount > max.amount ? d : max),
    dailyData[0] || { amount: 0, date: null }
  );

  expenseSummary.value = {
    total,
    dailyAverage: dailyData.length > 0 ? total / dailyData.length : 0,
    periodDays: dailyData.length,
    highestDay: highestDay.amount > 0 ? highestDay : null,
    count: expenses.value.length,
    categoryBreakdown,
    dailyData,
  };

  // Update charts
  await updateCharts();
};

// ===== CHARTS =====
const updateCharts = async () => {
  await nextTick();

  // Trend Chart
  if (trendChartInstance) {
    trendChartInstance.destroy();
    trendChartInstance = null;
  }

  const trendCanvas = trendChart.value as HTMLCanvasElement;
  if (trendCanvas && trendData.value.labels.length > 0) {
    const trendCtx = trendCanvas.getContext("2d");
    if (trendCtx) {
      trendChartInstance = new Chart(trendCtx, {
        type: chartView.value.toLowerCase() as "line" | "bar",
        data: {
          labels: trendData.value.labels,
          datasets: [
            {
              label: "Daily Expenses",
              data: trendData.value.values,
              borderColor: "#E07A5F",
              backgroundColor:
                chartView.value === "Line"
                  ? "rgba(224, 122, 95, 0.1)"
                  : "#E07A5F",
              tension: 0.4,
              fill: chartView.value === "Line",
              borderRadius: chartView.value === "Bar" ? 4 : undefined,
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
                label: (context) => `ksh${Number(context.raw).toFixed(2)}`,
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: "#E5E7EB" },
              ticks: {
                callback: (value) => "ksh" + value,
              },
            },
            x: {
              grid: { display: false },
            },
          },
        },
      });
    }
  }

  // Category Chart
  if (categoryChartInstance) {
    categoryChartInstance.destroy();
    categoryChartInstance = null;
  }

  const categoryCanvas = categoryChart.value as HTMLCanvasElement;
  if (categoryCanvas && categoryBreakdown.value.length > 0) {
    const categoryCtx = categoryCanvas.getContext("2d");
    if (categoryCtx) {
      const colors = categoryBreakdown.value.map((c) => c.color);
      const data = categoryBreakdown.value.map((c) => c.amount);
      const labels = categoryBreakdown.value.map((c) => c.name);

      categoryChartInstance = new Chart(categoryCtx, {
        type: "doughnut",
        data: {
          labels,
          datasets: [
            {
              data,
              backgroundColor: colors,
              borderWidth: 2,
              borderColor: "white",
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
                  const label = context.label || "";
                  const value = Number(context.raw) || 0;
                  const total = (context.dataset.data as number[]).reduce(
                    (a, b) => a + b,
                    0
                  );
                  const percentage = ((value / total) * 100).toFixed(1);
                  return `${label}: ksh${value.toFixed(2)} (${percentage}%)`;
                },
              },
            },
          },
          cutout: "60%",
        },
      });
    }
  }
};
// ===== EXPENSE CRUD =====

const OpenExpeseDialog = () => {
  showExpenseDialog.value = true;
};
const submitExpense = async () => {
  if (!expenseForm.value) return;
  const { valid } = await expenseForm.value.validate();
  if (!valid) return;

  saving.value = true;
  try {
    const formData = new FormData();
    formData.append("description", expenseFormData.value.description);
    formData.append("amount", expenseFormData.value.amount);
    formData.append("category", expenseFormData.value.category);
    formData.append("payment_method", expenseFormData.value.payment_method);
    formData.append("notes", expenseFormData.value.notes || "");
    if (expenseFormData.value.receipt) {
      formData.append("receipt", expenseFormData.value.receipt);
    }
    console.log("Submitting expense:", {
      description: expenseFormData.value.description,
      amount: expenseFormData.value.amount,
      category: expenseFormData.value.category,
      payment_method: expenseFormData.value.payment_method,
      notes: expenseFormData.value.notes || "",
      receipt: expenseFormData.value.receipt,
    });

    await $fetch("http://127.0.0.1:8000/expenses/", {
      method: "POST",
      body: formData,
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
      },
    });

    showExpenseDialog.value = false;
    resetExpenseForm();
    await fetchExpenses();

    showSnackbar("Expense recorded successfully!", "success");
  } catch (error) {
    console.error("Failed to record expense:", error);
    showSnackbar("Failed to record expense", "error");
  } finally {
    saving.value = false;
  }
};

const resetExpenseForm = () => {
  expenseFormData.value = {
    description: "",
    amount: "",
    category: "",
    payment_method: "",
    receipt: null,
    notes: "",
  };
};

const viewExpenseDetails = (expense: any) => {
  selectedExpense.value = expense;
  showDetailsDialog.value = true;
};

const deleteExpense = (expense: any) => {
  selectedExpense.value = expense;
  showDeleteDialog.value = true;
};

const confirmDelete = async () => {
  if (!selectedExpense.value) return;

  try {
    await $fetch(`http://127.0.0.1:8000/expenses/${selectedExpense.value.id}`, {
      method: "DELETE",
    });

    showDeleteDialog.value = false;
    await fetchExpenses();

    showSnackbar("Expense deleted successfully!", "success");
  } catch (error) {
    console.error("Failed to delete expense:", error);
    showSnackbar("Failed to delete expense", "error");
  }
};

const exportExpenseReport = () => {
  const headers = [
    "Date",
    "Description",
    "Category",
    "Amount",
    "Payment Method",
    "Notes",
  ];
  const rows = expenses.value.map((e) => [
    new Date(e.date).toLocaleDateString(),
    e.description,
    formatCategoryName(e.category),
    e.amount,
    e.payment_method,
    e.notes || "",
  ]);

  let csv = headers.join(",") + "\n";
  rows.forEach((row) => {
    csv += row.join(",") + "\n";
  });

  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `expenses_${new Date().toISOString().split("T")[0]}.csv`;
  link.click();
  URL.revokeObjectURL(url);
};

// ===== HELPER FUNCTIONS =====
const formatDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("en-KE", {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

const formatCategoryName = (category: string) => {
  const map: Record<string, string> = {
    inventory: "☕ Inventory",
    supplies: "🧴 Supplies",
    utilities: "💡 Utilities",
    rent: "🏠 Rent",
    salaries: "👨‍🍳 Salaries",
    maintenance: "🔧 Maintenance",
    marketing: "📢 Marketing",
    miscellaneous: "📦 Other",
  };
  return map[category] || category;
};

const getCategoryColorByName = (category: string) => {
  return categoryColors[category] || "#95A5A6";
};

const getCategoryColor = (index: number) => {
  const colors = ["#2D6A4F", "#E07A5F", "#F4A261", "#6B4E71", "#E9C46A"];
  return colors[index % colors.length];
};

const getRankClass = (rank: number) => {
  if (rank === 1) return "gold";
  if (rank === 2) return "silver";
  if (rank === 3) return "bronze";
  return "";
};

const getSortIcon = (key: string) => {
  return "mdi-arrow-up-down";
};

const applyCustomRange = () => {
  if (customStartDate.value && customEndDate.value) {
    fetchExpenses();
  }
};

const showSnackbar = (text: string, color: string = "success") => {
  snackbar.value = {
    show: true,
    text,
    color,
    icon: color === "success" ? "mdi-check-circle" : "mdi-alert-circle",
  };
};

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

// ===== WATCHERS =====
watch(selectedPeriod, () => {
  fetchExpenses();
});

watch(chartView, () => {
  updateCharts();
});

// ===== SNACKBAR =====
const snackbar = ref({
  show: false,
  text: "",
  color: "success",
  icon: "mdi-check-circle",
});

// ===== ON MOUNT =====
onMounted(async () => {
  // Set default dates for custom range
  const today = new Date();
  const thirtyDaysAgo = new Date(today);
  thirtyDaysAgo.setDate(today.getDate() - 30);
  customStartDate.value = thirtyDaysAgo.toISOString().split("T")[0];
  customEndDate.value = today.toISOString().split("T")[0];

  await fetchExpenses();
});
</script>

<style scoped>
.expenses-dashboard {
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

.add-expense-btn {
  text-transform: none;
  border-radius: 40px;
}

.export-btn {
  border-color: #e5e7eb;
  border-radius: 40px;
  text-transform: none;
}

/* Period Selector */
.period-selector {
  background: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.period-toggle {
  width: 100%;
  border-radius: 12px !important;
}

.period-btn {
  flex: 1;
  text-transform: none;
  font-size: 14px;
  font-weight: 500;
}

.period-btn .v-icon {
  margin-right: 8px;
}

.custom-date-range {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
  flex-wrap: wrap;
}

.date-field {
  flex: 1;
  min-width: 150px;
}

.date-separator {
  color: #6b7280;
  font-weight: 500;
}

.apply-btn {
  border-radius: 40px;
  text-transform: none;
}

/* Summary Cards */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
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
  transition: all 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.card-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-content {
  flex: 1;
}

.card-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-value {
  font-size: 24px;
  font-weight: 800;
  color: #1b4332;
  margin: 4px 0;
}

.card-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.card-change.positive {
  color: #2d6a4f;
}

.card-change.negative {
  color: #e07a5f;
}

.card-sub {
  font-size: 12px;
  color: #6b7280;
}

/* Charts Row */
.charts-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
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
  align-items: center;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.chart-subtitle {
  font-size: 12px;
  color: #6b7280;
}

.chart-view-select {
  width: 120px;
}

.chart-container {
  height: 300px;
  position: relative;
}

.chart-container.small {
  height: 200px;
}

/* Category Legend */
.category-legend {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  background: #f8f6f2;
  border-radius: 8px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 4px;
}

.legend-name {
  flex: 1;
  font-size: 12px;
  font-weight: 500;
  color: #1b4332;
}

.legend-amount {
  font-size: 11px;
  font-weight: 600;
  color: #e07a5f;
}

.legend-percentage {
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
}

/* Categories Section */
.categories-section {
  margin-bottom: 24px;
}

.categories-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.card-subtitle {
  font-size: 12px;
  color: #6b7280;
}

.view-all-btn {
  text-transform: none;
  color: #e07a5f;
}

.categories-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: #f8f6f2;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.category-item:hover {
  background: #f0ede5;
}

.category-item.top-category {
  background: #fff8f0;
  border: 1px solid #e07a5f30;
}

.category-rank {
  min-width: 32px;
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

.category-info {
  flex: 1;
}

.category-name {
  font-weight: 600;
  color: #1b4332;
}

.category-transactions {
  font-size: 11px;
  color: #6b7280;
}

.category-amount {
  font-weight: 700;
  color: #e07a5f;
  min-width: 80px;
  text-align: right;
}

.category-progress {
  flex: 1;
  height: 4px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  min-width: 100px;
}

.progress-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 1s ease;
}

/* Expenses Table */
.expenses-table-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.table-controls {
  display: flex;
  gap: 12px;
}

.search-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8f6f2;
  padding: 4px 12px;
  border-radius: 8px;
}

.table-search {
  border: none;
  background: transparent;
  outline: none;
  font-size: 13px;
  padding: 6px 0;
}

.category-filter {
  width: 180px;
}

.table-container {
  overflow-x: auto;
  margin-top: 16px;
}

.expenses-table {
  width: 100%;
  border-collapse: collapse;
}

.expenses-table th {
  text-align: left;
  padding: 12px 16px;
  background: #f8f6f2;
  font-weight: 600;
  color: #1b4332;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.expenses-table th:hover {
  background: #ede8df;
}

.expenses-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  color: #4b5563;
}

.date-cell {
  font-weight: 500;
  color: #1b4332;
  white-space: nowrap;
}

.desc-cell {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.amount-cell {
  font-weight: 700;
  color: #e07a5f;
}

.category-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
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

.payment-badge.bank {
  background: #4a90d920;
  color: #4a90d9;
}

.action-buttons {
  display: flex;
  gap: 4px;
}

/* Pagination */
.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
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

/* Dialog Styles */
.expense-dialog {
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

.dialog-actions {
  padding: 16px 24px 24px;
  gap: 12px;
}

.save-btn {
  border-radius: 40px;
  text-transform: none;
}

.details-dialog {
  border-radius: 32px !important;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.detail-label {
  font-weight: 500;
  color: #6b7280;
}

.detail-value {
  font-weight: 600;
  color: #1b4332;
}

.detail-value.amount {
  color: #e07a5f;
}

.receipt-link {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #2d6a4f;
  text-decoration: none;
}

.receipt-link:hover {
  text-decoration: underline;
}

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

/* Snackbar */
.custom-snackbar :deep(.v-snackbar__content) {
  font-weight: 500;
}

/* Responsive */
@media (max-width: 1200px) {
  .summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .category-legend {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .expenses-dashboard {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    flex-direction: column;
  }

  .header-actions .v-btn {
    width: 100%;
    justify-content: center;
  }

  .period-btn {
    font-size: 11px;
    padding: 4px 8px;
  }

  .period-btn .v-icon {
    margin-right: 4px;
    font-size: 14px;
  }

  .summary-grid {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .summary-card {
    padding: 16px;
  }

  .card-value {
    font-size: 18px;
  }

  .card-icon {
    width: 40px;
    height: 40px;
  }

  .custom-date-range {
    flex-direction: column;
    gap: 12px;
  }

  .date-field {
    width: 100%;
  }

  .date-separator {
    text-align: center;
  }

  .apply-btn {
    width: 100%;
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 250px;
  }

  .category-legend {
    grid-template-columns: 1fr;
  }

  .categories-grid {
    gap: 8px;
  }

  .category-item {
    flex-wrap: wrap;
    gap: 8px;
  }

  .category-rank {
    min-width: 24px;
  }

  .rank-badge {
    width: 24px;
    height: 24px;
    font-size: 10px;
  }

  .category-amount {
    min-width: 60px;
    font-size: 14px;
  }

  .category-progress {
    flex-basis: 100%;
    min-width: unset;
  }

  .table-controls {
    flex-direction: column;
  }

  .category-filter {
    width: 100%;
  }

  .pagination-section {
    flex-direction: column;
    gap: 12px;
  }

  .expenses-table th,
  .expenses-table td {
    padding: 8px 10px;
    font-size: 12px;
  }

  .desc-cell {
    max-width: 120px;
  }

  .dialog-header {
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }

  .period-toggle {
    flex-direction: column;
  }

  .period-btn {
    width: 100%;
  }

  .expenses-table th,
  .expenses-table td {
    padding: 6px 8px;
    font-size: 11px;
  }

  .amount-cell {
    font-size: 13px;
  }
}
</style>
