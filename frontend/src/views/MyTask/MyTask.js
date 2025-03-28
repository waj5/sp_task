import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { fetchTasks, updateTaskStatus, deleteTask as apiDeleteTask } from '@/api/auth';
import { ElMessage, ElMessageBox } from 'element-plus';

export function useTaskLogic() {
  const tasks = ref([]);
  const activeTaskId = ref(null);
  const deleting = ref(false);
  const router = useRouter();

  const handleMenuSelect = (index) => {
    if (index === "1") {
      // 通过事件触发添加任务对话框
      emit('show-add-task');
    }
  };

  const handleTaskUpdated = () => {
    loadTasks();
  };

  const handleTaskAdded = () => {
    loadTasks();
  };

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

  const loadTasks = async () => {
    try {
      const response = await fetchTasks();
      tasks.value = response || [];
    } catch (error) {
      ElMessage.error("加载任务失败");
    }
  };

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

  const goBack = () => {
    router.push({ name: "Home" });
  };

  return {
    tasks,
    activeTaskId,
    deleting,
    handleMenuSelect,
    handleTaskUpdated,
    handleTaskAdded,
    markTaskComplete,
    loadTasks,
    deleteTask,
    goBack
  };
}
