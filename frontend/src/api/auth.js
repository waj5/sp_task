import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // 后端地址
  timeout: 1000,
})

export const login = async (username, password) => {
  const response = await apiClient.post('/auth/login', { username, password });
  const token = response.data.token; // 假设后端返回的 Token 字段是 "token"
  localStorage.setItem('jwtToken', token); // 将 Token 存储在 localStorage 中
  return response.data;
};

// 请求拦截器：在每次请求前将 Token 添加到请求头中
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwtToken');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`; // 添加 Authorization 头
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const fetchTasks = async () => {
  const response = await apiClient.get("/auth/tasks");
  return response.data.tasks; // 返回任务数据
};