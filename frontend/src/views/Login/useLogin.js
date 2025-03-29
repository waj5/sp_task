// views/Login/useLogin.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth'
import { ElMessage } from 'element-plus'

export function useLogin(loginFormRef) {
  const router = useRouter()

  // 响应式数据
  const form = ref({
    username: '',
    password: ''
  })

  // 验证规则
  const rules = {
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
  }

  // 提交登录
  const onSubmit = async () => {
    loginFormRef.value.validate(async (valid) => {
      if (valid) {
        try {
          const response = await login(form.value.username, form.value.password)

          // 处理不同的token字段名
          const token = response.access_token || response.token
          if (token) {
            localStorage.setItem('jwtToken', token)
            router.push({ name: 'Home' })
            ElMessage.success('登录成功')
          } else {
            console.error('Token字段缺失:', response)
            ElMessage.error('登录凭证获取失败')
          }
        } catch (error) {
          console.error('登录失败:', error)
          const message = error.response?.data?.detail
            || error.response?.data?.message
            || '登录失败'
          ElMessage.error(message)
        }
      }
    })
  }

  // 重置表单
  const onReset = () => {
    loginFormRef.value.resetFields()
  }

  return {
    form,
    rules,
    onSubmit,
    onReset
  }
}
