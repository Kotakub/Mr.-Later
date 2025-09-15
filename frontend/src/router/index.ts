import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/authorization',
      name: 'authorization',
      component: () => import('../pages/Auth.vue'),
    },
    {
      path: '/registration',
      name: 'registration',
      component: () => import('../pages/Registration.vue'),
    },
    {
      path: '/schedule/:login',
      name: 'Schedule',
      component: () => import('../pages/Schedule.vue'),
      meta: { requiresAuth: false }
    }
  ],
})

export default router