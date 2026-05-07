<template>
  <main class="page">
    <h1>智慧冷鏈儀表板</h1>

    <section class="cards">
      <div class="card">
        <h3>魚貨箱總數</h3>
        <p>{{ dashboard.total_boxes }}</p>
      </div>

      <div class="card">
        <h3>正常數量</h3>
        <p>{{ dashboard.normal_count }}</p>
      </div>

      <div class="card danger-card">
        <h3>異常數量</h3>
        <p>{{ dashboard.abnormal_count }}</p>
      </div>

      <div class="card">
        <h3>平均溫度</h3>
        <p>{{ dashboard.average_temperature }} °C</p>
      </div>

      <div class="card">
        <h3>總預估價值</h3>
        <p>NT$ {{ dashboard.total_estimated_value }}</p>
      </div>
    </section>

    <section v-if="dashboard.abnormal_count > 0" class="alert-banner">
      ⚠️ 目前有魚貨箱溫度異常，請立即檢查冷凍庫狀態
    </section>

    <section class="panel">
      <h2>最新告警</h2>

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
          <tr v-for="alert in dashboard.latest_alerts" :key="alert.id">
            <td>{{ alert.box_id }}</td>
            <td>{{ alert.level }}</td>
            <td>{{ alert.message }}</td>
            <td>{{ alert.temperature }} °C</td>
            <td>{{ formatTime(alert.timestamp) }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../api/api'

const dashboard = ref({
  total_boxes: 0,
  normal_count: 0,
  abnormal_count: 0,
  average_temperature: null,
  total_estimated_value: 0,
  latest_alerts: []
})

let timer = null

function formatTime(time) {
  if (!time) return '-'
  return new Date(time).toLocaleString()
}

async function fetchDashboard() {
  const res = await api.get('/dashboard')
  dashboard.value = res.data
}

onMounted(() => {
  fetchDashboard()
  timer = setInterval(fetchDashboard, 3000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped>
.page {
  padding: 24px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.card p {
  font-size: 28px;
  font-weight: bold;
}

.danger-card {
  border-left: 6px solid #ef4444;
}

.alert-banner {
  margin: 20px 0;
  padding: 16px;
  background: #dc2626;
  color: white;
  border-radius: 8px;
  font-weight: bold;
}

.panel {
  margin-top: 24px;
  background: white;
  padding: 20px;
  border-radius: 12px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}
</style>