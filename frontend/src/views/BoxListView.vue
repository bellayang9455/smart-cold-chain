<template>
  <main class="page">
    <h1>魚貨箱列表</h1>

    <table>
      <thead>
        <tr>
          <th>箱號</th>
          <th>魚種</th>
          <th>重量</th>
          <th>數量</th>
          <th>初始分級</th>
          <th>目前分級</th>
          <th>冷凍庫</th>
          <th>最新溫度</th>
          <th>預估價值</th>
          <th>狀態</th>
          <th>操作</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="box in boxList"
          :key="box.box_id"
          :class="{
            danger: box.status === 'danger',
            warning: box.status === 'warning'
          }"
        >
          <td>{{ box.box_id }}</td>
          <td>{{ box.species }}</td>
          <td>{{ box.weight }} kg</td>
          <td>{{ box.quantity }}</td>
          <td>{{ box.initial_grade }}</td>
          <td>{{ box.current_grade }}</td>
          <td>{{ box.warehouse_id }}</td>
          <td>{{ box.latest_temperature }} °C</td>
          <td>NT$ {{ box.estimated_price }}</td>
          <td>{{ statusText(box.status) }}</td>
          <td>
            <RouterLink :to="`/boxes/${box.box_id}`">
              查看詳情
            </RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../api/api'

const boxList = ref([])
let timer = null

function statusText(status) {
  if (status === 'danger') return '嚴重異常'
  if (status === 'warning') return '警告'
  return '正常'
}

async function fetchBoxes() {
  try {
    const res = await api.get('/boxes')
    boxList.value = res.data
  } catch (error) {
    console.error('魚貨箱資料取得失敗：', error)
  }
}
onMounted(() => {
  fetchBoxes()
  timer = setInterval(fetchBoxes, 3000)
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