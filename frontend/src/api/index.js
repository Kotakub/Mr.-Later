import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',  // Адрес FastAPI
});

export default {
    async getData() {
        const response = await api.get('/data');
        return response.data;
    },
    async postData(payload) {
        const response = await api.post('/data', payload);
        return response.data;
    },
};