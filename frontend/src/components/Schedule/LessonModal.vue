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

      <!-- Поле для нового комментария -->
      <div class="form-group">
        <label class="span-input">Комментарий на {{ formatCommentDate(currentDate) }}:</label>
        <textarea 
          v-model="editedLesson.new_comment" 
          placeholder="Введите комментарий для этой даты..."
          class="registr-input textarea"
          rows="3"
        ></textarea>
      </div>

      <!-- Блок существующих комментариев -->
      <div class="form-group" v-if="comments.length > 0">
        <label class="span-input">Предыдущие комментарии:</label>
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
import { reactive, computed, watch, ref } from 'vue';
import { formatDate, formatDateYMD } from '../../utils/dateUtils';

const props = defineProps({
  lesson: Object,
  date: Date,
  comments: Array
});

const emit = defineEmits(['close', 'delete', 'save']);

const currentDate = ref(props.date ? new Date(props.date) : new Date());

const editedLesson = reactive({
  subject_name: '',
  teacher_name: '',
  room: '',
  start_time: '09:00',
  end_time: '10:30',
  description: '',
  new_comment: '', // Добавляем поле для нового комментария
  dayOfWeek: '' // Добавляем день недели
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
      description: newLesson.description || '',
      dayOfWeek: newLesson.dayOfWeek || '',
      new_comment: '' // Сбрасываем комментарий при каждом открытии
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

const formatCommentDate = (dateObj) => {
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
/* Стили остаются без изменений, только добавляем для нового комментария */
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
</style>