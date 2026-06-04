// frontend/components/charts/RevenueChart.vue
<template>
  <div class="revenue-chart">
    <div class="chart-header">
      <div class="chart-title">Revenue Overview</div>
      <div class="chart-controls">
        <button
          v-for="type in chartTypes"
          :key="type.value"
          :class="['chart-type-btn', { active: currentType === type.value }]"
          @click="changeChartType(type.value)"
        >
          {{ type.label }}
        </button>
      </div>
    </div>
    <div class="chart-wrapper">
      <canvas ref="revenueCanvas"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const props = defineProps({
  data: {
    type: Array,
    default: () => [1250, 1420, 1380, 1650, 1890, 2100, 1950],
  },
  labels: {
    type: Array,
    default: () => ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  },
});

const currentType = ref("line");
const revenueCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const chartTypes = [
  { label: "Line", value: "line" },
  { label: "Bar", value: "bar" },
];

const changeChartType = (type: string) => {
  currentType.value = type;
  updateChart();
};

const updateChart = () => {
  if (!revenueCanvas.value) return;

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(revenueCanvas.value, {
    type: currentType.value as any,
    data: {
      labels: props.labels,
      datasets: [
        {
          label: "Revenue",
          data: props.data,
          borderColor: "#2D6A4F",
          backgroundColor:
            currentType.value === "line" ? "rgba(45, 106, 79, 0.1)" : "#2D6A4F",
          tension: 0.4,
          fill: currentType.value === "line",
          borderRadius: 8,
          barPercentage: 0.7,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: (context: any) => {
              return `Revenue: ksh${context.raw}`;
            },
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
            callback: (value: any) => "ksh" + value,
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
    },
  });
};

onMounted(() => {
  updateChart();
});

watch(
  () => props.data,
  () => {
    updateChart();
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
.revenue-chart {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.chart-title {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.chart-controls {
  display: flex;
  gap: 8px;
}

.chart-type-btn {
  padding: 6px 16px;
  border-radius: 20px;
  background: #f8f6f2;
  border: none;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.chart-type-btn.active {
  background: #2d6a4f;
  color: white;
}

.chart-wrapper {
  height: 350px;
  position: relative;
}
</style>
