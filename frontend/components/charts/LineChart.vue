// frontend/components/charts/LineChart.vue
<template>
  <BaseChart type="line" :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps({
  labels: {
    type: Array,
    default: () => [],
  },
  datasets: {
    type: Array,
    required: true,
  },
  showGrid: {
    type: Boolean,
    default: true,
  },
});

const chartData = computed(() => ({
  labels: props.labels,
  datasets: props.datasets.map((dataset) => ({
    tension: 0.4,
    fill: true,
    ...dataset,
  })),
}));

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "top" as const,
      labels: {
        usePointStyle: true,
        boxWidth: 8,
      },
    },
    tooltip: {
      mode: "index" as const,
      intersect: false,
    },
  },
  scales: {
    y: {
      grid: {
        display: props.showGrid,
        drawBorder: true,
        color: "#E5E7EB",
      },
      ticks: {
        callback: (value: any) => "$" + value,
      },
    },
    x: {
      grid: {
        display: false,
      },
    },
  },
}));
</script>
