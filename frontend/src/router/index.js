import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import BorrowKey from '../views/BorrowKey.vue'
import ReturnKey from '../views/ReturnKey.vue'
import UserManagement from '../views/UserManagement.vue'
import KeyManagement from '../views/KeyManagement.vue'

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
    path: '/users',
    name: 'UserManagement',
    component: UserManagement
  },
  {
    path: '/keys',
    name: 'KeyManagement',
    component: KeyManagement
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router