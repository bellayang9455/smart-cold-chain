<template>
  <div ref="chartRef" class="chart"></div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  records: {
    type: Array,
    default: () => []
  }
})

const chartRef = ref(null)
let chart = null

function renderChart() {
  if (!chart) return

  const xData = props.records.map(item =>
    new Date(item.timestamp).toLocaleString()
  )

  const yData = props.records.map(item => item.temperature)

  chart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: xData,
      axisLabel: {
        rotate: 30
      }
    },
    yAxis: {
      type: 'value',
      name: '°C'
    },
    series: [
      {
        name: '溫度',
        type: 'line',
        data: yData,
        smooth: true
      }
    ]
  })
}

onMounted(() => {
  chart = echarts.init(chartRef.value)
  renderChart()
})

watch(
  () => props.records,
  () => {
    renderChart()
  },
  { deep: true }
)
</script>

<style scoped>
.chart {
  width: 100%;
  height: 360px;
}
</style>