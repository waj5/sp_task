<!-- views/MyTask/MyTask.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useMyTask } from './useMyTask'
import EditTask from '@/views/EditTask/EditTask.vue'
import AddTask from '@/views/AddTask/AddTask.vue'
import './MyTask.css';

// 组合式API
const {
  tasks,
  activeTaskId,
  deleting,
  loadTasks,
  markTaskComplete,
  deleteTaskHandler ,
  goBack
} = useMyTask()

// 子组件引用
const editTaskRef = ref(null)
const addTaskRef = ref(null)

// 菜单选择处理
const handleMenuSelect = (index) => {
  if (index === '1') {
    addTaskRef.value.showDialog()
  }
}

// 打开编辑对话框
const openEditDialog = (task) => {
  editTaskRef.value.openDialog(task)
}

// 初始化加载
onMounted(() => {
  loadTasks()
})
</script>

<template>
  <div class="my-tasks-container">
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
      <h1>我的任务</h1>

      <el-collapse v-model="activeTaskId" accordion>
        <el-collapse-item
          v-for="task in tasks"
          :key="task.id"
          :name="task.id"
        >
          <template #title>
            <div class="task-title">
              <span>{{ task.title }}</span>
              <el-tag
                :type="task.status === '已完成' ? 'success' : 'warning'"
                size="small"
              >
                {{ task.status }}
              </el-tag>
            </div>
          </template>

          <el-card class="task-detail-card">
            <div class="task-info">
              <p><strong>任务ID:</strong> {{ task.id }}</p>
              <p><strong>内容:</strong> {{ task.content }}</p>
              <p><strong>创建时间:</strong> {{ task.create_time }}</p>
              <p v-if="task.status === '已完成'">
                <strong>完成时间:</strong> {{ task.complete_time }}
              </p>
              <p><strong>负责人:</strong> {{ task.designee_name }}</p>
              <p><strong>创建人:</strong> {{ task.creator_name }}</p>
            </div>

            <div class="task-actions">
              <el-button
                v-if="task.status !== '已完成'"
                type="success"
                @click="markTaskComplete(task)"
              >
                标记完成
              </el-button>
              <el-button
                type="primary"
                @click="openEditDialog(task)"
              >
                编辑任务
              </el-button>
              <el-button
                type="danger"
                :loading="deleting"
                @click="deleteTaskHandler(task)"
              >
                删除任务
              </el-button>
            </div>
          </el-card>
        </el-collapse-item>

        <div v-if="tasks.length === 0" class="no-tasks">
          <el-empty description="暂无任务" />
        </div>
      </el-collapse>

      <el-button
        type="primary"
        @click="goBack"
        class="back-button"
      >
        返回首页
      </el-button>
    </div>
  </div>
</template>
