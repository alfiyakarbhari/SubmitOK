import { createRouter, createWebHistory } from 'vue-router'
import MainWelcome from '../components/MainWelcome.vue'

const routes = [
  {
    path: '/',
    name: 'welcome',
    component: MainWelcome
  },
  {
    path: '/login/user',
    name: 'user-login',
    component: () => import('../components/UserLogin.vue')
  },
  {
    path: '/login/teacher',
    name: 'teacher-login',
    component: () => import('../components/TeacherLogin.vue')
  },
  {
    path: '/dashboard/teacher',
    name: 'teacher-dashboard',
    component: () => import('../components/TeacherDashboard.vue') // <-- load from components
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
