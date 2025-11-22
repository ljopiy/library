import { createRouter, createWebHistory } from 'vue-router'
import SignIn from '@/pages/sign-in.vue'
import Book from '@/pages/Book.vue'
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
        }
      ]
    },
    {
      path: '/sign-in',
      name: 'SignIn',
      component: SignIn,
    },
    {
      path: '/map',
      name: 'Map',
      component: Map,
    }
  ],

})

export default router
