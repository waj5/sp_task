<!-- views/Register/Register.vue -->
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
          <el-input
            v-model="form.name"
            placeholder="4-20位字母数字"
            clearable
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="至少8位，包含大写字母和数字"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="form.email"
            placeholder="example@domain.com"
            clearable
          />
        </el-form-item>

        <el-form-item label="角色" prop="isMaster">
          <el-radio-group v-model="form.isMaster">
            <el-radio :label="true">管理者</el-radio>
            <el-radio :label="false">普通用户</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item
          v-if="!form.isMaster"
          label="管理者ID"
          prop="masterId"
        >
          <el-input
            v-model="form.masterId"
            placeholder="请输入管理者的用户ID"
            clearable
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            @click="submitForm"
            :loading="isSubmitting"
          >
            立即注册
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRegister } from './useRegister'
import './Register.css'

// 表单引用
const registerForm = ref(null)

// 组合式API
const {
  form,
  rules,
  isSubmitting,
  submitForm,
  resetForm
} = useRegister(registerForm)
</script>
