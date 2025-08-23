<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <button class="modal-close" @click="$emit('close')">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
          <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
        </svg>
      </button>
      
      <h2>{{ lesson?.subject_name }}</h2>
      
      <div class="modal-details">
        <div class="detail-row">
          <span class="detail-label">Дата:</span>
          <span class="detail-value">{{ formattedDate }}</span>
        </div>
        
        <div class="detail-row">
          <span class="detail-label">Преподаватель:</span>
          <span class="detail-value">{{ lesson?.teacher_name }}</span>
        </div>
        
        <div class="detail-row">
          <span class="detail-label">Аудитория:</span>
          <span class="detail-value">{{ lesson?.room }}</span>
        </div>
        
        <div class="detail-row">
          <span class="detail-label">Дни проведения:</span>
          <span class="detail-value">
            {{ lesson?.dates.join(', ') }}
          </span>
        </div>
        
        <div class="detail-row full-width">
          <span class="detail-label">Описание:</span>
          <span class="detail-value">
            {{ description }}
          </span>
        </div>

        <!-- Блок комментариев -->
        <div class="detail-row full-width" v-if="comments.length > 0">
          <span class="detail-label">Комментарии:</span>
          <div class="comments-section">
            <div 
              v-for="(comment, index) in comments" 
              :key="index"
              class="comment-item"
            >
              {{ comment.comment }}
            </div>
          </div>
        </div>

        <!-- Форма добавления комментария -->
        <div class="detail-row full-width">
          <span class="detail-label">Добавить комментарий:</span>
          <div class="comment-form">
            <textarea 
              v-model="newComment" 
              placeholder="Введите ваш комментарий..."
              class="comment-textarea"
              rows="3"
            ></textarea>
            <button 
              @click="addNewComment" 
              class="submit-button small"
              :disabled="!newComment.trim()"
            >
              Добавить
            </button>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button class="action-button secondary" @click="$emit('close')">
          Закрыть
        </button>
        <button class="action-button danger" @click="$emit('delete')">
          Удалить
        </button>
        <button class="action-button primary" @click="$emit('add-to-calendar')">
          Добавить в календарь
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { formatDate, formatDateYMD } from '../../utils/dateUtils';

const props = defineProps({
  lesson: Object,
  date: Date,
  comments: Array,
  subjectDescriptions: Object
});

const emit = defineEmits(['close', 'delete', 'add-to-calendar', 'add-comment']);

const newComment = ref('');

const formattedDate = computed(() => {
  return props.date ? formatDate(props.date, { 
    weekday: 'long', 
    day: 'numeric', 
    month: 'long',
    year: 'numeric'
  }) : '';
});

const description = computed(() => {
  return props.subjectDescriptions?.[props.lesson?.subject_name] || 
         'Описание предмета отсутствует.';
});

// Добавление нового комментария
const addNewComment = () => {
  if (!newComment.value.trim() || !props.lesson || !props.date) return;
  
  const commentData = {
    lesson_id: generateLessonId(props.lesson, formatDateYMD(props.date)),
    date: formatDateYMD(props.date),
    comment: newComment.value.trim()
  };
  
  emit('add-comment', commentData);
  newComment.value = '';
};

// Генерация ID для занятия
const generateLessonId = (lesson, dateStr) => {
  return `${lesson.subject_name}-${lesson.teacher_name}-${lesson.room}-${dateStr}`.hashCode();
};
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
  margin-bottom: 20px;
  text-align: center;
  font-size: 24px;
  font-weight: 700;
}

.modal-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 25px;
}

.detail-row {
  display: flex;
  align-items: flex-start;
}

.detail-row.full-width {
  flex-direction: column;
  gap: 8px;
}

.detail-label {
  font-weight: 600;
  color: #4a2d7c;
  min-width: 120px;
  flex-shrink: 0;
  font-size: 16px;
}

.detail-value {
  color: #5d4b7a;
  flex: 1;
  font-size: 15px;
  line-height: 1.4;
}

/* Стили для комментариев */
.comments-section {
  margin-top: 10px;
}

.comment-item {
  padding: 12px;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  border-left: 3px solid #ffa726;
  font-size: 14px;
  color: #5d4b7a;
}

.comment-form {
  margin-top: 10px;
}

.comment-textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #9f8cb9;
  border-radius: 8px;
  font-family: "Stick", sans-serif;
  font-size: 14px;
  resize: vertical;
  margin-bottom: 10px;
}

.comment-textarea:focus {
  outline: none;
  border-color: #4a2d7c;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.action-button {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-family: "Stick", sans-serif;
  font-weight: 600;
  transition: all 0.3s;
}

.action-button.primary {
  background: #4a2d7c;
  color: white;
}

.action-button.primary:hover {
  background: #3a225f;
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

.submit-button.small {
  padding: 8px 16px;
  font-size: 14px;
  background-color: #4a2d7c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-family: "Stick", sans-serif;
  font-weight: 600;
  transition: background-color 0.3s;
}

.submit-button.small:hover:not(:disabled) {
  background-color: #3a225f;
}

.submit-button.small:disabled {
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

  .action-button {
    width: 100%;
    text-align: center;
  }

  .detail-row {
    flex-direction: column;
    gap: 5px;
  }

  .detail-label {
    min-width: auto;
  }
  
  .modal-content h2 {
    font-size: 22px;
  }
}
</style>