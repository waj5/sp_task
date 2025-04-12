import { useRouter } from 'vue-router';
import {fetchAllTasks} from "@/api/auth";

export const useHome = () => {
  const router = useRouter();
  const getAllTasks = async () => {
    try {
      const response = await fetchAllTasks();
      console.log('接口原始响应:', response);
      return response?.tasks || [];
    } catch (error) {
      console.error('获取任务失败:', error);
      return [];
    }
  };

  const goToTasks = () => {
    router.push({ name: 'MyTasks' });
  };

  const logout = () => {
    localStorage.removeItem('jwtToken');
    router.push({ name: 'Login' });
  };

  const shuffleArray = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};

  return {
    goToTasks,
    logout,
    getAllTasks,
    shuffleArray,
  };
};
