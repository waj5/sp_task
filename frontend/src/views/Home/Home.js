import { useRouter } from 'vue-router';

export const useHome = () => {
  const router = useRouter();

  const goToTasks = () => {
    router.push({ name: 'MyTasks' });
  };

  const logout = () => {
    localStorage.removeItem('jwtToken');
    router.push({ name: 'Login' });
  };

  return {
    goToTasks,
    logout,
  };
};
