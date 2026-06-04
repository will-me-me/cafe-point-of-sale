<!-- // frontend/components/charts/DoughnutChart.vue -->
<template>
  <!-- <h1>DoughnutChart Loaded</h1> -->
  <BaseChart type="doughnut" :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import { computed } from "vue";
import BaseChart from "./BaseChart.vue";

const props = defineProps({
  labels: {
    type: Array,
    default: () => [],
  },
  data: {
    type: Array,
    required: true,
  },
  colors: {
    type: Array,
    default: () => ["#2D6A4F", "#E07A5F", "#F4A261", "#6B4E71", "#E9C46A"],
  },
});

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      data: props.data,
      backgroundColor: props.colors,
      borderWidth: 0,
      hoverOffset: 10,
    },
  ],
}));

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "bottom" as const,
      labels: {
        usePointStyle: true,
        boxWidth: 8,
        padding: 20,
      },
    },
    tooltip: {
      callbacks: {
        label: (context: any) => {
          const label = context.label || "";
          const value = context.raw || 0;
          const total = context.dataset.data.reduce(
            (a: number, b: number) => a + b,
            0
          );
          const percentage = ((value / total) * 100).toFixed(1);
          return `${label}: ksh${value} (${percentage}%)`;
        },
      },
    },
  },
  cutout: "60%",
}));
</script>
