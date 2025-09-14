<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <button class="modal-close" @click="$emit('close')">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
          <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
        </svg>
      </button>
      
      <h2>Редактирование занятия</h2>
      <p class="modal-subtitle">Дата: {{ formattedDate }}</p>
      
      <div class="form-group">
        <label class="span-input">Название предмета:</label>
        <input 
          v-model="editedLesson.subject_name" 
          type="text" 
          placeholder="Введите название предмета"
          class="registr-input"
        >
      </div>

      <div class="form-group">
        <label class="span-input">Преподаватель:</label>
        <input 
          v-model="editedLesson.teacher_name" 
          type="text" 
          placeholder="Введите ФИО преподавателя"
          class="registr-input"
        >
      </div>

      <div class="form-group">
        <label class="span-input">Место проведения:</label>
        <input 
          v-model="editedLesson.room" 
          type="text" 
          placeholder="Введите место проведения"
          class="registr-input"
        >
      </div>

      <div class="form-group time-group">
        <label class="span-input">Время проведения:</label>
        <div class="time-inputs">
          <input 
            v-model="editedLesson.start_time" 
            type="time" 
            class="registr-input time-input"
          >
          <span class="time-separator">—</span>
          <input 
            v-model="editedLesson.end_time" 
            type="time" 
            class="registr-input time-input"
          >
        </div>
      </div>

      <div class="form-group date-group">
        <label class="span-input">Дата окончания:</label>
        <div class="date-inputs">
          <input 
            v-model="editedLesson.end_date" 
            type="date" 
            class="registr-input date-input"
          >
        </div>
      </div>

      <div class="form-group">
        <label class="span-input">Описание занятия:</label>
        <textarea 
          v-model="editedLesson.description" 
          placeholder="Введите описание занятия..."
          class="registr-input textarea"
          rows="4"
        ></textarea>
      </div>

      <div class="modal-actions">
        <button class="action-button danger" @click="$emit('delete')">
          Удалить
        </button>
        <button class="action-button secondary" @click="$emit('close')">
          Отмена
        </button>
        <button 
          class="submit-button" 
          @click="saveChanges"
          :disabled="!isFormValid"
        >
          Сохранить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, watch, ref } from 'vue';
import { formatDate, formatDateYMD } from '../../utils/dateUtils';

const props = defineProps({
  lesson: Object,
  date: Date,
  comments: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['close', 'delete', 'save']);

const currentDate = ref(props.date ? new Date(props.date) : new Date());

const editedLesson = reactive({
  subject_name: '',
  teacher_name: '',
  room: '',
  start_time: '09:00',
  end_time: '10:30',
  start_date: '',
  end_date: '',
  description: '',
  new_comment: '',
  dayOfWeek: '',
  repeat: 'none'
});

// Инициализация формы при открытии модального окна
watch(() => props.lesson, (newLesson) => {
  if (newLesson) {
    Object.assign(editedLesson, {
      subject_name: newLesson.subject_name || '',
      teacher_name: newLesson.teacher_name || '',
      room: newLesson.room || '',
      start_time: newLesson.start_time || '09:00',
      end_time: newLesson.end_time || '10:30',
      start_date: newLesson.start_date || '',
      end_date: newLesson.end_date || '',
      description: newLesson.description || '',
      dayOfWeek: newLesson.dayOfWeek || '',
      repeat: newLesson.repeat || 'none',
      new_comment: '' // Сбрасываем комментарий при каждом открытии
    });
    
    // Если время в формате HH:MM:SS, обрезаем секунды
    if (editedLesson.start_time && editedLesson.start_time.includes(':')) {
      editedLesson.start_time = editedLesson.start_time.substring(0, 5);
    }
    if (editedLesson.end_time && editedLesson.end_time.includes(':')) {
      editedLesson.end_time = editedLesson.end_time.substring(0, 5);
    }
  }
}, { immediate: true });

const formattedDate = computed(() => {
  return props.date ? formatDate(props.date, { 
    weekday: 'long', 
    day: 'numeric', 
    month: 'long',
    year: 'numeric'
  }) : '';
});

const formatCommentDate = (dateObj) => {
  if (typeof dateObj === 'string') {
    dateObj = new Date(dateObj);
  }
  return formatDate(dateObj, { 
    day: 'numeric', 
    month: 'long',
    year: 'numeric'
  });
};

const isFormValid = computed(() => {
  return editedLesson.subject_name.trim() && 
         editedLesson.teacher_name.trim() && 
         editedLesson.room.trim() &&
         editedLesson.start_time &&
         editedLesson.end_time;
});

// Сохранение изменений
const saveChanges = () => {
  if (!isFormValid.value) return;
  
  // Создаем объект с данными для сохранения
  const saveData = {
    ...editedLesson,
    comment: editedLesson.new_comment.trim() // Добавляем комментарий если он есть
  };
  
  emit('save', saveData);
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Chiron+GoRound+TC:wght@200..900&family=Playpen+Sans:wght@100..800&family=Stick&display=swap');

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
  font-family: "Chiron GoRound TC", sans-serif;
}

.modal-content {
  position: relative;
  background-color: #D3C5E5;
  border-radius: 15px;
  padding: 30px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  box-sizing: border-box;
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
  font-family: "Chiron GoRound TC", sans-serif;
  transition: border-color 0.3s;
  background: white;
  color: #333;
  box-sizing: border-box;
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

.date-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-input {
  flex: 1;
  text-align: center;
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

.action-button.danger {
  background-color: #ff4757;
  color: white;
  border: none;
}

.action-button.danger:hover {
  background-color: #ff3742;
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

.comments-section {
  max-height: 200px;
  overflow-y: auto;
  margin-top: 10px;
}

.comment-item {
  padding: 10px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 6px;
  margin-bottom: 8px;
  border-left: 3px solid #ffa726;
  font-size: 13px;
  color: #5d4b7a;
}

.comment-item:last-child {
  margin-bottom: 0;
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

  .date-inputs {
    flex-direction: column;
    gap: 8px;
  }
}
</style>