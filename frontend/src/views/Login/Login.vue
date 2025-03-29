<!-- views/Login/Login.vue -->
<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>登录</h2>
      <el-form
        :model="form"
        :rules="rules"
        ref="loginForm"
        label-width="80px"
        class="login-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">登录</el-button>
          <el-button @click="onReset">重置</el-button>
        </el-form-item>
      </el-form>
      <div class="register-link">
        <el-link type="primary" @click="$router.push('/register')">没有账号？立即注册</el-link>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useLogin } from './useLogin'
import './Login.css'

const loginForm = ref(null)
const { form, rules, onSubmit, onReset } = useLogin(loginForm)
</script>
