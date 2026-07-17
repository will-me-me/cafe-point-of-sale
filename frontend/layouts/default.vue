<!-- frontend/layouts/default.vue -->
<template>
  <div>
    <v-app>
      <v-navigation-drawer
        v-model="drawer"
        app
        v-if="authStore.isAuthenticated"
      >
        <div class="drawer-header">
          <div class="logo-section">
            <div class="logo-icon">🍩</div>
            <div class="logo-text">BABADEACON</div>
          </div>
        </div>

        <v-list nav density="comfortable">
          <!-- Dashboard -->
          <v-list-item
            v-if="authStore.isAdmin"
            to="/admin/dashboard"
            prepend-icon="mdi-view-dashboard"
            title="Dashboard"
          />
          <!-- {{ authStore.isAdmin }} -->

          <!-- POS Terminal -->
          <v-list-item
            to="/pos"
            prepend-icon="mdi-cash-register"
            title="POS Terminal"
          />

          <!-- Products Management -->
          <v-list-group value="products" v-if="authStore.isAdmin">
            <template #activator="{ props }">
              <v-list-item
                v-bind="props"
                prepend-icon="mdi-package-variant"
                title="Products"
              />
            </template>

            <v-list-item
              to="/admin/products"
              prepend-icon="mdi-view-list"
              title="All Products"
            />

            <v-list-item
              to="/admin/products/add"
              prepend-icon="mdi-plus"
              title="Add Product"
            />

            <v-list-item
              to="/admin/products/categories"
              prepend-icon="mdi-folder"
              title="Categories"
            />

            <v-list-item
              to="/admin/products/brands"
              prepend-icon="mdi-tag"
              title="Brands"
            />

            <v-list-item
              to="/admin/products/suppliers"
              prepend-icon="mdi-truck"
              title="Suppliers"
            />
          </v-list-group>

          <!-- Inventory -->
          <v-list-group value="inventory" v-if="authStore.isAdmin">
            <template #activator="{ props }">
              <v-list-item
                v-bind="props"
                prepend-icon="mdi-warehouse"
                title="Inventory"
              />
            </template>

            <v-list-item
              to="/admin/inventory"
              prepend-icon="mdi-view-list"
              title="Stock Overview"
            />

            <v-list-item
              to="/admin/inventory/movements"
              prepend-icon="mdi-swap-horizontal"
              title="Stock Movements"
            />

            <v-list-item
              to="/admin/inventory/low-stock"
              prepend-icon="mdi-alert"
              title="Low Stock Alert"
            />

            <v-list-item
              to="/admin/inventory/out-of-stock"
              prepend-icon="mdi-close-circle"
              title="Out of Stock"
            />
          </v-list-group>

          <!-- Orders -->
          <v-list-item
            to="/orders"
            prepend-icon="mdi-receipt"
            title="Order History"
          />

          <!-- Sales -->
          <v-list-group value="sales" v-if="authStore.isAdmin">
            <template #activator="{ props }">
              <v-list-item
                v-bind="props"
                prepend-icon="mdi-chart-line"
                title="Sales"
              />
            </template>

            <v-list-item
              to="/admin/sales/today"
              prepend-icon="mdi-calendar-today"
              title="Today's Sales"
            />

            <v-list-item
              to="/admin/sales/transactions"
              prepend-icon="mdi-cash-multiple"
              title="Transactions"
            />

            <v-list-item
              to="/admin/sales/debt"
              prepend-icon="mdi-credit-card-clock"
              title="Debt Orders"
            />
          </v-list-group>

          <!-- Reports -->
          <v-list-group value="reports" v-if="authStore.isAdmin">
            <template #activator="{ props }">
              <v-list-item
                v-bind="props"
                prepend-icon="mdi-chart-bar"
                title="Reports"
                to="/reports"
              />
            </template>

            <v-list-item
              to="/reports/sales"
              prepend-icon="mdi-chart-line"
              title="Sales Report"
            />

            <v-list-item
              to="/reports/inventory"
              prepend-icon="mdi-chart-pie"
              title="Inventory Report"
            />

            <v-list-item
              to="/reports/profit"
              prepend-icon="mdi-chart-timeline"
              title="Profit Report"
            />

            <v-list-item
              to="/reports/expiry"
              prepend-icon="mdi-calendar-clock"
              title="Expiry Report"
            />
          </v-list-group>

          <!-- Users -->
          <v-list-item
            v-if="authStore.isAdmin"
            to="/admin/users"
            prepend-icon="mdi-account-group"
            title="Manage Users"
          />

          <!-- Expenses -->
          <v-list-item
            v-if="authStore.isAdmin"
            to="/admin/expenses"
            prepend-icon="mdi-cash-minus"
            title="Expenses"
          />

          <!-- Settings -->
          <v-list-item
            v-if="authStore.isAdmin"
            to="/admin/settings"
            prepend-icon="mdi-cog"
            title="Settings"
          />
        </v-list>

        <template #append>
          <div class="user-section">
            <v-divider />
            <v-list-item>
              <template #prepend>
                <v-avatar color="#1B4332" size="40">
                  <span class="avatar-initials">{{
                    authStore.userName.charAt(0)
                  }}</span>
                </v-avatar>
              </template>
              <v-list-item-title>{{ authStore.userName }}</v-list-item-title>
              <v-list-item-subtitle>{{
                authStore.userRole
              }}</v-list-item-subtitle>
              <template #append>
                <v-btn icon variant="text" @click="authStore.logout">
                  <v-icon>mdi-logout</v-icon>
                </v-btn>
              </template>
            </v-list-item>
          </div>
        </template>
      </v-navigation-drawer>

      <v-app-bar
        app
        color="white"
        elevation="0"
        v-if="authStore.isAuthenticated"
      >
        <v-app-bar-nav-icon @click="drawer = !drawer" />
        <v-app-bar-title>{{ settingsStore?.storeName }}</v-app-bar-title>
        <v-spacer />
        <div class="user-info">
          <span class="user-role-badge">{{ authStore.userRole }}</span>
          <span class="user-name">{{ authStore.userName }}</span>
          <v-btn icon variant="text" @click="authStore.logout">
            <v-icon>mdi-logout</v-icon>
          </v-btn>
        </div>
      </v-app-bar>

      <v-main>
        <NuxtPage />
      </v-main>
    </v-app>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from "~/stores/settings";

const drawer = ref(true);
const authStore = useAuthStore();
const settingsStore = useSettingsStore();
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap");

.drawer-header {
  padding: 24px 16px;
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
  margin-bottom: 16px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-family: "Playfair Display", serif;
  font-size: 20px;
  font-weight: 800;
  color: white;
}

.user-section {
  padding: 16px;
}

.avatar-initials {
  font-weight: 600;
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-right: 24px;
}

.user-role-badge {
  background: #e07a5f;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.user-name {
  font-weight: 500;
  color: #374151;
}

/* Vuetify overrides */
:deep(.v-list-item) {
  border-radius: 8px;
  margin: 2px 8px;
}

:deep(.v-list-item:hover) {
  background: #f3f4f6;
}

:deep(.v-list-group__items .v-list-item) {
  padding-left: 40px !important;
}
</style>
