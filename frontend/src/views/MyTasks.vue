<template>
 <div class="my-tasks-container">
  <!-- 左侧菜单栏 -->
  <el-menu
    class="side-menu"
    default-active="1"
    @select="handleMenuSelect"
  >
    <el-menu-item index="1">
      <span>添加任务</span>
    </el-menu-item>
  </el-menu>
  <div class="my-tasks">
    <h1>我的任务</h1>
    <el-collapse v-model="activeTaskId" accordion>
      <el-collapse-item v-for="task in tasks" :key="task.id" :name="task.id">
        <template #title>
          <div class="task-title">
            <span>{{ task.title }}</span>
          </div>
        </template>
        <el-card class="task-detail-card">
          <div class="task-info">
            <p><strong>任务ID:</strong> {{ task.id }}</p>
            <p><strong>任务内容:</strong> {{ task.content }}</p>
            <p><strong>创建时间:</strong> {{ task.create_time }}</p>
            <p><strong>完成时间:</strong> {{ task.complete_time || "未完成" }}</p>
            <p><strong>负责人ID:</strong> {{ task.designee_id }}</p>
            <p><strong>创建人ID:</strong> {{ task.create_user_id }}</p>
            <el-button
              type="primary"
              @click="markTaskComplete(task)"
              v-if="!task.complete_time"
              class="complete-button"
            >
              标记为完成
            </el-button>
          </div>
        </el-card>
      </el-collapse-item>
    </el-collapse>
    <el-button type="primary" @click="goBack" style="margin-top: 20px;">返回首页</el-button>
  </div>
 </div>
</template>

<script>
import { fetchTasks } from "../api/auth"; // 引入任务接口方法
import { ElMessage } from "element-plus";
import { ElCard, ElButton, ElCollapse, ElCollapseItem } from 'element-plus';

export default {
  name: "MyTasks",
  data() {
    return {
      tasks: [], // 用于存储任务数据
      activeTaskId: null, // 当前展开的任务ID
    };
  },
  methods: {
    async loadTasks() {
      try {
        this.tasks = await fetchTasks(); // 调用接口获取任务数据
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
  components: {
    ElCard,
    ElButton,
    ElCollapse,
    ElCollapseItem,
  },
};
</script>

<style>
.my-tasks {
  text-align: center;
  margin: 20px auto;
  max-width: 800px;
}

.task-title {
  font-size: 16px;
  font-weight: bold;
}

.task-detail-card {
  margin-top: 10px;
  text-align: left;
}

.task-info p {
  margin: 5px 0;
}

.complete-button {
  margin-top: 10px; /* 完成按钮与上方内容保持一定距离 */
}

/* 确保 el-collapse-item 内容左对齐 */
.el-collapse-item__content {
  text-align: left;
}
</style>
