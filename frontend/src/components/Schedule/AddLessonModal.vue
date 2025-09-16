<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <button class="modal-close" @click="$emit('close')">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
          <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
        </svg>
      </button>
      
      <h2>Добавить новое занятие</h2>
      <p class="modal-subtitle">Дата: {{ formattedDate }}</p>
      
      <div class="form-group">
        <label for="subjectName" class="span-input">Название занятия:</label>
        <input 
          id="subjectName"
          v-model="newLesson.subject_name" 
          type="text" 
          placeholder="Введите название занятия"
          class="registr-input"
        >
      </div>

      <div class="form-group">
        <label for="teacherName" class="span-input">Преподаватель:</label>
        <input 
          id="teacherName"
          v-model="newLesson.teacher_name" 
          type="text" 
          placeholder="Введите ФИО преподавателя"
          class="registr-input"
        >
      </div>

      <div class="form-group">
        <label for="room" class="span-input">Место проведения:</label>
        <input 
          id="room"
          v-model="newLesson.room" 
          type="text" 
          placeholder="Введите место проведения"
          class="registr-input"
        >
      </div>

      <div class="form-group time-group">
        <label class="span-input">Время проведения:</label>
        <div class="time-inputs">
          <input 
            v-model="newLesson.start_time" 
            type="time" 
            class="registr-input time-input"
          >
          <span class="time-separator">—</span>
          <input 
            v-model="newLesson.end_time" 
            type="time" 
            class="registr-input time-input"
          >
        </div>
      </div>

      <div class="form-group date-group">
        <label class="span-input">Дата окончания:</label>
        <div class="date-inputs">
          <input 
            v-model="newLesson.end_date" 
            type="date" 
            class="registr-input date-input"
          >
        </div>
      </div>

      <div class="form-group">
        <label class="span-input">Повторение занятия:</label>
        <select v-model="newLesson.repeat" class="registr-input">
          <option value="none">Не повторять</option>
          <option value="weekly">Каждую неделю</option>
          <option value="biweekly">Каждые 2 недели</option>
        </select>
      </div>

      <div class="modal-actions">
        <button class="action-button secondary" @click="$emit('close')">
          Отмена
        </button>
        <button 
          class="submit-button" 
          @click="saveLesson"
          :disabled="!isFormValid"
        >
          Сохранить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { formatDate, formatDateYMD } from '../../utils/dateUtils';

const props = defineProps({
  date: Date
});

const emit = defineEmits(['close', 'save']);

const newLesson = reactive({
  subject_name: '',
  teacher_name: '',
  room: '',
  start_time: '09:00',
  end_time: '10:30',
  end_date: '',
  repeat: 'none',
  comment: '',
  dates: []
});

const formattedDate = computed(() => {
  return props.date ? formatDate(props.date, { 
    weekday: 'long', 
    day: 'numeric', 
    month: 'long',
    year: 'numeric'
  }) : '';
});

const isFormValid = computed(() => {
  return newLesson.subject_name.trim() && 
         newLesson.teacher_name.trim() && 
         newLesson.room.trim() &&
         newLesson.start_time &&
         newLesson.end_time;
});

// Сохранение занятия
const saveLesson = () => {
  if (!isFormValid.value) return;
  
  const lessonData = {
    subject_name: newLesson.subject_name,
    teacher_name: newLesson.teacher_name,
    room: newLesson.room,
    start_time: newLesson.start_time,
    end_time: newLesson.end_time,
    end_date: newLesson.end_date,
    repeat: newLesson.repeat,
    comment: newLesson.comment,
    dates: [formatDateYMD(props.date)]
  };
  
  // Добавляем повторяющиеся даты если нужно
  if (newLesson.repeat !== 'none') {
    const weeks = newLesson.repeat === 'weekly' ? 1 : 2;
    for (let i = 1; i <= 4; i++) {
      const nextDate = new Date(props.date);
      nextDate.setDate(nextDate.getDate() + (i * 7 * weeks));
      lessonData.dates.push(formatDateYMD(nextDate));
    }
  }
  
  emit('save', lessonData);
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Chiron+GoRound+TC:wght@200..900&family=Playpen+Sans:wght@100..800&family=Stick&display=swap');



.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: background-color 0.3s;
  color: #4a2d7c;
}

.modal-close:hover {
  background: rgba(74, 45, 124, 0.1);
}

.modal-content h2 {
  color: #4a2d7c;
  margin-bottom: 15px;
  text-align: center;
  font-size: 24px;
  font-weight: 700;
}

.modal-subtitle {
  color: #5d4b7a;
  margin-bottom: 25px;
  font-size: 16px;
  text-align: center;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

.span-input {
  font-size: 16px;
  margin-bottom: 8px;
  color: #4a2d7c;
  font-weight: 600;
  display: block;
}

.registr-input {
  padding: 12px 15px;
  width: 100%;
  border: 2px solid #9f8cb9;
  border-radius: 8px;
  font-size: 16px;
  font-family: "Chiron GoRound TC", sans-serif;
  transition: border-color 0.3s;
  background: white;
  color: #333;
}

.registr-input:focus {
  outline: none;
  border-color: #4a2d7c;
}

.textarea {
  resize: vertical;
  min-height: 80px;
}

.time-group {
  margin-bottom: 25px;
}

.time-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-input {
  flex: 1;
  text-align: center;
}

.time-separator {
  color: #5d4b7a;
  font-weight: 600;
  font-size: 18px;
}

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 25px;
}

.action-button {
  padding: 12px 25px;
  border: 2px solid #4a2d7c;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-family: "Chiron GoRound TC", sans-serif;
  font-weight: 600;
  transition: all 0.3s;
  background: white;
  color: #4a2d7c;
}

.action-button:hover {
  background: #4a2d7c;
  color: white;
}

.submit-button {
  background-color: #4a2d7c;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  font-family: "Chiron GoRound TC", sans-serif;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover:not(:disabled) {
  background-color: #3a225f;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  position: relative;
  background-color: #D3C5E5;
  border-radius: 15px;
  padding: 30px;
  max-width: 50%;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin: 0 auto; /* Центрирование */
  
  box-sizing: border-box;
  overflow-x: hidden;
}
@media (max-width: 768px) {
  .modal-content {
    
    margin: 10px;
    padding: 25px;
  }

  .modal-actions {
    flex-direction: column;
  }

  .action-button, .submit-button {
    width: 100%;
    text-align: center;
  }
  
  .modal-content h2 {
    font-size: 22px;
  }
  
  .modal-subtitle {
    font-size: 14px;
  }

  .time-inputs {
    flex-direction: column;
    gap: 8px;
  }

  .time-separator {
    margin: 5px 0;
  }
}
.date-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-input {
  flex: 1;
  text-align: center;
}
</style>