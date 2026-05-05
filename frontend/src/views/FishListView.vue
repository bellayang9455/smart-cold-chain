<template>
  <main class="page">
    <h1>魚貨冷鍊追蹤列表</h1>

    <table>
      <thead>
        <tr>
          <th>魚 ID</th>
          <th>魚種</th>
          <th>冷凍庫</th>
          <th>最新溫度</th>
          <th>狀態</th>
          <th>入庫時間</th>
          <th>累計超溫時間</th>
          <th>操作</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="fish in fishList"
          :key="fish.fish_id"
          :class="{ danger: fish.status === 'danger', warning: fish.status === 'warning' }"
        >
          <td>{{ fish.fish_id }}</td>
          <td>{{ fish.species }}</td>
          <td>{{ fish.warehouse_id }}</td>
          <td>{{ fish.latest_temperature }} °C</td>
          <td>{{ statusText(fish.status) }}</td>
          <td>{{ formatTime(fish.created_at) }}</td>
          <td>{{ formatDuration(fish.cumulative_over_temp_seconds) }}</td>
          <td>
            <RouterLink :to="`/fish/${fish.fish_id}`">查看詳情</RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../api/api'

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

const fishList = ref([])
let timer = null

function statusText(status) {
  if (status === 'danger') return '嚴重異常'
  if (status === 'warning') return '警告'
  return '正常'
}

async function fetchFish() {
  const res = await api.get('/fish')
  fishList.value = res.data
}

onMounted(() => {
  fetchFish()
  timer = setInterval(fetchFish, 3000)
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

.danger {
  background: #fee2e2;
}

.warning {
  background: #fef3c7;
}
</style>