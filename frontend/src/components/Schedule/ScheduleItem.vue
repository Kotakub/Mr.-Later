<template>
  <div class="schedule-item" @click="$emit('item-click', item)">
    <div class="time-badge" v-if="item.start_time && item.end_time">
      {{ item.start_time }} - {{ item.end_time }}
    </div>
    <div class="subject">{{ item.subject_name }}</div>
    <div class="teacher">Преподаватель: {{ item.teacher_name }}</div>
    <div class="room">Аудитория: {{ item.room }}</div>
    
    <!-- Кнопка отметки посещения -->
    <div class="attendance-control" v-if="showAttendanceButton">
      <button 
        class="attendance-button"
        :class="{ 'attended': isAttended }"
        @click.stop="toggleAttendance"
        :disabled="isLoading"
      >
        <span v-if="isLoading">...</span>
        <span v-else>{{ isAttended ? '✓ Присутствовал' : 'Отметиться' }}</span>
      </button>
    </div>
    
    <div v-if="hasComments" class="comment-indicator">
      💬
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  hasComments: {
    type: Boolean,
    default: false
  },
  showAttendanceButton: {
    type: Boolean,
    default: true
  },
  currentDate: {
    type: Date,
    default: () => new Date()
  }
});

const emit = defineEmits(['item-click', 'attendance-toggle']);

const isLoading = ref(false);
const isAttended = ref(false);

// Проверяем статус посещения при монтировании
onMounted(() => {
  checkAttendanceStatus();
});

// Функция для проверки статуса посещения
const checkAttendanceStatus = async () => {
  try {
    // Здесь будет запрос к API для проверки статуса посещения
    // Временно используем localStorage для демонстрации
    const attendanceKey = `attendance_${props.item.lesson_id}_${props.currentDate.toISOString().split('T')[0]}`;
    isAttended.value = localStorage.getItem(attendanceKey) === 'true';
  } catch (error) {
    console.error('Error checking attendance:', error);
  }
};

// Переключение статуса посещения
const toggleAttendance = async () => {
  isLoading.value = true;
  try {
    // Инвертируем текущее состояние
    const newStatus = !isAttended.value;
    
    // Здесь будет запрос к API для сохранения статуса посещения
    // Временно используем localStorage для демонстрации
    const attendanceKey = `attendance_${props.item.lesson_id}_${props.currentDate.toISOString().split('T')[0]}`;
    localStorage.setItem(attendanceKey, newStatus.toString());
    
    isAttended.value = newStatus;
    
    // Отправляем событие родительскому компоненту
    emit('attendance-toggle', {
      lesson: props.item,
      date: props.currentDate,
      attended: newStatus
    });
    
  } catch (error) {
    console.error('Error toggling attendance:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Chiron+GoRound+TC:wght@200..900&family=Playpen+Sans:wght@100..800&family=Stick&display=swap');

.schedule-item {
  padding: 18px;
  border-radius: 12px;
  background: white;
  margin-bottom: 15px;
  border-left: 5px solid #4a2d7c;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  font-family: "Chiron GoRound TC", sans-serif;
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

.time-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #4a2d7c;
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.subject {
  font-weight: 700;
  font-size: 17px;
  color: #4a2d7c;
  margin-bottom: 8px;
  padding-right: 80px;
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
  bottom: 10px;
  right: 10px;
  font-size: 16px;
}

/* Стили для кнопки отметки посещения */
.attendance-control {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.attendance-button {
  width: 100%;
  padding: 8px 12px;
  border: 2px solid #4a2d7c;
  border-radius: 6px;
  background: white;
  color: #4a2d7c;
  font-family: "Chiron GoRound TC", sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.attendance-button:hover:not(:disabled) {
  background: #f0e6ff;
}

.attendance-button.attended {
  background: #4a2d7c;
  color: white;
  border-color: #4a2d7c;
}

.attendance-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>