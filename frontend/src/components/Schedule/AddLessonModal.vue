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
        <label for="subjectName" class="span-input">Название предмета:</label>
        <input 
          id="subjectName"
          v-model="newLesson.subject_name" 
          type="text" 
          placeholder="Введите название предмета"
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
        <label for="room" class="span-input">Аудитория:</label>
        <input 
          id="room"
          v-model="newLesson.room" 
          type="text" 
          placeholder="Введите номер аудитории"
          class="registr-input"
        >
      </div>

      <div class="form-group">
        <label class="span-input">Повторять занятие:</label>
        <div class="repeat-options">
          <label class="checkbox-label">
            <input 
              type="checkbox" 
              v-model="newLesson.repeatWeekly"
              @change="updateRepeatDates"
            >
            Каждую неделю в этот же день
          </label>
        </div>
      </div>

      <div class="form-group" v-if="newLesson.repeatWeekly">
        <label class="span-input">Количество недель:</label>
        <input 
          v-model="newLesson.weeksCount" 
          type="number" 
          min="1" 
          max="12"
          class="registr-input"
          @change="updateRepeatDates"
        >
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
import { ref, reactive, computed, watch } from 'vue';
import { formatDate, formatDateYMD } from '../../utils/dateUtils';

const props = defineProps({
  date: Date
});

const emit = defineEmits(['close', 'save']);

const newLesson = reactive({
  subject_name: '',
  teacher_name: '',
  room: '',
  repeatWeekly: false,
  weeksCount: 4,
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
         newLesson.room.trim();
});

// Обновление дат повторения
const updateRepeatDates = () => {
  if (!props.date) return;
  
  const dates = [formatDateYMD(props.date)];
  
  if (newLesson.repeatWeekly) {
    for (let i = 1; i < newLesson.weeksCount; i++) {
      const nextDate = new Date(props.date);
      nextDate.setDate(nextDate.getDate() + (i * 7));
      dates.push(formatDateYMD(nextDate));
    }
  }
  
  newLesson.dates = dates;
};

// Сохранение занятия
const saveLesson = () => {
  if (!isFormValid.value) return;
  
  const lessonData = {
    subject_name: newLesson.subject_name,
    teacher_name: newLesson.teacher_name,
    room: newLesson.room,
    dates: newLesson.dates
  };
  
  emit('save', lessonData);
};

// Сброс формы при изменении даты
watch(() => props.date, () => {
  if (props.date) {
    updateRepeatDates();
  }
}, { immediate: true });
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playpen+Sans:wght@100..800&family=Stick&display=swap');

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
  font-family: "Stick", sans-serif;
}

.modal-content {
  background-color: #D3C5E5;
  border-radius: 15px;
  padding: 30px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

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
  font-family: "Stick", sans-serif;
  transition: border-color 0.3s;
  background: white;
  color: #333;
}

.registr-input:focus {
  outline: none;
  border-color: #4a2d7c;
}

.registr-input::placeholder {
  color: #aaa;
}

.repeat-options {
  margin-top: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  cursor: pointer;
  color: #5d4b7a;
  font-size: 14px;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  transform: scale(1.2);
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
  font-family: "Stick", sans-serif;
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
  font-family: "Stick", sans-serif;
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
}
</style>