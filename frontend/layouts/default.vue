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

        <v-list>
          <v-list-item
            v-if="authStore.isAdmin"
            to="/admin/dashboard"
            prepend-icon="mdi-view-dashboard"
            title="Dashboard"
          />
          <v-list-item
            to="/pos"
            prepend-icon="mdi-cash-register"
            title="POS Terminal"
          />
          <v-list-item
            v-if="authStore.isAdmin"
            to="/admin/products"
            prepend-icon="mdi-coffee"
            title="Manage Products"
          />
          <v-list-item
            to="/orders"
            prepend-icon="mdi-receipt"
            title="Order History"
          />
          <v-list-item
            v-if="authStore.isAdmin"
            to="/admin/users"
            prepend-icon="mdi-account-group"
            title="Manage Users"
          />
          <v-list-item
            to="/reports"
            prepend-icon="mdi-chart-bar"
            title="Reports"
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
        <v-app-bar-title>Grounds Coffee POS</v-app-bar-title>
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
const drawer = ref(true);
const authStore = useAuthStore();
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
</style>
