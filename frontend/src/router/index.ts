import { createRouter, createWebHistory } from 'vue-router';
import { defineAsyncComponent } from 'vue';

const Auth = defineAsyncComponent(() => import('../pages/Auth.vue'));
const Schedule = defineAsyncComponent(() => import('../pages/Schedule.vue'));
const Registr = defineAsyncComponent(() => import('../pages/Registration.vue'));

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path:'/authorization',
      name: 'authorization',
      component: Auth
    },
    {
      path: '/registration',
      name: 'registration',
      component: Registr
    },
    {
      path: '/schedule',
      name: 'schedule',
      component: Schedule
    },
  ],
})

export default router
