import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../views/Home.vue'
import MyTasks from '../views/MyTasks.vue'

const routes = [
  {
    path: '/',
    redirect: { name: 'Home' }, // 修改点4：默认跳转到任务页
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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 改进后的导航守卫
router.beforeEach((to, from, next) => {
     const isAuthenticated = localStorage.getItem('jwtToken');

     // 白名单机制
     const authWhitelist = ['Login'];

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

export default router
