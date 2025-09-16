<template>
  <div class="schedule-navigation">
    <div class="nav-left">
      <button 
        v-if="user" 
        class="user-login-btn"
        @click="goToMySchedule"
      >
        {{ user.login }}
      </button>
      <span v-else class="app-title">Расписание занятий</span>
    </div>
    
    <div class="nav-right">
      <button 
        v-if="user" 
        class="logout-btn"
        @click="logout"
      >
        Выйти
      </button>
      <button 
        v-else 
        class="login-btn"
        @click="goToLogin"
      >
        Войти
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
const props = defineProps({
  user: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['logout']);

const goToMySchedule = () => {
  if (props.user) {
    router.push(`/schedule/${props.user.login}`);
  }
};

const goToLogin = () => {
  router.push('/authorization');
};

const logout = () => {
  emit('logout');
};
</script>

<style scoped>
.schedule-navigation {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: #4a2d7c;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-left, .nav-right {
  display: flex;
  align-items: center;
}

.app-title {
  color: white;
  font-family: "Chiron GoRound TC", sans-serif;
  font-weight: 600;
  font-size: 18px;
}

.user-login-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-family: "Chiron GoRound TC", sans-serif;
  font-weight: 600;
  transition: all 0.3s ease;
}

.user-login-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.login-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-family: "Chiron GoRound TC", sans-serif;
  font-weight: 600;
  transition: all 0.3s ease;
}

.login-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.logout-btn {
  background: #ff4757;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-family: "Chiron GoRound TC", sans-serif;
  font-weight: 600;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: #ff3742;
  transform: translateY(-2px);
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .schedule-navigation {
    padding: 0 15px;
    height: 50px;
  }
  
  .user-login-btn,
  .logout-btn,
  .login-btn {
    padding: 6px 12px;
    font-size: 14px;
  }
  
  .app-title {
    font-size: 16px;
  }
}
</style>