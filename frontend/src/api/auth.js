import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // 后端地址
  timeout: 5000,  // 延长超时时间到5秒
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('jwtToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器（新增错误处理）
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token过期处理
      localStorage.removeItem('jwtToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const login = async (username, password) => {
  try {
    const response = await apiClient.post('/auth/login', { username, password })
    if (response.data.token) {
      localStorage.setItem('jwtToken', response.data.token)
    }
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || '登录失败')
  }
}

export const fetchTasks = async () => {
  try {
    const response = await apiClient.get('/auth/tasks')
    return response.data.tasks
  } catch (error) {
    throw new Error(error.response?.data?.message || '获取任务失败')
  }
}

// 新增添加任务接口
export const addTask = async (taskData) => {
  try {
    const response = await apiClient.post('/auth/tasks', taskData)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || '创建任务失败')
  }
}
