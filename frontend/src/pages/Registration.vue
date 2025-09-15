<template>
    <div class="auth-page">
        <div class="auth-window">
            <h1 class="title">
                РЕГИСТРАЦИЯ
            </h1>

            <span class="span-input">Логин</span>
            <input 
                class="auth-input" 
                type="text"
                required
                v-model="formData.login"
                placeholder="Ваш логин"
            />
            <span v-if="errors.login" class="error-message">{{ errors.login }}</span>

            <span class="span-input">Почта</span>
            <input 
                class="auth-input" 
                type="email"
                required
                v-model="formData.email"
                placeholder="example@mail.ru"
            />
            <span v-if="errors.email" class="error-message">{{ errors.email }}</span>

            <span class="span-input">Пароль</span>
            <input 
                class="auth-input"
                type="password"
                required
                v-model="formData.password"
                placeholder="Не менее 8 символов"
            />
            <span v-if="errors.password" class="error-message">{{ errors.password }}</span>

            <span class="span-input">Подтверждение пароля</span>
            <input 
                class="auth-input"
                type="password"
                required
                v-model="formData.confirmPassword"
                placeholder="Повторите пароль"
            />
            <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
            
            <div class="login-prompt">
                Уже есть аккаунт? <span class="register-link" @click="navigateToLogin">Войти</span>
            </div>
            
            <button class="submit-button" @click="handleSubmit" :disabled="isLoading">
                {{ isLoading ? 'РЕГИСТРАЦИЯ...' : 'ЗАРЕГИСТРИРОВАТЬСЯ' }}
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
      login: '',
      email: '',
      password: '',
      confirmPassword: ''
    });
    
    const errors = ref({
      login: '',
      email: '',
      password: '',
      confirmPassword: ''
    });
    
    const isLoading = ref(false);
    
    const validateForm = () => {
      let isValid = true;
      
      // Сброс ошибок
      errors.value = { login: '', email: '', password: '', confirmPassword: '' };
      
      // Проверка логина
      if (!formData.value.login.trim()) {
        errors.value.login = 'Логин обязателен';
        isValid = false;
      } else if (formData.value.login.length < 3) {
        errors.value.login = 'Логин должен быть не менее 3 символов';
        isValid = false;
      }
      
      // Проверка email
      if (!formData.value.email.trim()) {
        errors.value.email = 'Почта обязательна';
        isValid = false;
      } else if (!/^\S+@\S+\.\S+$/.test(formData.value.email)) {
        errors.value.email = 'Некорректный email';
        isValid = false;
      }
      
      // Проверка пароля
      if (!formData.value.password) {
        errors.value.password = 'Пароль обязателен';
        isValid = false;
      } else if (formData.value.password.length < 8) {
        errors.value.password = 'Пароль должен быть не менее 8 символов';
        isValid = false;
      }
      
      // Проверка подтверждения пароля
      if (!formData.value.confirmPassword) {
        errors.value.confirmPassword = 'Подтверждение пароля обязательно';
        isValid = false;
      } else if (formData.value.password !== formData.value.confirmPassword) {
        errors.value.confirmPassword = 'Пароли не совпадают';
        isValid = false;
      }
      
      return isValid;
    };
    
    const handleSubmit = async () => {
    if (!validateForm()) return;
    
    isLoading.value = true;
    
    try {
        const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            login: formData.value.login,
            email: formData.value.email,
            password: formData.value.password
        })
        });
        
        if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка регистрации');
        }
        
        const data = await response.json();
        
        // Сохраняем токен в localStorage
        localStorage.setItem('auth_token', data.access_token);
        
        console.log('Успешная регистрация:', data);
        
        // Перенаправляем на страницу расписания
        router.push(`/schedule/${data.user.login}`);
        
    } catch (error) {
        console.error('Ошибка регистрации:', error);
        
        // Обработка специфических ошибок с сервера
        if (error.message.includes('Email уже зарегистрирован')) {
        errors.value.email = error.message;
        } else if (error.message.includes('Логин уже занят')) {
        errors.value.login = error.message;
        } else {
        errors.value.password = 'Ошибка регистрации. Попробуйте еще раз.';
        }
    } finally {
        isLoading.value = false;
    }
    };
    
    const navigateToLogin = () => {
      router.push('/authorization');
    };
    
    return {
      formData,
      errors,
      isLoading,
      handleSubmit,
      navigateToLogin
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