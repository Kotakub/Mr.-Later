<template>
  <div>
    <h1>{{ message }}</h1>
    <button @click="fetchData">Get Data from FastAPI</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: "Hello Vue!",
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/hello");
        this.message = response.data.message;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>