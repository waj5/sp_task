<template>
  <div class="home">
    <h1>欢迎来到首页</h1>
    <el-button type="primary" @click="goToTasks">我的任务</el-button>
    <el-button type="primary" @click="logout">退出登录</el-button>
  </div>
</template>

<script>
export default {
  name: "Home",
  methods: {
    goToTasks() {
      this.$router.push({ name: "MyTasks" }); // 跳转到我的任务页面
    },
    logout() {
      // 清除登录状态
      localStorage.removeItem('token'); // 假设 token 是登录状态的标识

      // 跳转到登录页面
      this.$router.push({ name: 'Login' }); // 使用命名路由跳转
    },
  },
};
</script>

<style>
.home {
  text-align: center;
  margin-top: 50px;
}
</style>
