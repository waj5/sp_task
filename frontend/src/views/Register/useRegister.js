// views/Register/useRegister.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'
import { ElMessage } from 'element-plus'

export function useRegister(registerFormRef) {
  const router = useRouter()

  // 响应式表单数据
  const form = ref({
    name: '',
    password: '',
    confirmPassword: '',
    email: '',
    isMaster: true,
    masterId: ''
  })

  // 密码验证规则
  const validatePass = (rule, value, callback) => {
    if (!value) {
      callback(new Error('请输入密码'))
    } else if (value.length < 8) {
      callback(new Error('密码长度至少8位'))
    } else if (!/[A-Z]/.test(value)) {
      callback(new Error('必须包含至少一个大写字母'))
    } else if (!/[0-9]/.test(value)) {
      callback(new Error('必须包含至少一个数字'))
    } else {
      if (form.value.confirmPassword) {
        registerFormRef.value.validateField('confirmPassword')
      }
      callback()
    }
  }

  // 确认密码验证
  const validatePass2 = (rule, value, callback) => {
    if (!value) {
      callback(new Error('请确认密码'))
    } else if (value !== form.value.password) {
      callback(new Error('两次输入密码不一致'))
    } else {
      callback()
    }
  }

  // 表单验证规则
  const rules = {
    name: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 4, max: 20, message: '长度在4到20个字符', trigger: 'blur' },
      { pattern: /^[a-zA-Z0-9_]+$/, message: '只能包含字母、数字和下划线' }
    ],
    password: [
      { required: true, validator: validatePass, trigger: 'blur' }
    ],
    confirmPassword: [
      { required: true, validator: validatePass2, trigger: 'blur' }
    ],
    email: [
      { required: true, message: '请输入邮箱地址', trigger: 'blur' },
      { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
    ],
    masterId: [
      { required: true, message: '请输入管理者ID', trigger: 'blur' }
    ]
  }

  // 提交表单
  const submitForm = async () => {
    try {
      await registerFormRef.value.validate()

      const userData = {
        name: form.value.name,
        password: form.value.password,
        email: form.value.email,
        is_master: form.value.isMaster,
        master_id: form.value.isMaster ? null : form.value.masterId
      }

      await register(userData)
      ElMessage.success('注册成功')
      router.push('/login')
    } catch (error) {
      const message = error.response?.data?.detail
        || error.response?.data?.message
        || '注册失败'
      ElMessage.error(message)
    }
  }

  // 重置表单
  const resetForm = () => {
    registerFormRef.value.resetFields()
  }

  return {
    form,
    rules,
    submitForm,
    resetForm
  }
}
