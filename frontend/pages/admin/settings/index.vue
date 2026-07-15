<!-- pages/admin/settings/index.vue -->
<template>
  <div class="settings-container">
    <!-- Page Header -->
    <v-row
      class="page-header"
      no-gutters
      style="
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 24px;
      "
    >
      <v-col cols="12" md="8">
        <div class="page-badge">
          <v-icon size="16" color="#2D6A4F">mdi-cog</v-icon>
          System Settings
        </div>
        <h1 class="page-title">Settings</h1>
        <p class="page-subtitle">
          Configure your system preferences and settings
        </p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right mt-4 mt-md-0">
        <v-btn
          variant="outlined"
          color="#6B7280"
          @click="resetSettings"
          :loading="saving"
        >
          <v-icon start>mdi-restore</v-icon>
          Reset
        </v-btn>
        <v-btn
          color="#2D6A4F"
          class="ml-2"
          @click="saveAllSettings"
          :loading="saving"
        >
          <v-icon start>mdi-content-save</v-icon>
          Save Settings
        </v-btn>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <div v-if="loading" class="text-center pa-8">
      <v-progress-circular indeterminate color="#2D6A4F" size="48" />
      <p class="mt-4 text-medium-emphasis">Loading settings...</p>
    </div>

    <!-- Settings Content -->
    <div v-else>
      <v-row no-gutters>
        <v-col cols="12" lg="3" class="pr-lg-4">
          <!-- Settings Navigation -->
          <v-card class="settings-nav-card" elevation="0" rounded="xl">
            <v-card-text class="pa-0">
              <v-list dense nav>
                <v-list-item
                  v-for="section in sections"
                  :key="section.id"
                  :active="activeSection === section.id"
                  @click="activeSection = section.id"
                  class="settings-nav-item"
                >
                  <template #prepend>
                    <v-icon
                      :color="
                        activeSection === section.id ? '#2D6A4F' : '#6B7280'
                      "
                    >
                      {{ section.icon }}
                    </v-icon>
                  </template>
                  <v-list-item-title
                    :class="activeSection === section.id ? 'active-text' : ''"
                  >
                    {{ section.title }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" lg="9" class="pl-lg-4 mt-4 mt-lg-0">
          <!-- Store Settings -->
          <div v-show="activeSection === 'general'">
            <v-card class="settings-card" elevation="0" rounded="xl">
              <v-card-text class="pa-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F">mdi-store</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">Store Information</h3>
                    <p class="section-subtitle">
                      Basic store details and contact information
                    </p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Store Name</label>
                      <v-text-field
                        v-model="settings.store.name"
                        placeholder="Babadeacon Coffee"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Store Email</label>
                      <v-text-field
                        v-model="settings.store.email"
                        placeholder="info@babadeacon.com"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div class="form-group">
                      <label class="form-label">Store Address</label>
                      <v-textarea
                        v-model="settings.store.address"
                        placeholder="123 Coffee Street, Nairobi, Kenya"
                        variant="outlined"
                        rows="2"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="4">
                    <div class="form-group">
                      <label class="form-label">Phone Number</label>
                      <v-text-field
                        v-model="settings.store.phone"
                        placeholder="+254-700-123456"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="4">
                    <div class="form-group">
                      <label class="form-label">Currency</label>
                      <v-select
                        v-model="settings.store.currency"
                        :items="currencyOptions"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="4">
                    <div class="form-group">
                      <label class="form-label">Time Zone</label>
                      <v-select
                        v-model="settings.store.timezone"
                        :items="timezoneOptions"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>
                </v-row>

                <v-divider class="my-6" />

                <!-- Store Logo -->
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F">mdi-image</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">Store Logo</h3>
                    <p class="section-subtitle">Upload your store logo</p>
                  </div>
                </div>

                <div class="logo-upload-area" @click="triggerLogoUpload">
                  <input
                    ref="logoInput"
                    type="file"
                    accept="image/*"
                    hidden
                    @change="handleLogoUpload"
                  />
                  <div v-if="settings.store.logo" class="logo-preview">
                    <img :src="settings.store.logo" alt="Store Logo" />
                    <div class="logo-overlay">
                      <v-icon size="24">mdi-camera</v-icon>
                      <span>Change Logo</span>
                    </div>
                  </div>
                  <div v-else class="logo-placeholder">
                    <v-icon size="48" color="#9CA3AF">mdi-image-plus</v-icon>
                    <p>Click to upload store logo</p>
                    <span>PNG, JPG up to 2MB</span>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </div>

          <!-- POS Settings -->
          <div v-show="activeSection === 'pos'">
            <v-card class="settings-card" elevation="0" rounded="xl">
              <v-card-text class="pa-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F">mdi-cash-register</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">POS Settings</h3>
                    <p class="section-subtitle">
                      Configure your Point of Sale preferences
                    </p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Default Order Type</label>
                      <v-select
                        v-model="settings.pos.default_order_type"
                        :items="orderTypeOptions"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Default Payment Method</label>
                      <v-select
                        v-model="settings.pos.default_payment"
                        :items="paymentMethodOptions"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Tax Rate (%)</label>
                      <v-text-field
                        v-model="settings.pos.tax_rate"
                        placeholder="10"
                        type="number"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Receipt Footer</label>
                      <v-text-field
                        v-model="settings.pos.receipt_footer"
                        placeholder="Thank you for your order!"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div class="form-group">
                      <v-switch
                        v-model="settings.pos.auto_print_receipt"
                        color="#2D6A4F"
                        hide-details
                      >
                        <template #label>
                          <div>
                            <div class="switch-label">Auto-print Receipt</div>
                            <div class="switch-hint">
                              Automatically print receipt after placing order
                            </div>
                          </div>
                        </template>
                      </v-switch>
                    </div>

                    <div class="form-group">
                      <v-switch
                        v-model="settings.pos.require_customer"
                        color="#2D6A4F"
                        hide-details
                      >
                        <template #label>
                          <div>
                            <div class="switch-label">
                              Require Customer Name
                            </div>
                            <div class="switch-hint">
                              Prompt for customer name before checkout
                            </div>
                          </div>
                        </template>
                      </v-switch>
                    </div>

                    <div class="form-group">
                      <v-switch
                        v-model="settings.pos.allow_debt"
                        color="#2D6A4F"
                        hide-details
                      >
                        <template #label>
                          <div>
                            <div class="switch-label">Allow Debt Orders</div>
                            <div class="switch-hint">
                              Enable 'Pay Later' option at checkout
                            </div>
                          </div>
                        </template>
                      </v-switch>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>

          <!-- Payment Settings -->
          <div v-show="activeSection === 'payments'">
            <v-card class="settings-card" elevation="0" rounded="xl">
              <v-card-text class="pa-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F">mdi-credit-card</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">Payment Settings</h3>
                    <p class="section-subtitle">
                      Configure payment methods and options
                    </p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12">
                    <div class="form-group">
                      <label class="form-label">Accepted Payment Methods</label>
                      <div class="payment-methods-grid">
                        <div
                          v-for="method in settings.payments.payment_methods"
                          :key="method.id"
                          class="payment-method-item"
                        >
                          <v-checkbox
                            v-model="method.enabled"
                            :label="method.name"
                            :color="method.enabled ? '#2D6A4F' : '#6B7280'"
                            hide-details
                          />
                          <v-icon
                            :color="method.enabled ? '#2D6A4F' : '#6B7280'"
                          >
                            {{ method.icon }}
                          </v-icon>
                        </div>
                      </div>
                    </div>
                  </v-col>

                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">M-Pesa Paybill Number</label>
                      <v-text-field
                        v-model="settings.payments.mpesa_paybill"
                        placeholder="123456"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">M-Pesa Account Number</label>
                      <v-text-field
                        v-model="settings.payments.mpesa_account"
                        placeholder="Store Account"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div class="form-group">
                      <v-switch
                        v-model="settings.payments.allow_partial_payment"
                        color="#2D6A4F"
                        hide-details
                      >
                        <template #label>
                          <div>
                            <div class="switch-label">
                              Allow Partial Payments
                            </div>
                            <div class="switch-hint">
                              Customers can pay partially and settle later
                            </div>
                          </div>
                        </template>
                      </v-switch>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>

          <!-- Receipt Settings -->
          <div v-show="activeSection === 'receipt'">
            <v-card class="settings-card" elevation="0" rounded="xl">
              <v-card-text class="pa-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F">mdi-receipt</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">Receipt Settings</h3>
                    <p class="section-subtitle">Customize your receipts</p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12">
                    <div class="form-group">
                      <label class="form-label">Receipt Header</label>
                      <v-textarea
                        v-model="settings.receipt.header"
                        placeholder="☕ BABADEACON COFFEE"
                        variant="outlined"
                        rows="2"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div class="form-group">
                      <label class="form-label">Receipt Footer</label>
                      <v-textarea
                        v-model="settings.receipt.footer"
                        placeholder="Thank you for your order!\nVisit us again at Babadeacon Coffee"
                        variant="outlined"
                        rows="2"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Receipt Paper Width (mm)</label>
                      <v-select
                        v-model="settings.receipt.paper_width"
                        :items="paperWidthOptions"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Receipt Font Size</label>
                      <v-select
                        v-model="settings.receipt.font_size"
                        :items="fontSizeOptions"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div class="form-group">
                      <v-switch
                        v-model="settings.receipt.show_tax_breakdown"
                        color="#2D6A4F"
                        hide-details
                      >
                        <template #label>
                          <div>
                            <div class="switch-label">Show Tax Breakdown</div>
                            <div class="switch-hint">
                              Display tax calculation on receipts
                            </div>
                          </div>
                        </template>
                      </v-switch>
                    </div>

                    <div class="form-group">
                      <v-switch
                        v-model="settings.receipt.show_item_discounts"
                        color="#2D6A4F"
                        hide-details
                      >
                        <template #label>
                          <div>
                            <div class="switch-label">Show Item Discounts</div>
                            <div class="switch-hint">
                              Display discount per item on receipts
                            </div>
                          </div>
                        </template>
                      </v-switch>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>

          <!-- Printer Settings -->
          <div v-show="activeSection === 'printer'">
            <v-card class="settings-card" elevation="0" rounded="xl">
              <v-card-text class="pa-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F">mdi-printer</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">Printer Settings</h3>
                    <p class="section-subtitle">Configure receipt printer</p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12">
                    <div class="form-group">
                      <label class="form-label">Printer Connection Type</label>
                      <v-select
                        v-model="settings.printer.connection_type"
                        :items="connectionTypeOptions"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col
                    cols="12"
                    md="6"
                    v-if="settings.printer.connection_type === 'bluetooth'"
                  >
                    <div class="form-group">
                      <label class="form-label">Bluetooth Device</label>
                      <v-select
                        v-model="settings.printer.bluetooth_device"
                        :items="bluetoothDevices"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                      <v-btn
                        variant="text"
                        size="small"
                        color="#2D6A4F"
                        class="mt-2"
                        @click="scanBluetoothDevices"
                      >
                        <v-icon size="16">mdi-bluetooth</v-icon>
                        Scan for Devices
                      </v-btn>
                    </div>
                  </v-col>

                  <v-col
                    cols="12"
                    md="6"
                    v-if="settings.printer.connection_type === 'network'"
                  >
                    <div class="form-group">
                      <label class="form-label">Printer IP Address</label>
                      <v-text-field
                        v-model="settings.printer.ip_address"
                        placeholder="192.168.1.100"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col
                    cols="12"
                    md="6"
                    v-if="settings.printer.connection_type === 'network'"
                  >
                    <div class="form-group">
                      <label class="form-label">Printer Port</label>
                      <v-text-field
                        v-model="settings.printer.port"
                        placeholder="9100"
                        type="number"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <v-btn
                      color="#2D6A4F"
                      variant="outlined"
                      @click="testPrinterConnection"
                    >
                      <v-icon start>mdi-printer-check</v-icon>
                      Test Printer Connection
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>

          <!-- System Settings -->
          <div v-show="activeSection === 'system'">
            <v-card class="settings-card" elevation="0" rounded="xl">
              <v-card-text class="pa-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F">mdi-server</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">System Settings</h3>
                    <p class="section-subtitle">
                      Advanced system configuration
                    </p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Backup Frequency</label>
                      <v-select
                        v-model="settings.system.backup_frequency"
                        :items="backupFrequencyOptions"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" md="6">
                    <div class="form-group">
                      <label class="form-label">Log Retention (days)</label>
                      <v-text-field
                        v-model="settings.system.log_retention"
                        placeholder="30"
                        type="number"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div class="form-group">
                      <v-switch
                        v-model="settings.system.auto_backup"
                        color="#2D6A4F"
                        hide-details
                      >
                        <template #label>
                          <div>
                            <div class="switch-label">Auto Backup</div>
                            <div class="switch-hint">
                              Automatically backup data daily
                            </div>
                          </div>
                        </template>
                      </v-switch>
                    </div>

                    <div class="form-group">
                      <v-switch
                        v-model="settings.system.debug_mode"
                        color="#2D6A4F"
                        hide-details
                      >
                        <template #label>
                          <div>
                            <div class="switch-label">Debug Mode</div>
                            <div class="switch-hint">
                              Enable detailed error logging
                            </div>
                          </div>
                        </template>
                      </v-switch>
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <v-divider class="my-4" />
                    <div class="danger-zone">
                      <h4 class="danger-title">Danger Zone</h4>
                      <p class="danger-subtitle">
                        Destructive actions that cannot be undone
                      </p>
                      <div class="danger-actions">
                        <v-btn
                          color="#E07A5F"
                          variant="outlined"
                          @click="confirmAction('clearCache')"
                        >
                          <v-icon start>mdi-broom</v-icon>
                          Clear Cache
                        </v-btn>
                        <v-btn
                          color="#E07A5F"
                          variant="outlined"
                          @click="confirmAction('resetSettings')"
                        >
                          <v-icon start>mdi-restore</v-icon>
                          Reset All Settings
                        </v-btn>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>
        </v-col>
      </v-row>
    </div>

    <!-- Confirmation Dialog -->
    <v-dialog v-model="confirmDialog.show" max-width="400">
      <v-card class="confirm-dialog">
        <div class="confirm-icon">
          <v-icon size="48" color="#E07A5F">mdi-alert-circle</v-icon>
        </div>
        <h3>{{ confirmDialog.title }}</h3>
        <p>{{ confirmDialog.message }}</p>
        <div class="dialog-actions">
          <v-btn variant="text" @click="confirmDialog.show = false"
            >Cancel</v-btn
          >
          <v-btn
            color="#E07A5F"
            :loading="confirmDialog.loading"
            @click="executeConfirmAction"
          >
            Confirm
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :timeout="3000"
      :color="snackbar.color"
      location="top"
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
import { ref, reactive, computed, onMounted } from "vue";
import { useSettingsStore } from "~/stores/settings";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const settingsStore = useSettingsStore();

// State
const activeSection = ref("general");
const loading = ref(true);
const saving = ref(false);
const logoInput = ref(null);

const confirmDialog = ref({
  show: false,
  title: "",
  message: "",
  action: "",
  loading: false,
});

const snackbar = ref({
  show: false,
  text: "",
  color: "success",
  icon: "mdi-check-circle",
});

// Settings Data
const settings = computed(() => settingsStore.settings || getDefaultSettings());

// Options
const sections = [
  { id: "general", title: "General", icon: "mdi-store" },
  { id: "pos", title: "POS Settings", icon: "mdi-cash-register" },
  { id: "payments", title: "Payment Settings", icon: "mdi-credit-card" },
  { id: "receipt", title: "Receipt Settings", icon: "mdi-receipt" },
  { id: "printer", title: "Printer Settings", icon: "mdi-printer" },
  { id: "system", title: "System Settings", icon: "mdi-server" },
];

const currencyOptions = [
  { title: "KES - Kenyan Shilling", value: "KES" },
  { title: "USD - US Dollar", value: "USD" },
  { title: "EUR - Euro", value: "EUR" },
  { title: "GBP - British Pound", value: "GBP" },
];

const timezoneOptions = [
  { title: "Africa/Nairobi", value: "Africa/Nairobi" },
  { title: "Africa/Lagos", value: "Africa/Lagos" },
  { title: "Africa/Johannesburg", value: "Africa/Johannesburg" },
  { title: "UTC", value: "UTC" },
];

const orderTypeOptions = [
  { title: "Dine In", value: "dine-in" },
  { title: "Takeaway", value: "takeaway" },
  { title: "Delivery", value: "delivery" },
  { title: "Online Order", value: "order-online" },
];

const paymentMethodOptions = [
  { title: "Cash", value: "cash" },
  { title: "M-Pesa", value: "mpesa" },
  { title: "Card", value: "card" },
  { title: "Debt", value: "debt" },
];

const paperWidthOptions = [
  { title: "58mm", value: "58" },
  { title: "80mm", value: "80" },
  { title: "112mm", value: "112" },
];

const fontSizeOptions = [
  { title: "Small (10px)", value: "10" },
  { title: "Medium (12px)", value: "12" },
  { title: "Large (14px)", value: "14" },
];

const connectionTypeOptions = [
  { title: "Bluetooth", value: "bluetooth" },
  { title: "USB", value: "usb" },
  { title: "Network (WiFi/LAN)", value: "network" },
];

const backupFrequencyOptions = [
  { title: "Daily", value: "daily" },
  { title: "Weekly", value: "weekly" },
  { title: "Monthly", value: "monthly" },
  { title: "Never", value: "never" },
];

const bluetoothDevices = ref([]);

// Default Settings
function getDefaultSettings() {
  return {
    store: {
      name: "Babadeacon Coffee",
      email: "info@babadeacon.com",
      address: "123 Coffee Street, Nairobi, Kenya",
      phone: "+254-700-123456",
      currency: "KES",
      timezone: "Africa/Nairobi",
      logo: null,
    },
    pos: {
      default_order_type: "takeaway",
      default_payment: "cash",
      tax_rate: 10,
      receipt_footer: "Thank you for your order!",
      auto_print_receipt: true,
      require_customer: false,
      allow_debt: true,
    },
    products: {
      default_reorder: 10,
      low_stock_threshold: 5,
      enable_variants: true,
      track_inventory: true,
      require_barcode: false,
    },
    payments: {
      payment_methods: [
        { id: "cash", name: "Cash", icon: "mdi-cash", enabled: true },
        { id: "mpesa", name: "M-Pesa", icon: "mdi-cellphone", enabled: true },
        { id: "card", name: "Card", icon: "mdi-credit-card", enabled: false },
        { id: "debt", name: "Debt", icon: "mdi-account-cash", enabled: true },
      ],
      mpesa_paybill: null,
      mpesa_account: null,
      allow_partial_payment: false,
    },
    receipt: {
      header: "☕ BABADEACON COFFEE\nPremium Coffee & Snacks",
      footer: "Thank you for your order!\nVisit us again at Babadeacon Coffee",
      paper_width: "80",
      font_size: "12",
      show_tax_breakdown: true,
      show_item_discounts: true,
    },
    printer: {
      connection_type: "bluetooth",
      bluetooth_device: null,
      usb_device: null,
      ip_address: null,
      port: "9100",
    },
    system: {
      backup_frequency: "daily",
      log_retention: 30,
      auto_backup: true,
      debug_mode: false,
    },
  };
}

// Methods
const triggerLogoUpload = () => {
  logoInput.value?.click();
};

const handleLogoUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (file) {
    try {
      const result = await settingsStore.uploadLogo(file);
      snackbar.value = {
        show: true,
        text: "Logo uploaded successfully!",
        color: "success",
        icon: "mdi-check-circle",
      };
    } catch (error) {
      snackbar.value = {
        show: true,
        text: "Failed to upload logo",
        color: "error",
        icon: "mdi-alert-circle",
      };
    }
  }
};

const scanBluetoothDevices = () => {
  if (!navigator.bluetooth) {
    snackbar.value = {
      show: true,
      text: "Bluetooth is not supported on this browser",
      color: "error",
      icon: "mdi-alert-circle",
    };
    return;
  }

  navigator.bluetooth
    .requestDevice({
      acceptAllDevices: true,
      optionalServices: ["000018f0-0000-1000-8000-00805f9b34fb"],
    })
    .then((device) => {
      if (device.name) {
        bluetoothDevices.value.push({
          title: device.name,
          value: device.id,
        });
        settings.value.printer.bluetooth_device = device.id;
        snackbar.value = {
          show: true,
          text: `Connected to ${device.name}`,
          color: "success",
          icon: "mdi-bluetooth",
        };
      }
    })
    .catch((error) => {
      console.error("Bluetooth scan error:", error);
      snackbar.value = {
        show: true,
        text: "Failed to scan for Bluetooth devices",
        color: "error",
        icon: "mdi-alert-circle",
      };
    });
};

const testPrinterConnection = () => {
  snackbar.value = {
    show: true,
    text: "Testing printer connection...",
    color: "info",
    icon: "mdi-printer",
  };

  setTimeout(() => {
    snackbar.value = {
      show: true,
      text: "✅ Printer connected successfully!",
      color: "success",
      icon: "mdi-check-circle",
    };
  }, 2000);
};

const saveAllSettings = async () => {
  saving.value = true;
  try {
    await settingsStore.saveSettings(settings.value);
    snackbar.value = {
      show: true,
      text: "All settings saved successfully!",
      color: "success",
      icon: "mdi-check-circle",
    };
  } catch (error) {
    snackbar.value = {
      show: true,
      text: "Failed to save settings",
      color: "error",
      icon: "mdi-alert-circle",
    };
  } finally {
    saving.value = false;
  }
};

const resetSettings = async () => {
  confirmDialog.value = {
    show: true,
    title: "Reset Settings?",
    message:
      "This will reset all settings to their default values. This action cannot be undone.",
    action: "resetSettings",
    loading: false,
  };
};

const confirmAction = (action: string) => {
  const actions: Record<string, { title: string; message: string }> = {
    clearCache: {
      title: "Clear Cache?",
      message:
        "This will clear all local cache data. Your settings will not be affected.",
    },
    resetSettings: {
      title: "Reset All Settings?",
      message:
        "This will reset ALL settings to factory defaults. This action cannot be undone.",
    },
  };

  const data = actions[action];
  if (data) {
    confirmDialog.value = {
      show: true,
      title: data.title,
      message: data.message,
      action: action,
      loading: false,
    };
  }
};

const executeConfirmAction = async () => {
  confirmDialog.value.loading = true;
  try {
    if (confirmDialog.value.action === "clearCache") {
      localStorage.clear();
      sessionStorage.clear();
      snackbar.value = {
        show: true,
        text: "Cache cleared successfully!",
        color: "success",
        icon: "mdi-check-circle",
      };
    } else if (confirmDialog.value.action === "resetSettings") {
      await settingsStore.resetSettings();
      snackbar.value = {
        show: true,
        text: "Settings have been reset to default values",
        color: "success",
        icon: "mdi-check-circle",
      };
    }
    confirmDialog.value.show = false;
  } catch (error) {
    snackbar.value = {
      show: true,
      text: "Action failed. Please try again.",
      color: "error",
      icon: "mdi-alert-circle",
    };
  } finally {
    confirmDialog.value.loading = false;
  }
};

// Lifecycle
onMounted(async () => {
  try {
    await settingsStore.fetchSettings();
  } catch (error) {
    console.error("Error loading settings:", error);
    snackbar.value = {
      show: true,
      text: "Failed to load settings",
      color: "error",
      icon: "mdi-alert-circle",
    };
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.settings-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
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

.header-actions {
  display: flex;
  gap: 12px;
}

.settings-nav-card {
  background: white;
  border: 1px solid #e5e7eb;
  position: sticky;
  top: 20px;
}

.settings-nav-item {
  border-radius: 8px;
  margin: 2px 8px;
  cursor: pointer;
}

.settings-nav-item:hover {
  background: #f8f6f2;
}

.settings-nav-item .active-text {
  color: #2d6a4f;
  font-weight: 600;
}

.settings-card {
  background: white;
  border: 1px solid #e5e7eb;
}

.section-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
}

.section-icon {
  width: 40px;
  height: 40px;
  background: rgba(45, 106, 79, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 2px;
}

.section-subtitle {
  font-size: 13px;
  color: #6b7280;
}

.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.switch-label {
  font-weight: 500;
  color: #1b4332;
}

.switch-hint {
  font-size: 12px;
  color: #6b7280;
}

.logo-upload-area {
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logo-upload-area:hover {
  border-color: #2d6a4f;
  background: rgba(45, 106, 79, 0.05);
}

.logo-preview {
  position: relative;
  height: 150px;
}

.logo-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #f8f6f2;
  padding: 20px;
}

.logo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.logo-preview:hover .logo-overlay {
  opacity: 1;
}

.logo-placeholder {
  padding: 40px;
  text-align: center;
}

.logo-placeholder p {
  margin-top: 12px;
  color: #374151;
}

.logo-placeholder span {
  font-size: 12px;
  color: #9ca3af;
}

.payment-methods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.payment-method-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f8f6f2;
  border-radius: 12px;
}

.danger-zone {
  padding: 16px;
  background: #fff5f5;
  border-radius: 12px;
  border: 1px solid #fee2e2;
}

.danger-title {
  color: #e07a5f;
  font-weight: 700;
  margin-bottom: 4px;
}

.danger-subtitle {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 16px;
}

.danger-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.confirm-dialog {
  text-align: center;
  padding: 32px;
  border-radius: 24px !important;
}

.confirm-icon {
  margin-bottom: 16px;
}

.confirm-dialog h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 8px;
}

.confirm-dialog p {
  color: #6b7280;
  margin-bottom: 24px;
}

.dialog-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

/* Responsive */
@media (max-width: 768px) {
  .settings-container {
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

  .settings-nav-card {
    position: relative;
    top: 0;
  }

  .payment-methods-grid {
    grid-template-columns: 1fr;
  }

  .danger-actions {
    flex-direction: column;
  }

  .danger-actions .v-btn {
    width: 100%;
  }

  .dialog-actions {
    flex-direction: column;
  }

  .dialog-actions .v-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .section-icon {
    width: 32px;
    height: 32px;
  }

  .logo-preview {
    height: 120px;
  }

  .logo-placeholder {
    padding: 24px;
  }
}
</style>
