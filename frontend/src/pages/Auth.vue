<template>
    <div class="auth-page">
        <div class="auth-window">
            <h1 class="title">
                АВТОРИЗАЦИЯ
            </h1>

            <span class="span-input">Почта или логин</span>
            <input 
                class="auth-input" 
                type="text"
                required
                id="username"
                v-model="formData.username"
                placeholder="example@mail.ru или ваш логин"
            />
            <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
            
            <span class="span-input">Пароль</span>
            <input 
                class="auth-input"
                type="password"
                required
                v-model="formData.password"
                id="password"
                placeholder="HvblcGqc"
            />
            <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
            
            <div class="login-prompt">
                Нету аккаунта? <span class="register-link" @click="navigateToRegistration">Зарегистрироваться</span>
            </div>
            
            <button class="submit-button" @click="handleSubmit" :disabled="isLoading">
                {{ isLoading ? 'ЗАГРУЗКА...' : 'ВОЙТИ' }}
            </button>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    
    const formData = ref({
      username: '',
      password: ''
    });
    
    const errors = ref({
      username: '',
      password: ''
    });
    
    const isLoading = ref(false);
    
    const validateForm = () => {
      let isValid = true;
      
      // Reset errors
      errors.value = { username: '', password: '' };
      
      // Validate username
      if (!formData.value.username.trim()) {
        errors.value.username = 'Почта или логин обязательны';
        isValid = false;
      }
      
      // Validate password
      if (!formData.value.password) {
        errors.value.password = 'Пароль обязателен';
        isValid = false;
      } else if (formData.value.password.length < 8) {
        errors.value.password = 'Пароль должен быть не менее 8 символов';
        isValid = false;
      }
      
      return isValid;
    };
    
    const handleSubmit = async () => {
      if (!validateForm()) return;
      
      isLoading.value = true;
      
      try {
        const response = await fetch('http://localhost:8000/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData.value)
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Ошибка аутентификации');
        }
        
        const data = await response.json();
        
        // Сохраняем токен в localStorage
        localStorage.setItem('auth_token', data.access_token);
        localStorage.setItem('user_data', JSON.stringify(data.user));
        
        console.log('Успешный вход:', data);
        
        // Перенаправляем на страницу расписания
        router.push(`/schedule/${data.user.login}`);
        
      } catch (error) {
        console.error('Ошибка входа:', error);
        errors.value.password = error.message || 'Неверные учетные данные';
      } finally {
        isLoading.value = false;
      }
    };
    
    const navigateToRegistration = () => {
      router.push('/registration');
    };
    
    return {
      formData,
      errors,
      isLoading,
      handleSubmit,
      navigateToRegistration
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playpen+Sans:wght@100..800&family=Stick&display=swap');

.auth-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f5f5;
    font-family: "Stick", sans-serif;
}

.auth-window {
    display: flex;
    flex-direction: column;
    width: 400px;
    padding: 30px;
    background-color: #D3C5E5;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.title {
    font-size: 24px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 25px;
    color: #4a2d7c;
}

.span-input {
    font-size: 16px;
    margin-bottom: 8px;
    color: #333;
}

.auth-input {
    padding: 12px 15px;
    margin-bottom: 5px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
    font-family: "Stick", sans-serif;
    transition: border-color 0.3s;
}

.auth-input:focus {
    outline: none;
    border-color: #4a2d7c;
}

.auth-input::placeholder {
    color: #aaa;
}

.error-message {
    color: #ff0000;
    font-size: 14px;
    margin-bottom: 15px;
    display: block;
}

.login-prompt {
    margin-top: 10px;
    margin-bottom: 20px;
    text-align: center;
    font-size: 14px;
}

.register-link {
    color: #4a2d7c;
    text-decoration: none;
    margin-left: 5px;
    font-weight: 600;
    cursor: pointer;
}

.register-link:hover {
    text-decoration: underline;
}

.submit-button {
    background-color: #4a2d7c;
    color: white;
    border: none;
    padding: 14px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    font-family: "Stick", sans-serif;
    cursor: pointer;
    transition: background-color 0.3s;
}

.submit-button:hover:not(:disabled) {
    background-color: #3a225f;
}

.submit-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}
</style>