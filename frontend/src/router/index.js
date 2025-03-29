import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/Login/Login.vue';
import Home from '@/views/Home/Home.vue';
import MyTasks from '@/views/MyTask/MyTask.vue';
import Register from '@/views/Register/Register.vue';

const routes = [
  {
    path: '/',
    redirect: (to) => {
      // 根据登录状态动态跳转
      return localStorage.getItem('jwtToken')
        ? { name: 'Home' }
        : { name: 'Login' };
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false } // 添加元信息
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/tasks',
    name: 'MyTasks',
    component: MyTasks,
    meta: {
      requiresAuth: true,
      title: '我的任务列表'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 改进后的导航守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('jwtToken');

  // 退出登录后访问根路径
  if (to.path === '/' && !isAuthenticated) {
    next({ name: 'Login' });
    return;
  }

  // 需要登录且未认证
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({
      name: 'Login',
      query: { redirect: to.fullPath }
    });
    return;
  }

  // 已登录时访问登录页
  if (to.name === 'Login' && isAuthenticated) {
    next({ name: 'Home' });
    return;
  }

  next();
});

export default router;
