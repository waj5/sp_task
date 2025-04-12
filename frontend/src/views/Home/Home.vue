<script setup>
import { onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { useHome } from './Home.js';

const {
  randomTasks,
  selectedTask,
  dialogVisible,
  loading,
  homeStyle,
  getAllTasks,
  shuffleArray,
  goToTasks,
  logout,
  showTaskDetails
} = useHome();

onMounted(async () => {
  try {
    const tasks = await getAllTasks();
    console.log('获取到的原始任务:', tasks);
    
    // 确保 tasks 是数组且不为空
    if (Array.isArray(tasks) && tasks.length > 0) {
      randomTasks.value = shuffleArray([...tasks]).slice(0, 9);
      console.log('处理后的任务:', randomTasks.value);
    } else {
      console.log('没有获取到任务数据或数据为空');
      randomTasks.value = []; // 确保设置为空数组
      ElMessage.info('暂无任务数据');
    }
  } catch (error) {
    console.error('初始化任务失败:', error);
    randomTasks.value = []; // 确保设置为空数组
    ElMessage.error('加载任务失败，请刷新页面重试');
  }
});
</script>

<template>
  <div class="home" :style="homeStyle">
    <div class="header">
      <h1>欢迎来到首页</h1>
      <div class="nav-buttons">
        <el-button type="primary" :plain="false">首页</el-button>
        <el-button type="primary" :plain="true" @click="goToTasks">我的任务</el-button>
      </div>
      <div class="header-actions">
        <el-button type="danger" @click="logout">退出登录</el-button>
      </div>
    </div>
    <div class="task-grid">
      <div
        v-for="(task,index) in randomTasks"
        :key="index"
        class="task-card"
        :style="{
          backgroundColor: `hsl(${Math.random()*360},70%,85%)`,
          transform: `rotateY(${Math.random()*10-5}deg)`
        }"
        @click="showTaskDetails(task)"
      >
        <div class="book-spine"></div>
        <div class="book-content">
          <h3>{{task.title}}</h3>
          <div class="task-preview">
            <p><strong>负责人:</strong> {{ task.designee_name }}</p>
            <p><strong>状态:</strong> {{ task.status }}</p>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      v-model="dialogVisible"
      title="任务详情"
      width="70%"
      center
      class="book-dialog"
    >
      <div v-if="selectedTask" class="task-details">
        <div class="book-cover">
          <div class="book-spine"></div>
          <div class="book-pages">
            <div class="book-left">
              <h3>{{ selectedTask.title }}</h3>
              <div class="task-meta">
                <p><strong>任务ID:</strong> {{ selectedTask.id }}</p>
                <p><strong>创建时间:</strong> {{ selectedTask.create_time }}</p>
                <p v-if="selectedTask.status === '已完成'">
                  <strong>完成时间:</strong> {{ selectedTask.complete_time }}
                </p>
                <p><strong>负责人:</strong> {{ selectedTask.designee_name }}</p>
                <p><strong>创建人:</strong> {{ selectedTask.creator_name }}</p>
              </div>
            </div>
            <div class="book-right">
              <div class="task-content">
                <h4>任务内容</h4>
                <p>{{ selectedTask.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<style src="./Home.css"></style>