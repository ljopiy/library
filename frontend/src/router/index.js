import { createRouter, createWebHistory } from 'vue-router'
import SidnIn from '@/views/sign-in.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/sign-in',
      name: 'SignIn',
      component: SignIn,
    }
  ],
})

export default router
