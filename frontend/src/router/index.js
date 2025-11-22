import { createRouter, createWebHistory } from 'vue-router'
import SignIn from '@/pages/sign-in.vue'
import Book from '@/pages/Book.vue'
import Account from '@/pages/Account.vue'
import ReviewsAccount from '@/pages/ReviewsAccount.vue'

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
    },
    {
      path: '/account',
      name: 'Account',
      component: Account,
    },
    {
      path: '/reviews-account',
      name: 'reviewsAccount',
      component: ReviewsAccount,
    }

  ],

})

export default router
