  // src/utils/taskLogic.js
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
        emit('show-add-task');
      }
    };

    // 其他逻辑保持不变
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
