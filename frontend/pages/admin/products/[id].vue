<!-- pages/admin/products/[id].vue -->
<template>
  <ProductForm
    mode="edit"
    :product-id="route.params.id as string"
    @success="onSuccess"
    @cancel="onCancel"
  />
</template>

<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import ProductForm from "~/components/products/ProductForm.vue";

const route = useRoute();
const router = useRouter();

const onSuccess = (product: any) => {
  // Optional: handle success
};

const onCancel = () => {
  router.push("/admin/products");
};
</script>
