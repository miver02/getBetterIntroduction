// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '../view/index.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: IndexView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router