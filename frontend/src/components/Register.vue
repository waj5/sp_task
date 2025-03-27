<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2>用户注册</h2>
      <el-form
        :model="form"
        :rules="rules"
        ref="registerForm"
        label-width="100px"
        class="register-form"
      >
        <el-form-item label="用户名" prop="name">
          <el-input v-model="form.name" placeholder="4-20位字母数字"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="至少8位，包含大写字母和数字"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="有效邮箱地址"></el-input>
        </el-form-item>
        <el-form-item label="角色" prop="isMaster">
          <el-radio-group v-model="form.isMaster">
            <el-radio :label="true">管理者</el-radio>
            <el-radio :label="false">普通用户</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="!form.isMaster" label="管理者ID" prop="masterId">
          <el-input v-model="form.masterId" placeholder="请输入管理者的ID"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">立即注册</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { register } from '../api/auth'
import { ElMessage } from 'element-plus'

export default {
  name: 'Register',
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else if (value.length < 8) {
        callback(new Error('密码长度至少8位'))
      } else if (!/[A-Z]/.test(value)) {
        callback(new Error('密码必须包含至少一个大写字母'))
      } else if (!/[0-9]/.test(value)) {
        callback(new Error('密码必须包含至少一个数字'))
      } else {
        if (this.form.confirmPassword !== '') {
          this.$refs.registerForm.validateField('confirmPassword')
        }
        callback()
      }
    }
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.form.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }

    return {
      form: {
        name: '',
        password: '',
        confirmPassword: '',
        email: '',
        isMaster: true, // 默认选择为管理者
        masterId: '' // 普通用户需要填写管理者ID
      },
      rules: {
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
    }
  },
  methods: {
    submitForm() {
      this.$refs.registerForm.validate(async (valid) => {
        if (valid) {
          try {
            const userData = {
              name: this.form.name,
              password: this.form.password,
              email: this.form.email,
              is_master: this.form.isMaster,
              master_id: this.form.isMaster ? null : this.form.masterId
            }
            await register(userData)
            ElMessage.success('注册成功，请登录')
            this.$router.push('/login')
          } catch (error) {
            ElMessage.error(error.message || '注册失败')
          }
        }
      })
    },
    resetForm() {
      this.$refs.registerForm.resetFields()
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f4f9;
}

.register-card {
  width: 500px;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.register-form {
  margin-top: 20px;
}
</style>
