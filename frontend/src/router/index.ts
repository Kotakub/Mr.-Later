import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'root',
      redirect: () => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          try {
            const userData = localStorage.getItem('user_data');
            if (userData) {
              const user = JSON.parse(userData);
              return `/schedule/${user.login}`;
            }
            const payload = JSON.parse(atob(token.split('.')[1]));
            const login = payload.sub.split('@')[0];
            return `/schedule/${login}`;
          } catch (error) {
            console.error('Error parsing user data:', error);
            return '/authorization';
          }
        }
        return '/authorization';
      }
    },
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
      
    }
  ],
})

export default router