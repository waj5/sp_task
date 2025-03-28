<script setup>
import { useHome } from './Home.js';

const { goToTasks, logout } = useHome();
</script>

<template>
  <div class="home">
    <h1>欢迎来到首页</h1>
    <el-button type="primary" @click="goToTasks">我的任务</el-button>
    <el-button type="primary" @click="logout">退出登录</el-button>
  </div>
</template>

<style src="./Home.css"></style>
