<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    
    const formData = ref({
      login: '',
      email: '',
      password: ''
    });
    
    const errors = ref({
      login: '',
      email: '',
      password: ''
    });
    
    const validateForm = () => {
      let isValid = true;
      
      // Reset errors
      errors.value = { login: '', email: '', password: '' };
      
      // Validate login
      if (!formData.value.login.trim()) {
        errors.value.login = 'Логин обязателен';
        isValid = false;
      } else if (formData.value.login.length < 3) {
        errors.value.login = 'Логин слишком короткий';
        isValid = false;
      }
      
      // Validate email
      if (!formData.value.email.trim()) {
        errors.value.email = 'Почта обязательна';
        isValid = false;
      } else if (!/^\S+@\S+\.\S+$/.test(formData.value.email)) {
        errors.value.email = 'Некорректный email';
        isValid = false;
      }
      
      // Validate password
      if (!formData.value.password) {
        errors.value.password = 'Пароль обязателен';
        isValid = false;
      } else if (formData.value.password.length < 6) {
        errors.value.password = 'Пароль должен быть не менее 6 символов';
        isValid = false;
      }
      
      return isValid;
    };
    
    const handleSubmit = () => {
      if (validateForm()) {
        // Здесь обычно отправка данных на сервер
        console.log('Форма отправлена:', formData.value);
        
        // После успешной регистрации перенаправляем на страницу входа
        router.push('/authorization');
      }
    };
    
    const navigateToLogin = () => {
      router.push('/authorization');
    };
    
    return {
      formData,
      errors,
      handleSubmit,
      navigateToLogin
    };
  }
};
</script>

<template>
    <div class="registr-page">
        <div class="registr-window">
            <span class="title">
                РЕГИСТРАЦИЯ
            </span>

            <span class="span-input">Логин</span>
            <input 
                class="registr-input" 
                type="text"
                required
                id="login"
                v-model="formData.login"
                placeholder="MrLater"
            />
            <span v-if="errors.login" class="error-message">{{ errors.login }}</span>
            
            <span class="span-input">Почта</span>
            <input 
                class="registr-input" 
                type="text"
                required
                id="email"
                v-model="formData.email"
                placeholder="example@mail.ru"
            />
            <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
            
            <span class="span-input">Пароль</span>
            <input 
                class="registr-input"
                type="password"
                required
                v-model="formData.password"
                id="password"
                placeholder="HvblcGqc"
            />
            <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
            
            <div class="login-prompt">
                Есть аккаунт? <span class="register-link" @click="navigateToLogin">Войти</span>
            </div>
            
            <button class="submit-button" @click="handleSubmit">
                ЗАРЕГИСТРИРОВАТЬСЯ
            </button>
        </div>
    </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playpen+Sans:wght@100..800&family=Stick&display=swap');

.registr-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f5f5;
    font-family: "Stick", sans-serif;
}

.registr-window {
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

.registr-input {
    padding: 12px 15px;
    margin-bottom: 20px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
    font-family: "Stick", sans-serif;
    transition: border-color 0.3s;
}

.registr-input:focus {
    outline: none;
    border-color: #4a2d7c;
}

.registr-input::placeholder {
    color: #aaa;
}

.register-link {
    color: #4a2d7c;
    text-decoration: none;
    margin-left: 5px;
    font-weight: 600;
}

.register-link:hover {
    text-decoration: underline;
}

.submit-button {
    background-color: #4a2d7c;
    color: white;
    border: none;
    padding: 14px;
    margin-top: 20px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    font-family: "Stick", sans-serif;
    cursor: pointer;
    transition: background-color 0.3s;
}

.submit-button:hover {
    background-color: #3a225f;
}
</style>