import { createRouter, createWebHistory } from 'vue-router'
import Auth from '../pages/Auth.vue'
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path:'/auth',
      name: 'auth',
      component: Auth
    }, 
  ],
})

export default router
