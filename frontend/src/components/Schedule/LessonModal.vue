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

      <div class="form-group">
        <label class="span-input">Описание занятия:</label>
        <textarea 
          v-model="editedLesson.description" 
          placeholder="Введите описание занятия..."
          class="registr-input textarea"
          rows="4"
        ></textarea>
      </div>

      <!-- Блок комментариев -->
      <div class="form-group" v-if="comments.length > 0">
        <label class="span-input">Комментарии:</label>
        <div class="comments-section">
          <div 
            v-for="(comment, index) in comments" 
            :key="index"
            class="comment-item"
          >
            <strong>{{ formatCommentDate(comment.date) }}:</strong> {{ comment.comment }}
          </div>
        </div>
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
import { reactive, computed, watch } from 'vue';
import { formatDate } from '../../utils/dateUtils';

const props = defineProps({
  lesson: Object,
  date: Date,
  comments: Array
});

const emit = defineEmits(['close', 'delete', 'save']);

const editedLesson = reactive({
  subject_name: '',
  teacher_name: '',
  room: '',
  start_time: '09:00',
  end_time: '10:30',
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
      description: newLesson.description || ''
    });
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

const formatCommentDate = (dateStr) => {
  const date = new Date(dateStr);
  return formatDate(date, { 
    day: 'numeric', 
    month: 'long'
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
  
  emit('save', editedLesson);
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
  margin-bottom: 20px;
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

.registr-input::placeholder {
  color: #aaa;
}

.textarea {
  resize: vertical;
  min-height: 100px;
  font-family: "Chiron GoRound TC", sans-serif;
}

/* Стили для комментариев */
.comments-section {
  margin-top: 10px;
}

.comment-item {
  padding: 12px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  margin-bottom: 8px;
  border-left: 3px solid #ffa726;
  font-size: 14px;
  color: #5d4b7a;
}

.comment-item:last-child {
  margin-bottom: 0;
}

/* Стили для времени */
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
  gap: 12px;
  justify-content: space-between;
  margin-top: 25px;
}

.action-button {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-family: "Chiron GoRound TC", sans-serif;
  font-weight: 600;
  transition: all 0.3s;
  flex: 1;
}

.action-button.secondary {
  background: #f8f9fa;
  color: #5d4b7a;
  border: 2px solid #9f8cb9;
}

.action-button.secondary:hover {
  background: #e9ecef;
}

.action-button.danger {
  background: #ff4757;
  color: white;
}

.action-button.danger:hover {
  background: #ff3742;
}

.submit-button {
  background-color: #4a2d7c;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  font-family: "Chiron GoRound TC", sans-serif;
  cursor: pointer;
  transition: background-color 0.3s;
  flex: 1;
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
  }

  .time-inputs {
    flex-direction: column;
    gap: 8px;
  }

  .time-separator {
    margin: 5px 0;
  }
  
  .modal-content h2 {
    font-size: 22px;
  }
}
</style>