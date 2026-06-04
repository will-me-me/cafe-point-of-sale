// frontend/components/charts/BaseChart.vue
<template>
  <div class="chart-container">
    <!-- <h2>BaseChart Loaded</h2> -->
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import { Chart, registerables } from "chart.js";

// Register all Chart.js components
Chart.register(...registerables);

const props = defineProps({
  type: {
    type: String,
    default: "line",
    validator: (value: string) =>
      ["line", "bar", "doughnut", "pie", "radar"].includes(value),
  },
  data: {
    type: Object,
    required: true,
  },
  options: {
    type: Object,
    default: () => ({}),
  },
});

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const createChart = () => {
  console.log("Creating chart");
  if (!chartCanvas.value) {
    console.log("Canvas not found");
    return;
  }
  console.log(props.type);
  console.log(props.data);
  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(chartCanvas.value, {
    type: props.type as any,
    data: props.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      ...props.options,
    },
  });
};

onMounted(() => {
  console.log("Canvas:", chartCanvas.value);
  createChart();
});

watch(
  () => [props.data, props.options],
  () => {
    createChart();
  },
  { deep: true }
);

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>
