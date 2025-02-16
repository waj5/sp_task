import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../views/Home.vue'
import MyTasks from '../views/MyTasks.vue'

const routes = [
  {
    path: '/',
    redirect: '/login', // 默认重定向到登录页
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
  path: '/tasks',
  name: 'MyTasks', // 命名路由
  component: MyTasks,
 },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 添加全局导航守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token'); // 获取 token

  if (to.name !== 'Login' && !token) {
    // 如果未登录且访问的不是登录页，则重定向到登录页
    next({ name: 'Login' });
  } else {
    next(); // 否则放行
  }
});

export default router;