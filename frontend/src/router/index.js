import { createRouter, createWebHistory } from 'vue-router'

// Existing imports
import MainWelcome from '../components/MainWelcome.vue'
import TeacherPage from '@/components/TeacherPage.vue'
import VerifyEmail from "@/components/verify-email.vue";

const routes = [
  {
    path: '/',
    name: 'welcome',
    component: MainWelcome
  },

  // -----------------------------
  // USER AUTH (NEW – FIXED)
  // -----------------------------
  {
    path: '/login',
    name: 'login',
    component: () => import('@/components/LoginPage.vue')
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('@/components/SignupPage.vue')
  },

  // -----------------------------
  // EXISTING ROUTES (UNCHANGED)
  // -----------------------------
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
    component: () => import('../components/TeacherDashboard.vue')
  },
  {
    path: '/teacher/:teacherId',
    component: TeacherPage
  },
  {
    path: "/verify-email",
    name: "VerifyEmail",
    component: VerifyEmail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
