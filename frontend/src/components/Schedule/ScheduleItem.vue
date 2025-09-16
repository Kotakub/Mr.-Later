<template>
  <div class="schedule-item" @click="$emit('item-click', item)">
    <div class="header-row">
      <div class="time-badge" v-if="item.start_time && item.end_time">
        {{ item.start_time }} - {{ item.end_time }}
      </div>
      <div class="subject">{{ item.subject_name }}</div>
    </div>
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
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

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
const API_BASE_URL = 'http://localhost:8000';

// Форматируем дату для API
const formatDateForAPI = (date) => {
  return date.toISOString().split('T')[0];
};

// Проверяем, отмечено ли посещение для текущей даты
const checkAttendance = () => {
  if (!props.item.attendances || !Array.isArray(props.item.attendances)) {
    isAttended.value = false;
    return;
  }
  
  const currentDateStr = formatDateForAPI(props.currentDate);
  isAttended.value = props.item.attendances.includes(currentDateStr);
};

// Переключение статуса посещения
const toggleAttendance = async () => {
  isLoading.value = true;
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      alert('Для отметки посещения необходимо войти в систему');
      return;
    }

    const attendanceData = {
      lesson_id: props.item.id, // Используем id вместо lesson_id
      lesson_date: formatDateForAPI(props.currentDate)
    };

    const response = await axios.post(`${API_BASE_URL}/attendance`, attendanceData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    // Обновляем состояние на основе ответа сервера
    isAttended.value = response.data.attended;
    
    // Обновляем локальный массив attendances
    const currentDateStr = formatDateForAPI(props.currentDate);
    if (response.data.attended) {
      // Добавляем дату в attendances
      if (!props.item.attendances) {
        props.item.attendances = [];
      }
      if (!props.item.attendances.includes(currentDateStr)) {
        props.item.attendances.push(currentDateStr);
      }
    } else {
      // Удаляем дату из attendances
      if (props.item.attendances) {
        props.item.attendances = props.item.attendances.filter(date => date !== currentDateStr);
      }
    }
    
    // Отправляем событие родительскому компоненту
    emit('attendance-toggle', {
      lesson: props.item,
      date: props.currentDate,
      attended: isAttended.value
    });
    
  } catch (error) {
    console.error('Error toggling attendance:', error);
    if (error.response?.status === 401) {
      alert('Необходима авторизация для отметки посещения');
    } else {
      alert('Ошибка при отметке посещения: ' + (error.response?.data?.detail || error.message));
    }
  } finally {
    isLoading.value = false;
  }
};

// Следим за изменениями даты или элемента
watch(() => [props.currentDate, props.item], () => {
  checkAttendance();
}, { immediate: true, deep: true });

// Также проверяем статус при монтировании
onMounted(() => {
  checkAttendance();
});
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

.header-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 8px;
}

.time-badge {
  align-self: flex-end;
  background: #4a2d7c;
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
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