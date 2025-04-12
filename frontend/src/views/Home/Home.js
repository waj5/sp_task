// Home.js
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { fetchAllTasks } from '@/api/auth';

export function useHome() {
  const route = useRoute();
  const router = useRouter();
  const randomTasks = ref([]);
  const selectedTask = ref(null);
  const dialogVisible = ref(false);
  const loading = ref(false);

  // 判断当前是否在首页
  const isHome = computed(() => route.path === '/');

  // 背景图片样式
  const homeStyle = computed(() => ({
    '--home-bg-image': `url('${import.meta.env.VITE_HOME_BG_IMAGE}')`
  }));

  // 获取所有任务
  // Home.js
const getAllTasks = async () => {
  loading.value = true;
  try {
    const response = await fetchAllTasks();
    console.log('获取到的任务数据:', response);
    // 确保返回一个数组
    if (response && response.tasks) {
      return response.tasks; // 如果数据在 tasks 字段中
    } else if (Array.isArray(response)) {
      return response; // 如果响应本身就是数组
    } else {
      console.error('任务数据格式不正确:', response);
      return [];
    }
  } catch (error) {
    console.error('获取任务失败:', error);
    ElMessage.error(error.message || '获取任务失败，请稍后重试');
    return [];
  } finally {
    loading.value = false;
  }
};

  // 随机打乱数组
  const shuffleArray = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  };

  // 跳转到任务页面
  const goToTasks = () => {
    router.push('/tasks');
  };

  // 退出登录
  const logout = () => {
    localStorage.removeItem('jwtToken');
    router.push('/login');
  };

  // 显示任务详情
  const showTaskDetails = (task) => {
    selectedTask.value = task;
    dialogVisible.value = true;
  };

  return {
    randomTasks,
    selectedTask,
    dialogVisible,
    isHome,
    homeStyle,
    getAllTasks,
    shuffleArray,
    goToTasks,
    logout,
    showTaskDetails
  };
}