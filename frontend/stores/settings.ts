// stores/settings.ts
import { defineStore } from "pinia";

export interface StoreSettings {
  name: string;
  email: string;
  address: string;
  phone: string;
  currency: string;
  timezone: string;
  logo: string | null;
}

export interface POSSettings {
  default_order_type: string;
  default_payment: string;
  tax_rate: number;
  receipt_footer: string;
  auto_print_receipt: boolean;
  require_customer: boolean;
  allow_debt: boolean;
}

export interface ProductSettings {
  default_reorder: number;
  low_stock_threshold: number;
  enable_variants: boolean;
  track_inventory: boolean;
  require_barcode: boolean;
}

export interface PaymentMethod {
  id: string;
  name: string;
  icon: string;
  enabled: boolean;
}

export interface PaymentSettings {
  payment_methods: PaymentMethod[];
  mpesa_paybill: string | null;
  mpesa_account: string | null;
  allow_partial_payment: boolean;
}

export interface ReceiptSettings {
  header: string;
  footer: string;
  paper_width: string;
  font_size: string;
  show_tax_breakdown: boolean;
  show_item_discounts: boolean;
}

export interface PrinterSettings {
  connection_type: string;
  bluetooth_device: string | null;
  usb_device: string | null;
  ip_address: string | null;
  port: string;
}

export interface SystemSettings {
  backup_frequency: string;
  log_retention: number;
  auto_backup: boolean;
  debug_mode: boolean;
}

export interface Settings {
  store: StoreSettings;
  pos: POSSettings;
  products: ProductSettings;
  payments: PaymentSettings;
  receipt: ReceiptSettings;
  printer: PrinterSettings;
  system: SystemSettings;
  updated_at?: string;
}

export const useSettingsStore = defineStore("settings", {
  state: () => ({
    settings: null as Settings | null,
    loading: false,
    saving: false,
    error: null as string | null,
  }),

  getters: {
    // Store Settings
    storeSettings: (state) => state.settings?.store || null,
    storeName: (state) => state.settings?.store?.name || "Babadeacon Coffee",
    storeEmail: (state) => state.settings?.store?.email || "",
    storeAddress: (state) => state.settings?.store?.address || "",
    storePhone: (state) => state.settings?.store?.phone || "",
    storeCurrency: (state) => state.settings?.store?.currency || "KES",
    storeTimezone: (state) =>
      state.settings?.store?.timezone || "Africa/Nairobi",
    storeLogo: (state) => state.settings?.store?.logo || null,

    // POS Settings
    posSettings: (state) => state.settings?.pos || null,
    defaultOrderType: (state) =>
      state.settings?.pos?.default_order_type || "takeaway",
    defaultPayment: (state) => state.settings?.pos?.default_payment || "cash",
    taxRate: (state) => state.settings?.pos?.tax_rate || 10,
    receiptFooter: (state) =>
      state.settings?.pos?.receipt_footer || "Thank you for your order!",
    autoPrintReceipt: (state) =>
      state.settings?.pos?.auto_print_receipt ?? true,
    requireCustomer: (state) => state.settings?.pos?.require_customer ?? false,
    allowDebt: (state) => state.settings?.pos?.allow_debt ?? true,

    // Product Settings
    productSettings: (state) => state.settings?.products || null,
    defaultReorder: (state) => state.settings?.products?.default_reorder || 10,
    lowStockThreshold: (state) =>
      state.settings?.products?.low_stock_threshold || 5,
    enableVariants: (state) =>
      state.settings?.products?.enable_variants ?? true,
    trackInventory: (state) =>
      state.settings?.products?.track_inventory ?? true,
    requireBarcode: (state) =>
      state.settings?.products?.require_barcode ?? false,

    // Payment Settings
    paymentSettings: (state) => state.settings?.payments || null,
    paymentMethods: (state) => state.settings?.payments?.payment_methods || [],
    enabledPaymentMethods: (state) =>
      state.settings?.payments?.payment_methods?.filter((m) => m.enabled) || [],
    mpesaPaybill: (state) => state.settings?.payments?.mpesa_paybill || null,
    mpesaAccount: (state) => state.settings?.payments?.mpesa_account || null,
    allowPartialPayment: (state) =>
      state.settings?.payments?.allow_partial_payment ?? false,

    // Receipt Settings
    receiptSettings: (state) => state.settings?.receipt || null,
    receiptHeader: (state) =>
      state.settings?.receipt?.header ||
      "☕ BABADEACON COFFEE\nPremium Coffee & Snacks",
    receiptFooterText: (state) =>
      state.settings?.receipt?.footer ||
      "Thank you for your order!\nVisit us again at Babadeacon Coffee",
    receiptPaperWidth: (state) => state.settings?.receipt?.paper_width || "80",
    receiptFontSize: (state) => state.settings?.receipt?.font_size || "12",
    showTaxBreakdown: (state) =>
      state.settings?.receipt?.show_tax_breakdown ?? true,
    showItemDiscounts: (state) =>
      state.settings?.receipt?.show_item_discounts ?? true,

    // Printer Settings
    printerSettings: (state) => state.settings?.printer || null,
    printerConnectionType: (state) =>
      state.settings?.printer?.connection_type || "bluetooth",
    printerBluetoothDevice: (state) =>
      state.settings?.printer?.bluetooth_device || null,
    printerUsbDevice: (state) => state.settings?.printer?.usb_device || null,
    printerIpAddress: (state) => state.settings?.printer?.ip_address || null,
    printerPort: (state) => state.settings?.printer?.port || "9100",

    // System Settings
    systemSettings: (state) => state.settings?.system || null,
    backupFrequency: (state) =>
      state.settings?.system?.backup_frequency || "daily",
    logRetention: (state) => state.settings?.system?.log_retention || 30,
    autoBackup: (state) => state.settings?.system?.auto_backup ?? true,
    debugMode: (state) => state.settings?.system?.debug_mode ?? false,

    isLoaded: (state) => state.settings !== null,
  },

  actions: {
    async fetchSettings() {
      const authStore = useAuthStore();
      this.loading = true;
      this.error = null;

      try {
        const response = await fetch("http://127.0.0.1:8000/settings/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authStore.token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(
            `Failed to fetch settings: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        this.settings = data;
        return data;
      } catch (error) {
        console.error("Error fetching settings:", error);
        this.error =
          error instanceof Error ? error.message : "Failed to load settings";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async saveSettings(settingsData: Partial<Settings>) {
      const authStore = useAuthStore();
      this.saving = true;
      this.error = null;

      try {
        const response = await fetch("http://127.0.0.1:8000/settings/", {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${authStore.token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(settingsData),
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(
            `Failed to save settings: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        this.settings = data;
        return data;
      } catch (error) {
        console.error("Error saving settings:", error);
        this.error =
          error instanceof Error ? error.message : "Failed to save settings";
        throw error;
      } finally {
        this.saving = false;
      }
    },

    async saveStoreSettings(storeData: Partial<StoreSettings>) {
      const authStore = useAuthStore();
      this.saving = true;
      this.error = null;

      try {
        const response = await fetch("http://127.0.0.1:8000/settings/store", {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${authStore.token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(storeData),
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(
            `Failed to save store settings: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        if (this.settings) {
          this.settings.store = data;
        }
        return data;
      } catch (error) {
        console.error("Error saving store settings:", error);
        this.error =
          error instanceof Error
            ? error.message
            : "Failed to save store settings";
        throw error;
      } finally {
        this.saving = false;
      }
    },

    async savePOSSettings(posData: Partial<POSSettings>) {
      const authStore = useAuthStore();
      this.saving = true;
      this.error = null;

      try {
        const response = await fetch("http://127.0.0.1:8000/settings/pos", {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${authStore.token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(posData),
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(
            `Failed to save POS settings: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        if (this.settings) {
          this.settings.pos = data;
        }
        return data;
      } catch (error) {
        console.error("Error saving POS settings:", error);
        this.error =
          error instanceof Error
            ? error.message
            : "Failed to save POS settings";
        throw error;
      } finally {
        this.saving = false;
      }
    },

    async resetSettings() {
      const authStore = useAuthStore();
      this.saving = true;
      this.error = null;

      try {
        const response = await fetch("http://127.0.0.1:8000/settings/reset", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${authStore.token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(
            `Failed to reset settings: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        this.settings = data;
        return data;
      } catch (error) {
        console.error("Error resetting settings:", error);
        this.error =
          error instanceof Error ? error.message : "Failed to reset settings";
        throw error;
      } finally {
        this.saving = false;
      }
    },

    async uploadLogo(file: File) {
      const authStore = useAuthStore();
      this.saving = true;
      this.error = null;

      try {
        const formData = new FormData();
        formData.append("logo", file);

        const response = await fetch(
          "http://127.0.0.1:8000/settings/store/logo",
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${authStore.token}`,
            },
            body: formData,
          }
        );

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(
            `Failed to upload logo: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        if (this.settings) {
          this.settings.store.logo = data.logo_url;
        }
        return data;
      } catch (error) {
        console.error("Error uploading logo:", error);
        this.error =
          error instanceof Error ? error.message : "Failed to upload logo";
        throw error;
      } finally {
        this.saving = false;
      }
    },
  },

  persist: {
    storage: localStorage,
    paths: ["settings"],
  },
});
