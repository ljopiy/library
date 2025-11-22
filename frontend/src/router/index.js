import { createRouter, createWebHistory } from 'vue-router'
import SignIn from '@/pages/sign-in.vue'
import Book from '@/pages/Book.vue'
import Account from '@/pages/Account.vue'
import ReviewsAccount from '@/pages/ReviewsAccount.vue'
import MainLayout from '@/layouts/paddingLayout.vue'
import BookCollection from '@/pages/bookCollection.vue'
import Map from '@/components/map.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainLayout',
      component: MainLayout,
      children: [
        {
          path: '/book',
          name: 'Book',
          component: Book,
        },
        {
          path: '/book-collection',
          name: 'BookCollection',
          component: BookCollection,
        },
        {
          path: '/account',
          name: 'Account',
          component: Account,
        },
        {
          path: '/reviews-account',
          name: 'reviewsAccount',
          component: ReviewsAccount
        },
      ]
    },
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
      path: '/map',
      name: 'Map',
      component: Map,
    }
  ],

})

export default router
