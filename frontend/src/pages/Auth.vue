<script>
import { useRouter } from 'vue-router';

const router = useRouter();
</script>



<template>
    <div class="auth-window">
        <input 
            class="auth-input" 
            type="text"
            required
            id="login"
        />
        <input 
            class="auth-input"
            type="password"
            required
            id="password"
        />
        <button>Войти</button>
    </div>
</template>



<style>

</style>