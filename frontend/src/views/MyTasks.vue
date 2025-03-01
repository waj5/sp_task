<template>
  <div class="my-tasks">
    <h1>我的任务</h1>
    <el-table :data="tasks" style="width: 100%">
      <el-table-column prop="id" label="任务ID" width="100"></el-table-column>
      <el-table-column prop="title" label="任务标题"></el-table-column>
      <el-table-column prop="status" label="任务状态"></el-table-column>
    </el-table>
    <el-button type="primary" @click="goBack" style="margin-top: 20px;">返回首页</el-button>
  </div>
</template>

<script>
import { fetchTasks } from "../api/auth"; // 引入任务接口方法
import { ElMessage } from "element-plus";

export default {
  name: "MyTasks",
  data() {
    return {
      tasks: [], // 用于存储任务数据
    };
  },
  methods: {
    async loadTasks() {
      try {
        this.tasks  = await fetchTasks(); // 调用接口获取任务数据

      } catch (error) {
        console.error(error);
        ElMessage.error("加载任务失败，请稍后重试");
      }
    },
    goBack() {
      this.$router.push({ name: "Home" }); // 返回首页
    },
  },
  mounted() {
    this.loadTasks(); // 页面加载时调用接口获取数据
  },
};
</script>

<style>
.my-tasks {
  text-align: center;
  margin: 20px auto;
  max-width: 800px;
}
</style>
