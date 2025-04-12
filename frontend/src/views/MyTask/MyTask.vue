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
  logout,
  dialogVisible,
  selectedTask,
  createDialogVisible,
  newTask,
  showTaskDetails,
  createTask,
  completeTask
} = useMyTask()

// 初始化加载
onMounted(() => {
  loadTasks()
})
</script>

<template>
  <div class="my-task" :style="myTaskStyle">
    <table class="page-layout">
      <tr>
        <td class="header-cell">
          <h1>我的任务</h1>
        </td>
      </tr>
      <tr>
        <td class="nav-cell">
          <div class="nav-buttons">
            <el-button type="primary" :plain="true" @click="goToHome">首页</el-button>
            <el-button type="primary" :plain="false">我的任务</el-button>
            <el-button type="success" @click="showCreateTaskDialog">新建任务</el-button>
          </div>
          <div class="header-actions">
            <el-button type="danger" @click="logout">退出登录</el-button>
          </div>
        </td>
      </tr>
      <tr>
        <td class="content-cell">
          <div class="task-grid">
            <div
              v-for="task in tasks"
              :key="task.id"
              class="task-card"
              @click="showTaskDetails(task)"
            >
              <div class="book-spine"></div>
              <div class="book-content">
                <div class="book-title">
                  <h3>{{task.title}}</h3>
                  <div class="book-author">{{ task.designee_name }}</div>
                </div>
                <div class="task-preview">
                  <div class="book-status">
                    <span class="status-label">状态:</span>
                    <span class="status-value">{{ task.status }}</span>
                  </div>
                  <div class="book-pages-indicator">
                    <span class="pages-dots"></span>
                    <span class="pages-dots"></span>
                    <span class="pages-dots"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </td>
      </tr>
    </table>

    <!-- 任务详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="任务详情"
      width="70%"
      center
      class="book-dialog"
      :modal-append-to-body="false"
      :append-to-body="true"
      :close-on-click-modal="false"
      :close-on-press-escape="true"
      :show-close="true"
      :destroy-on-close="true"
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
              <div class="task-actions" v-if="selectedTask.status !== '已完成'">
                <el-button type="success" @click="completeTask(selectedTask)">完成任务</el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 创建任务对话框 -->
    <el-dialog
      v-model="createDialogVisible"
      title="新建任务"
      width="50%"
      center
    >
      <el-form :model="newTask" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="newTask.title" placeholder="请输入任务标题"></el-input>
        </el-form-item>
        <el-form-item label="内容">
          <el-input
            v-model="newTask.content"
            type="textarea"
            :rows="4"
            placeholder="请输入任务内容"
          ></el-input>
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="newTask.designee_name" placeholder="请输入负责人姓名"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createTask">创建</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style src="./MyTask.css"></style>
