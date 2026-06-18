<!-- frontend/components/ExpenseTracker.vue -->
<template>
  <v-dialog v-model="dialog" max-width="600" transition="dialog-transition">
    <v-card class="expense-dialog">
      <v-card-title class="dialog-header">
        <div class="title-content">
          <v-icon size="28" color="#E07A5F" class="mr-3">mdi-cash-minus</v-icon>
          <span>Record Expense</span>
        </div>
        <v-btn icon variant="text" @click="dialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="dialog-content">
        <v-form ref="formRef" v-model="isValid">
          <v-row>
            <v-col cols="12" md="8">
              <v-text-field
                v-model="expense.description"
                label="Expense Description"
                placeholder="e.g., Coffee beans purchase"
                variant="outlined"
                :rules="[rules.required]"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="expense.amount"
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
                v-model="expense.category"
                label="Category"
                :items="expenseCategories"
                variant="outlined"
                :rules="[rules.required]"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                v-model="expense.paymentMethod"
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
                v-model="expense.receipt"
                label="Attach Receipt (Optional)"
                accept="image/*,.pdf"
                variant="outlined"
                prepend-inner-icon="mdi-receipt"
              />
            </v-col>
          </v-row>

          <v-textarea
            v-model="expense.notes"
            label="Notes"
            placeholder="Additional details..."
            variant="outlined"
            rows="2"
          />
        </v-form>
      </v-card-text>

      <v-card-actions class="dialog-actions">
        <v-btn variant="text" @click="dialog = false">Cancel</v-btn>
        <v-btn
          color="#E07A5F"
          :disabled="!isValid"
          @click="submitExpense"
          class="save-btn"
        >
          <v-icon start>mdi-plus</v-icon>
          Record Expense
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

const props = defineProps({
  modelValue: Boolean,
  onExpenseRecorded: Function,
});

const emit = defineEmits(["update:modelValue", "expense-recorded"]);

const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const expense = ref({
  description: "",
  amount: "",
  category: "",
  paymentMethod: "",
  receipt: null,
  notes: "",
});

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

const rules = {
  required: (v: any) => !!v || "This field is required",
  positive: (v: number) => v > 0 || "Amount must be positive",
};

const isValid = ref(false);
const formRef = ref(null);

const submitExpense = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  // Submit expense
  await props.onExpenseRecorded?.(expense.value);

  // Reset form
  expense.value = {
    description: "",
    amount: "",
    category: "",
    paymentMethod: "",
    receipt: null,
    notes: "",
  };

  dialog.value = false;
};
</script>

<style scoped>
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
</style>
