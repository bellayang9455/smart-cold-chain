<template>
  <main class="page">
    <h1>告警紀錄</h1>

    <table>
      <thead>
        <tr>
          <th>箱號</th>
          <th>等級</th>
          <th>訊息</th>
          <th>溫度</th>
          <th>時間</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="alert in alerts" :key="alert.id">
          <td>{{ alert.box_id }}</td>
          <td>{{ alert.level }}</td>
          <td>{{ alert.message }}</td>
          <td>{{ alert.temperature }} °C</td>
          <td>{{ formatTime(alert.timestamp) }}</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../api/api'

const alerts = ref([])
let timer = null

function formatTime(time) {
  if (!time) return '-'
  return new Date(time).toLocaleString()
}

async function fetchAlerts() {
  const res = await api.get('/alerts')
  alerts.value = res.data
}

onMounted(() => {
  fetchAlerts()
  timer = setInterval(fetchAlerts, 3000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped>
.page {
  padding: 24px;
}

table {
  width: 100%;
  background: white;
  border-collapse: collapse;
  border-radius: 12px;
  overflow: hidden;
}

th,
td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
}
</style>