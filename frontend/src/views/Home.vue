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
  localStorage.removeItem('jwtToken'); // 修改为 jwtToken
  this.$router.push({ name: 'Login' });
}
  },
};
</script>

<style>
.home {
  text-align: center;
  margin-top: 50px;
}
</style>
