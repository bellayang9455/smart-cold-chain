<template>
  <main class="page">
    <h1>冷鏈異常告警紀錄</h1>

    <table>
      <thead>
        <tr>
          <th>魚 ID</th>
          <th>等級</th>
          <th>訊息</th>
          <th>溫度</th>
          <th>時間</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="alert in alerts" :key="alert.id">
          <td>{{ alert.fish_id }}</td>
          <td>{{ alert.level }}</td>
          <td>{{ alert.message }}</td>
          <td>{{ alert.temperature }} °C</td>
          <td>{{ new Date(alert.timestamp).toLocaleString() }}</td>
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