<!-- pages/admin/products/add.vue -->
<template>
  <ProductForm mode="create" @success="onSuccess" @cancel="onCancel" />
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import ProductForm from "~/components/products/ProductForm.vue";

const router = useRouter();

const onSuccess = (product: any) => {
  // Optional: handle success
};

const onCancel = () => {
  router.push("/admin/products");
};
</script>
