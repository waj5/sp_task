<template>
  <div class="home">
    <h1>欢迎来到首页</h1>
    <el-button type="primary" @click="logout">退出登录</el-button>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    logout() {
      // 清除登录状态并重定向到登录页面
      localStorage.removeItem('token') // 假设使用 token 存储登录状态
      this.$router.push('/login')
    },
  },
}
</script>

<style>
.home {
  text-align: center;
  margin-top: 50px;
}
</style>
