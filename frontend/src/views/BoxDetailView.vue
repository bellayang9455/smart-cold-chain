<template>
  <main class="page" v-if="detail.box">
    <h1>魚貨箱詳細頁：{{ detail.box.box_id }}</h1>

    <section class="status-banner" :class="detail.box.status">
      目前狀態：{{ statusText(detail.box.status) }}
    </section>

    <section class="card">
      <p><strong>魚種：</strong>{{ detail.box.species }}</p>
      <p><strong>重量：</strong>{{ detail.box.weight }} kg</p>
      <p><strong>數量：</strong>{{ detail.box.quantity }}</p>
      <p><strong>初始分級：</strong>{{ detail.box.initial_grade }}</p>
      <p><strong>目前分級：</strong>{{ detail.box.current_grade }}</p>
      <p><strong>冷凍庫：</strong>{{ detail.box.warehouse_id }}</p>
      <p><strong>最新溫度：</strong>{{ detail.box.latest_temperature }} °C</p>
      <p><strong>最新濕度：</strong>{{ detail.box.latest_humidity }} %</p>
      <p><strong>預估價值：</strong>NT$ {{ detail.box.estimated_price }}</p>
    </section>

    <section class="card">
      <h2>溫度歷史紀錄</h2>
      <TemperatureChart :records="detail.records" />
    </section>

    <section class="card">
      <h2>告警紀錄</h2>

      <table>
        <thead>
          <tr>
            <th>等級</th>
            <th>訊息</th>
            <th>溫度</th>
            <th>時間</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="alert in detail.alerts" :key="alert.id">
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
import { useRoute } from 'vue-router'
import api from '../api/api'
import TemperatureChart from '../components/TemperatureChart.vue'

const route = useRoute()

const detail = ref({
  box: null,
  records: [],
  alerts: []
})

let timer = null

function statusText(status) {
  if (status === 'danger') return '嚴重異常'
  if (status === 'warning') return '警告'
  return '正常'
}

function formatTime(time) {
  if (!time) return '-'
  return new Date(time).toLocaleString()
}

async function fetchDetail() {
  const res = await api.get(`/boxes/${route.params.boxId}`)
  detail.value = res.data
}

onMounted(() => {
  fetchDetail()
  timer = setInterval(fetchDetail, 3000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped>
.page {
  padding: 24px;
}

.card {
  background: white;
  padding: 20px;
  margin-top: 20px;
  border-radius: 12px;
}

.status-banner {
  padding: 16px;
  border-radius: 8px;
  color: white;
  font-weight: bold;
}

.normal {
  background: #16a34a;
}

.warning {
  background: #f59e0b;
}

.danger {
  background: #dc2626;
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