<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { fetchTasks, updateTaskStatus, deleteTask as apiDeleteTask } from '@/api/auth';
import { ElMessage, ElMessageBox } from 'element-plus';
import EditTask from '@/views/EditTask/EditTask.vue';

// 任务列表
const tasks = ref([]);
const activeTaskId = ref(null);
const deleting = ref(false);
const router = useRouter();

// 获取 EditTask 组件实例
const editTaskRef = ref(null);

// 定义 openEditDialog 方法
const openEditDialog = (task) => {
  if (editTaskRef.value) {
    editTaskRef.value.openDialog(task); // 调用 EditTask 的 openDialog 方法
  }
};

// 加载任务
const loadTasks = async () => {
  try {
    const response = await fetchTasks();
    tasks.value = response || [];
  } catch (error) {
    ElMessage.error("加载任务失败");
  }
};

// 标记任务完成
const markTaskComplete = async (task) => {
  try {
    await updateTaskStatus(task.id);
    ElMessage.success("任务已标记完成");
    await loadTasks();
  } catch (error) {
    ElMessage.error(error.message || "操作失败");
    console.error("标记完成错误:", error);
  }
};

// 删除任务
const deleteTask = async (task) => {
  try {
    const confirm = await ElMessageBox.confirm('确认删除？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });

    if (confirm !== 'confirm') return;

    await apiDeleteTask(task.id);
    ElMessage.success("删除成功");
    await loadTasks();
  } catch (error) {
    console.error('完整错误对象:', error);
    if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请检查网络');
    } else if (error.response) {
      ElMessage.error(`后端错误: ${error.response.data.detail}`);
    } else if (error.request) {
      console.log('请求已发出但无响应:', error.request);
      ElMessage.error('服务器无响应');
    } else {
      ElMessage.error('请求配置错误');
    }
  }
};

// 返回首页
const goBack = () => {
  router.push({ name: "Home" });
};

// 初始化加载任务
onMounted(() => {
  loadTasks();
});
</script>

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
    <AddTask @task-added="loadTasks" />

    <!-- 添加编辑任务组件 -->
    <EditTask ref="editTaskRef" @task-updated="loadTasks" />

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
            <div class="task-actions">
              <el-button
                v-if="task.status === '未完成'"
                type="success"
                @click="markTaskComplete(task)"
                class="complete-button">
                标记完成
              </el-button>
              <el-button
                type="primary"
                @click="openEditDialog(task)"
                class="edit-button">
                编辑任务
              </el-button>
              <el-button
                :loading="deleting"
                type="danger"
                @click="deleteTask(task)">
                删除任务
              </el-button>
            </div>
          </el-card>
        </el-collapse-item>
        <div v-if="tasks.length === 0" class="no-tasks">
          暂无任务
        </div>
      </el-collapse>
      <el-button
        type="primary"
        @click="goBack"
        style="margin-top: 20px;">
        返回首页
      </el-button>
    </div>
  </div>
</template>

<style src="./MyTask.css" scoped></style>
