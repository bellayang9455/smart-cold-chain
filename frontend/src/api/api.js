import axios from 'axios'

const api = axios.create({
  baseURL: 'https://smart-cold-api.onrender.com'

})

export default api