<template>
  <main class="page">
    <h1>智慧冷鏈儀表板</h1>
      <p class="subtitle">即時追蹤魚貨溫度、濕度與異常告警狀態</p>

    <section class="cards">
      <div class="card">
        <h3>監控中的魚貨</h3>
        <p>{{ dashboard.total_fish }}</p>
      </div>

      <div class="card">
        <h3>冷鍊正常</h3>
        <p>{{ dashboard.normal_count }}</p>
      </div>

      <div class="card danger">
        <h3>溫度異常</h3>
        <p>{{ dashboard.abnormal_count }}</p>
      </div>

      <div class="card">
        <h3>平均保存溫度</h3>
        <p>{{ dashboard.average_temperature }} °C</p>
      </div>
    </section>

    <section v-if="dashboard.abnormal_count > 0" class="alert-banner">
      ⚠️ 目前有魚貨溫度異常，請立即檢查冷凍庫狀態
    </section>

    <section class="panel">
      <h2>最新告警</h2>

      <table>
        <thead>
          <tr>
            <th>魚 ID</th>
            <th>等級</th>
            <th>訊息</th>
            <th>溫度</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alert in dashboard.latest_alerts" :key="alert.id">
            <td>{{ alert.fish_id }}</td>
            <td>{{ alert.level }}</td>
            <td>{{ alert.message }}</td>
            <td>{{ alert.temperature }} °C</td>
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
  total_fish: 0,
  normal_count: 0,
  abnormal_count: 0,
  average_temperature: null,
  latest_alerts: []
})

let timer = null

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
.subtitle {
  color: #64748b;
  margin-top: -8px;
  margin-bottom: 24px;
}
.page {
  padding: 24px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.card p {
  font-size: 32px;
  font-weight: bold;
}

.danger {
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