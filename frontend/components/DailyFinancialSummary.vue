<!-- frontend/components/DailyFinancialSummary.vue -->
<template>
  <v-card class="financial-summary-card" elevation="0">
    <div class="card-header">
      <div>
        <div class="card-title">📊 Daily Financial Summary</div>
        <div class="card-subtitle">{{ todayDate }}</div>
      </div>
      <div class="header-actions">
        <v-btn size="small" variant="text" @click="showExpenseDialog = true">
          <v-icon start size="16">mdi-plus</v-icon>
          Add Expense
        </v-btn>
        <v-btn size="small" variant="text" @click="refreshData">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </div>
    </div>

    <div class="summary-grid">
      <!-- Revenue Card -->
      <div class="summary-card revenue">
        <div class="summary-card-header">
          <v-icon>mdi-currency-usd</v-icon>
          <span>Revenue</span>
        </div>
        <div class="summary-amount">
          ksh{{ summary.totalRevenue.toFixed(2) }}
        </div>
        <div class="summary-breakdown">
          <div class="breakdown-item">
            <span>Cash</span>
            <span>ksh{{ summary.cashRevenue.toFixed(2) }}</span>
          </div>
          <div class="breakdown-item">
            <span>M-Pesa</span>
            <span>ksh{{ summary.mpesaRevenue.toFixed(2) }}</span>
          </div>
          <div class="breakdown-item debt">
            <span>📋 Debt</span>
            <span>ksh{{ summary.debtRevenue.toFixed(2) }}</span>
          </div>
        </div>
        <div class="summary-orders">{{ summary.totalOrders }} orders today</div>
      </div>

      <!-- Expenses Card -->
      <div class="summary-card expenses">
        <div class="summary-card-header">
          <v-icon>mdi-cash-minus</v-icon>
          <span>Expenses</span>
        </div>
        <div class="summary-amount">
          ksh{{ summary.totalExpenses.toFixed(2) }}
        </div>
        <div class="summary-breakdown">
          <div
            v-for="(amount, category) in summary.expensesByCategory"
            :key="category"
            class="breakdown-item"
          >
            <span>{{ formatCategory(category) }}</span>
            <span>ksh{{ amount.toFixed(2) }}</span>
          </div>
        </div>
        <div class="summary-orders">
          {{ summary.expenseCount }} expenses recorded
        </div>
      </div>

      <!-- Profit Card -->
      <div class="summary-card profit">
        <div class="summary-card-header">
          <v-icon>mdi-chart-line</v-icon>
          <span>Net Profit</span>
        </div>
        <div
          class="summary-amount"
          :class="{
            positive: summary.netProfit > 0,
            negative: summary.netProfit < 0,
          }"
        >
          ksh{{ summary.netProfit.toFixed(2) }}
        </div>
        <div class="summary-breakdown">
          <div class="breakdown-item">
            <span>Profit Margin</span>
            <span>{{ summary.profitMargin.toFixed(1) }}%</span>
          </div>
          <div class="breakdown-item">
            <span>Cash Flow</span>
            <span>ksh{{ summary.cashFlow.toFixed(2) }}</span>
          </div>
        </div>
        <div class="summary-orders">
          {{ summary.netProfit > 0 ? "📈 Profitable day" : "📉 Loss day" }}
        </div>
      </div>

      <!-- Debt Card -->
      <div class="summary-card debt">
        <div class="summary-card-header">
          <v-icon>mdi-account-cash</v-icon>
          <span>Debt Overview</span>
        </div>
        <div class="summary-amount debt-amount">
          ksh{{ summary.totalDebtOutstanding.toFixed(2) }}
        </div>
        <div class="summary-breakdown">
          <div class="breakdown-item">
            <span>🆕 New Debts</span>
            <span>{{ summary.newDebtsToday }}</span>
          </div>
          <div class="breakdown-item paid">
            <span>✅ Cleared Today</span>
            <span>ksh{{ summary.debtsClearedToday.toFixed(2) }}</span>
          </div>
        </div>
        <div class="summary-orders">
          {{ summary.debtCustomers }} customers with debt
        </div>
      </div>
    </div>

    <!-- Debt Orders List -->
    <div v-if="summary.debtOrders.length > 0" class="debt-list-section">
      <div class="section-header">
        <span>📋 Pending Debt Orders</span>
        <v-btn size="small" variant="text" to="/orders">View All</v-btn>
      </div>
      <div class="debt-items">
        <div
          v-for="debt in summary.debtOrders.slice(0, 5)"
          :key="debt.id"
          class="debt-item"
        >
          <div class="debt-info">
            <div class="debt-customer">{{ debt.customerName }}</div>
            <div class="debt-receipt">{{ debt.receiptNumber }}</div>
          </div>
          <div class="debt-amount">ksh{{ debt.total.toFixed(2) }}</div>
          <div class="debt-age">{{ getDaysAgo(debt.created_at) }} days</div>
          <v-btn size="x-small" color="#2D6A4F" @click="markDebtPaid(debt)">
            Mark Paid
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Expense Tracker Dialog -->
    <ExpenseTracker
      v-model="showExpenseDialog"
      @expense-recorded="refreshData"
    />
  </v-card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import ExpenseTracker from "./ExpenseTracker.vue";
import { useAuthStore } from "@/stores/auth";
import { usePosStore } from "@/stores/pos";

const props = defineProps({
  date: {
    type: String,
    default: () => new Date().toISOString().split("T")[0],
  },
});

const posStore = usePosStore();
const showExpenseDialog = ref(false);
const loading = ref(false);
const summary = ref({
  totalRevenue: 0,
  cashRevenue: 0,
  mpesaRevenue: 0,
  debtRevenue: 0,
  totalExpenses: 0,
  expensesByCategory: {},
  expenseCount: 0,
  netProfit: 0,
  profitMargin: 0,
  cashFlow: 0,
  totalOrders: 0,
  totalDebtOutstanding: 0,
  newDebtsToday: 0,
  debtsClearedToday: 0,
  debtCustomers: 0,
  debtOrders: [],
});

const todayDate = computed(() => {
  return new Date().toLocaleDateString("en-KE", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });
});

const refreshData = async () => {
  loading.value = true;

  try {
    // Fetch financial summary from API
    const authStore = useAuthStore();
    const response = await fetch(
      `http://127.0.0.1:8000/reports/daily/${props.date}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authStore.token}`,
        },
      }
    );

    summary.value = await response.json();
    console.log("Financial summary fetched:", summary.value);
  } catch (error) {
    console.error("Failed to fetch financial summary:", error);
  } finally {
    loading.value = false;
  }
};

const formatCategory = (category: string) => {
  const map = {
    inventory: "☕ Inventory",
    supplies: "🧴 Supplies",
    utilities: "💡 Utilities",
    rent: "🏠 Rent",
    salaries: "👨‍🍳 Salaries",
    maintenance: "🔧 Maintenance",
    marketing: "📢 Marketing",
    miscellaneous: "📦 Other",
  };
  return map[category as keyof typeof map] || category;
};

const getDaysAgo = (date: string) => {
  const days = Math.floor(
    (Date.now() - new Date(date).getTime()) / (1000 * 60 * 60 * 24)
  );
  return days;
};

const markDebtPaid = async (debt: any) => {
  try {
    const debtId = debt.id;
    await posStore.updateDebtOrderStatus(debtId);

    // Refresh the summary data after marking debt as paid
    await refreshData();
  } catch (error) {
    console.error("Failed to mark debt as paid:", error);
  }
};

onMounted(() => {
  refreshData();
});
</script>

<style scoped>
.financial-summary-card {
  border-radius: 24px;
  padding: 24px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-title {
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
}

.card-subtitle {
  font-size: 13px;
  color: #6b7280;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.summary-card {
  padding: 20px;
  border-radius: 20px;
  background: #f8f6f2;
}

.summary-card.revenue {
  background: linear-gradient(135deg, #f0f9f4, #e8f5e9);
}

.summary-card.expenses {
  background: linear-gradient(135deg, #fff3e0, #ffe8cc);
}

.summary-card.profit {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
}

.summary-card.debt {
  background: linear-gradient(135deg, #fce4ec, #f8bbd0);
}

.summary-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 12px;
}

.summary-amount {
  font-size: 28px;
  font-weight: 800;
  color: #1b4332;
  margin-bottom: 8px;
}

.summary-amount.positive {
  color: #2d6a4f;
}

.summary-amount.negative {
  color: #e07a5f;
}

.summary-amount.debt-amount {
  color: #e07a5f;
}

.summary-breakdown {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #6b7280;
}

.breakdown-item.debt {
  color: #e07a5f;
}

.breakdown-item.paid {
  color: #2d6a4f;
}

.summary-orders {
  font-size: 11px;
  color: #9ca3af;
  padding-top: 8px;
  border-top: 1px solid #e5e7eb;
}

.debt-list-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 2px solid #f3f4f6;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-header span {
  font-weight: 600;
  color: #1b4332;
}

.debt-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.debt-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: #fff8f0;
  border-radius: 12px;
  border-left: 3px solid #e07a5f;
}

.debt-info {
  flex: 1;
}

.debt-customer {
  font-weight: 600;
  color: #1b4332;
}

.debt-receipt {
  font-size: 11px;
  color: #6b7280;
}

.debt-amount {
  font-weight: 700;
  color: #e07a5f;
}

.debt-age {
  font-size: 11px;
  color: #6b7280;
}

@media (max-width: 1200px) {
  .summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>
