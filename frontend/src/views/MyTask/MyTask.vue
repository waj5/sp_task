<!-- views/MyTask/MyTask.vue -->
<script setup>
import { onMounted } from 'vue'
import { useMyTask } from './useMyTask'
import EditTask from '@/views/EditTask/EditTask.vue'
import AddTask from '@/views/AddTask/AddTask.vue'
import './MyTask.css';

// 组合式API
const {
  tasks,
  activeTaskId,
  deleting,
  editTaskRef,
  addTaskRef,
  myTaskStyle,
  loadTasks,
  markTaskComplete,
  deleteTaskHandler,
  goBack,
  handleMenuSelect,
  openEditDialog,
  goToHome,
  logout
} = useMyTask()

// 初始化加载
onMounted(() => {
  loadTasks()
})
</script>

<template>
  <div class="my-tasks-container" :style="myTaskStyle">
    <!-- 左侧菜单 -->
    <el-menu
      class="side-menu"
      default-active="1"
      @select="handleMenuSelect"
    >
      <el-menu-item index="1">
        <span>添加任务</span>
      </el-menu-item>
    </el-menu>

    <!-- 添加任务组件 -->
    <AddTask
      ref="addTaskRef"
      @task-added="loadTasks"
    />

    <!-- 编辑任务组件 -->
    <EditTask
      ref="editTaskRef"
      @task-updated="loadTasks"
    />

    <!-- 主内容区 -->
    <div class="my-tasks">
      <div class="header">
        <h1>我的任务</h1>
        <div class="nav-buttons">
          <el-button type="primary" plain @click="goToHome">首页</el-button>
          <el-button type="primary">我的任务</el-button>
        </div>
        <div class="header-actions">
          <el-button type="danger" @click="logout">退出登录</el-button>
        </div>
      </div>

      <div class="task-grid">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="task-card"
          :style="{
            backgroundColor:`hsl(${Math.random()*360},70%,85%)`,
            transform: `rotateY(${Math.random()*10-5}deg)`
          }"
          @click="() => activeTaskId = task.id"
        >
          <div class="book-spine"></div>
          <div class="book-content">
            <h3>{{ task.title }}</h3>
            <div class="task-preview">
              <p><strong>负责人:</strong> {{ task.designee_name }}</p>
              <p><strong>状态:</strong> {{ task.status }}</p>
            </div>
          </div>
        </div>

        <div v-if="tasks.length === 0" class="no-tasks">
          <el-empty description="暂无任务" />
        </div>
      </div>

      <el-dialog
        v-model="activeTaskId"
        title="任务详情"
        width="70%"
        center
        class="book-dialog"
      >
        <div v-if="activeTaskId" class="task-details">
          <div class="book-cover">
            <div class="book-spine"></div>
            <div class="book-pages">
              <div class="book-left">
                <h3>{{ tasks.find(t => t.id === activeTaskId)?.title }}</h3>
                <div class="task-meta">
                  <p><strong>任务ID:</strong> {{ tasks.find(t => t.id === activeTaskId)?.id }}</p>
                  <p><strong>创建时间:</strong> {{ tasks.find(t => t.id === activeTaskId)?.create_time }}</p>
                  <p v-if="tasks.find(t => t.id === activeTaskId)?.status === '已完成'">
                    <strong>完成时间:</strong> {{ tasks.find(t => t.id === activeTaskId)?.complete_time }}
                  </p>
                  <p><strong>负责人:</strong> {{ tasks.find(t => t.id === activeTaskId)?.designee_name }}</p>
                  <p><strong>创建人:</strong> {{ tasks.find(t => t.id === activeTaskId)?.creator_name }}</p>
                </div>
              </div>
              <div class="book-right">
                <div class="task-content">
                  <h4>任务内容</h4>
                  <p>{{ tasks.find(t => t.id === activeTaskId)?.content }}</p>
                </div>
                <div class="task-actions">
                  <el-button
                    v-if="tasks.find(t => t.id === activeTaskId)?.status !== '已完成'"
                    type="success"
                    @click="markTaskComplete(tasks.find(t => t.id === activeTaskId))"
                  >
                    标记完成
                  </el-button>
                  <el-button
                    type="primary"
                    @click="openEditDialog(tasks.find(t => t.id === activeTaskId))"
                  >
                    编辑任务
                  </el-button>
                  <el-button
                    type="danger"
                    :loading="deleting"
                    @click="deleteTaskHandler(tasks.find(t => t.id === activeTaskId))"
                  >
                    删除任务
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-dialog>
    </div>
  </div>
</template>
