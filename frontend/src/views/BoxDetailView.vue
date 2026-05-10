<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import QRCode from 'qrcode'
import api from '../api/api'
import TemperatureChart from '../components/TemperatureChart.vue'

const route = useRoute()

const detail = ref({
  box: null,
  records: [],
  alerts: []
})

const qrCodeUrl = ref('')

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

async function generateQRCode() {
  const boxUrl = `${window.location.origin}/boxes/${route.params.boxId}`
  qrCodeUrl.value = await QRCode.toDataURL(boxUrl)
}

async function fetchDetail() {
  const res = await api.get(`/boxes/${route.params.boxId}`)
  detail.value = res.data

  await nextTick()
  await generateQRCode()
}

onMounted(() => {
  fetchDetail()
  timer = setInterval(fetchDetail, 3000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>