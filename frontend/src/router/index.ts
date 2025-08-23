import { createRouter, createWebHistory } from 'vue-router';
import Auth from '../pages/Auth.vue';
import Regist from '../pages/Registation.vue';
import Schedule from '../pages/Schedule.vue'
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path:'/authorization',
      name: 'authorization',
      component: Auth
    },
    {
      path:'/registration',
      name: 'registration',
      component: Regist
    },
    {
      path: '/schedule',
      name: 'schedule',
      component: Schedule
    },
  ],
})

export default router
