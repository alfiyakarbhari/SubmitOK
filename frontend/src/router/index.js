import { createRouter, createWebHistory } from 'vue-router'
import { auth } from "@/firebase";
// Existing imports
import MainWelcome from '../components/MainWelcome.vue'
import TeacherPage from '@/components/TeacherPage.vue'
import VerifyEmail from "@/components/verify-email.vue";
import UserDashboard from "@/components/UserDashboard.vue";
import TeacherAssignments from "@/components/TeacherAssignments.vue";

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
    path: '/dashboard/user',   // <-- NEW ROUTE
    name: 'user-dashboard',
    component: () => import('../components/UserDashboard.vue')
  },
  {
    path: '/teacher/:teacherId',
    component: TeacherPage
  },
  {
    path: "/verify-email",
    name: "VerifyEmail",
    component: VerifyEmail
  },
  {
    path: "/dashboard",
    name: "UserDashboard",
    component: UserDashboard
  },
  {
    path: "/teacher-assignments/:teacherId",
    name: "TeacherAssignments",
    component: TeacherAssignments,
    props: true // allows route params as props
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Global guard to protect routes
// Global guard to protect routes
router.beforeEach((to, from, next) => {
  const user = auth.currentUser;

  // 🔒 Only protect USER dashboard (Firebase auth)
  const protectedRoutes = ['/dashboard', '/dashboard/user'];

  if (protectedRoutes.includes(to.path) && !user) {
    next('/login'); // redirect to login if not authenticated
  } else {
    next();
  }
});


export default router
