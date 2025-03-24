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
  console.log('实际发送的Authorization头:', config.headers.Authorization)
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器（新增错误处理）
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      ElMessage.warning('登录已过期，请重新登录')
      console.error('认证失败详情:', {
        url: error.config.url,
        status: error.response.status,
        data: error.response.data
      })
      // Token过期处理
      localStorage.removeItem('jwtToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const login = async (username, password) => {
  try {
    console.log('请求参数:', { username, password }) // 新增
    const response = await apiClient.post('/auth/login', { username, password })
    console.log('完整响应:', response) // 新增

    // 检查字段名是否匹配后端返回
    const receivedToken = response.data.access_token
      || response.data.token
      || response.data.jwt; // 增加更多可能的字段名

    if (!receivedToken) {
      console.error('未找到token字段，响应数据:', response.data)
      console.log('Token存储完成，当前值:', localStorage.getItem('jwtToken'))
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

export const updateTaskStatus = async (taskId) => {
  try {
    const response = await apiClient.patch(`/auth/tasks/${taskId}`, {
      status: "已完成",          // 明确发送状态
      complete_time: new Date().toISOString()
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || '更新任务状态失败')
  }
}

export const deleteTask = async (taskId) => {
  try {
    await apiClient.delete(`/auth/tasks/${taskId}`)
  } catch (error) {
    throw new Error(error.response?.data?.detail || '删除任务失败')
  }
}

export const updateTaskDetail = async (taskId, taskData) => {
  try {
    const response = await apiClient.patch(`/auth/tasks/${taskId}`, taskData)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || '更新任务失败')
  }
}
export const register = async (userData) => {
  try {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || '注册失败')
  }
}
