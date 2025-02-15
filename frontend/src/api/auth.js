import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // 后端地址
  timeout: 1000,
})

export const login = async (username, password) => {
  const response = await apiClient.post('/auth/login', { username, password })
  return response.data
}