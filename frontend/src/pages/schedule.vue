<script>
import api from '@/api/index.js';

export default {
  methods: {
    async fetchData() {
      const data = await api.getHello();
      console.log(data);
    },
  },
};
</script>