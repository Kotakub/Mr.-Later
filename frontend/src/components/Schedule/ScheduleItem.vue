<template>
  <div class="schedule-item" @click="$emit('item-click', item)">
    <div class="subject">{{ item.subject_name }}</div>
    <div class="teacher">Преподаватель: {{ item.teacher_name }}</div>
    <div class="room">Аудитория: {{ item.room }}</div>
    <div v-if="hasComments" class="comment-indicator">
      💬
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  },
  hasComments: {
    type: Boolean,
    default: false
  }
});

defineEmits(['item-click']);
</script>

<style scoped>
.schedule-item {
  padding: 18px;
  border-radius: 12px;
  background: white;
  margin-bottom: 15px;
  border-left: 5px solid #4a2d7c;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  font-family: "Stick", sans-serif;
  position: relative;
}

.schedule-item:hover {
  background: #f8f5ff;
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.12);
}

.schedule-item:last-child {
  margin-bottom: 15px;
}

.subject {
  font-weight: 700;
  font-size: 17px;
  color: #4a2d7c;
  margin-bottom: 8px;
}

.teacher, .room {
  font-size: 15px;
  color: #666;
  margin-bottom: 5px;
}

.teacher {
  color: #5d4b7a;
}

.room {
  color: #6a5a8a;
  font-weight: 600;
}

.comment-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 16px;
}
</style>