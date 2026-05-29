<template>
  <v-app>
    <div class="app-container">
      <v-card class="main-card" elevation="0" flat>
        <slot />
      </v-card>
    </div>
  </v-app>
</template>

<script setup lang="ts"></script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f3ed 0%, #f5f3ed 100%);
  padding: 0px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-card {
  width: 100%;
  background: #f5f3ed !important;
  overflow: hidden;
}
</style>
