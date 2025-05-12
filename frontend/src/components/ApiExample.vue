<template>
  <div>
    <h1>{{ message }}</h1>
    <button @click="fetchData">Получить данные</button>
    <button @click="sendData">Отправить данные</button>
  </div>
</template>

<script>
import api from '@/api';

export default {
  data() {
    return {
      message: "Ожидание данных...",
    };
  },
  methods: {
    async fetchData() {
      try {
        const data = await api.getData();
        this.message = data.message;
      } catch (error) {
        this.message = "Ошибка запроса!";
      }
    },
    async sendData() {
      const response = await api.postData({ text: "Test" });
      console.log("Ответ от сервера:", response);
    },
  },
};
</script>