import { createRouter, createWebHistory } from 'vue-router'
import SignIn from '@/pages/sign-in.vue'
import Book from '@/pages/Book.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/sign-in',
      name: 'SignIn',
      component: SignIn,
    },
    {
      path: '/book',
      name: 'Book',
      component: Book,
    }
  ],

})

export default router
