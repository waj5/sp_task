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

    <!-- 添加任务组件 -->
    <AddTask ref="addTask" @task-added="handleTaskAdded" />

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
            </div>
          </template>
          <el-card class="task-detail-card">
            <div class="task-info">
              <p><strong>任务ID:</strong> {{ task.id }}</p>
              <p><strong>任务内容:</strong> {{ task.content }}</p>
              <p><strong>创建时间:</strong> {{ task.create_time }}</p>
              <p v-if="task.status === '已完成'">
                <strong>完成时间:</strong> {{ task.complete_time }}
              </p>
              <p v-else>
                <strong>状态:</strong> {{ task.status }}
              </p>
              <p><strong>负责人:</strong> {{ task.designee_name }}</p>
              <p><strong>创建人:</strong> {{ task.creator_name }}</p>
            </div>
             <el-button
              v-if="task.status === '未完成'"
              type="success"
              @click="markTaskComplete(task)"
              class="complete-button">
              标记完成
            </el-button>
             <el-button
              :loading="deleting"
              type="danger"
              @click="deleteTask(task)">
              删除任务
            </el-button>
          </el-card>
        </el-collapse-item>
        <div v-if="tasks.length === 0" class="no-tasks">
          暂无任务
        </div>
      </el-collapse>
      <el-button
        type="primary"
        @click="goBack"
        style="margin-top: 20px;"
      >
        返回首页
      </el-button>
    </div>
  </div>
</template>

<script>
import { fetchTasks,updateTaskStatus,deleteTask } from "../api/auth";
import { ElMessage } from "element-plus";
import AddTask from './AddTask.vue' // 导入组件


export default {
  name: "MyTasks",
  components: {
    AddTask // 注册组件
  },
  data() {
    return {
      tasks: [],
      activeTaskId: null
    };
  },
  data1() {
  return {
    deleting: false
  }
},
  methods: {
    // 修改后的菜单处理
    handleMenuSelect(index) {
      if (index === "1") {
        this.$refs.addTask.showDialog() // 调用子组件方法
      }
    },

    // 处理新增任务成功
    handleTaskAdded() {
      this.loadTasks() // 刷新任务列表
    },

    async markTaskComplete(task) {
      try {
        await updateTaskStatus(task.id)
        ElMessage.success("任务已标记完成")
        await this.loadTasks()
      } catch (error) {
        ElMessage.error(error.message || "操作失败")
        console.error("标记完成错误:", error)
      }
    },

    async loadTasks() {
      try {
        const response = await fetchTasks();
        this.tasks = response || []; // 直接使用返回的数组
      } catch (error) {
        ElMessage.error("加载任务失败");
      }
    },

    async deleteTask(task) {
      try {
        const confirm = await this.$confirm('确认删除？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        if (confirm !== 'confirm') return // 确认用户真实点击

        const response = await deleteTask(task.id)
        ElMessage.success("删除成功")
        await this.loadTasks()
      } catch (error) {
        console.error('完整错误对象:', error) // 添加详细日志
        if (error.code === 'ECONNABORTED') {
          ElMessage.error('请求超时，请检查网络')
        } else if (error.response) {
          ElMessage.error(`后端错误: ${error.response.data.detail}`)
        } else if (error.request) {
          console.log('请求已发出但无响应:', error.request)
          ElMessage.error('服务器无响应')
        } else {
          ElMessage.error('请求配置错误')
        }
      }
    },

    goBack() {
      this.$router.push({ name: "Home" })
    }
  },
  mounted() {
    this.loadTasks()
  }
};
</script>

<style>
.my-tasks-container {
  padding: 20px;
}

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
  padding: 10px;
  text-align: left;
}

.task-info p {
  margin: 5px 0;
}

.complete-button {
  margin-top: 10px;
}

.el-collapse-item__content {
  text-align: left;
}

.no-tasks {
  text-align: center;
  color: #999;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .el-dialog {
    width: 90% !important;
  }
}
</style>
