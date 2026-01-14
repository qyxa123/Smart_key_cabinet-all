import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import BorrowKey from '../views/BorrowKey.vue'
import ReturnKey from '../views/ReturnKey.vue'
import KeyManagement from '../views/KeyManagement.vue'
import BorrowRecords from '../views/BorrowRecords.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/borrow',
    name: 'BorrowKey',
    component: BorrowKey
  },
  {
    path: '/return',
    name: 'ReturnKey',
    component: ReturnKey
  },
  {
    path: '/keys',
    name: 'KeyManagement',
    component: KeyManagement
  },
  {
    path: '/records',
    name: 'BorrowRecords',
    component: BorrowRecords
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
