<template>
  <main class="page" v-if="detail.fish">
    <h1>魚貨冷鏈履歷：{{ detail.fish.fish_id }}</h1>

    <section
      class="status-banner"
      :class="detail.fish.status"
    >
      目前狀態：{{ statusText(detail.fish.status) }}
    </section>

    <section class="card">
      <p><strong>魚種：</strong>{{ detail.fish.species }}</p>
      <p><strong>冷凍庫：</strong>{{ detail.fish.warehouse_id }}</p>
      <p><strong>入庫時間：</strong>{{ formatTime(detail.fish.created_at) }}</p>
      <p><strong>最新溫度：</strong>{{ detail.fish.latest_temperature }} °C</p>
      <p><strong>最新濕度：</strong>{{ detail.fish.latest_humidity }} %</p>
      <p><strong>累計超溫時間：</strong>{{ formatDuration(detail.fish.cumulative_over_temp_seconds) }}</p>
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="alert in detail.alerts" :key="alert.id">
            <td>{{ alert.level }}</td>
            <td>{{ alert.message }}</td>
            <td>{{ alert.temperature }} °C</td>
          </tr>
        </tbody>
      </table>
    </section>
    <section class="card">
      <h2>魚貨追蹤 QR Code</h2>

      <div class="qr-box">
        <QrcodeVue :value="currentUrl" :size="180" />

        <p class="qr-text">
          掃描查看魚貨即時狀態
        </p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/api'
import TemperatureChart from '../components/TemperatureChart.vue'
import QrcodeVue from 'qrcode.vue'

const currentUrl = window.location.href

function formatTime(time) {
  if (!time) return '-'
  return new Date(time).toLocaleString()
}

function formatDuration(seconds) {
  if (!seconds) return '0 秒'

  const min = Math.floor(seconds / 60)
  const sec = seconds % 60

  if (min > 0) return `${min} 分 ${sec} 秒`
  return `${sec} 秒`
}

const route = useRoute()
const detail = ref({
  fish: null,
  records: [],
  alerts: []
})

let timer = null

function statusText(status) {
  if (status === 'danger') return '嚴重異常'
  if (status === 'warning') return '警告'
  return '正常'
}

async function fetchDetail() {
  const res = await api.get(`/fish/${route.params.fishId}`)
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