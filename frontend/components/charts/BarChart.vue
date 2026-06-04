// frontend/components/charts/BarChart.vue
<template>
  <BaseChart type="bar" :data="chartData" :options="chartOptions" />
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
  horizontal: {
    type: Boolean,
    default: false,
  },
});

const chartData = computed(() => ({
  labels: props.labels,
  datasets: props.datasets,
}));

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: props.horizontal ? ("y" as const) : ("x" as const),
  plugins: {
    legend: {
      position: "top" as const,
      labels: {
        usePointStyle: true,
        boxWidth: 8,
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: "#E5E7EB",
      },
      ticks: {
        callback: (value: any) => (props.horizontal ? "$" + value : value),
      },
    },
    x: {
      grid: {
        display: false,
      },
      ticks: {
        callback: (value: any) => (props.horizontal ? value : "$" + value),
      },
    },
  },
}));
</script>
