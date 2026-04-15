import { createRouter, createWebHistory } from 'vue-router'

import { authState, restoreSession } from '../services/auth'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        guestOnly: true,
      },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: {
        guestOnly: true,
      },
    },
  ],
})

router.beforeEach(async (to) => {
  if (to.meta.requiresAuth) {
    if (!authState.token) {
      return {
        name: 'login',
        query: {
          redirect: to.fullPath,
        },
      }
    }

    try {
      await restoreSession()
      return true
    } catch {
      return {
        name: 'login',
        query: {
          redirect: to.fullPath,
        },
      }
    }
  }

  if (to.meta.guestOnly && authState.token) {
    try {
      await restoreSession()
      return {
        name: 'home',
      }
    } catch {
      return true
    }
  }

  return true
})

export default router
