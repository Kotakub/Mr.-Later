<template>
  <div class="schedule-app">
    <h1 class="title">Расписание занятий</h1>
    
    <WeekNavigation
      :current-date="currentDate"
      :week-days="weekDays"
      :schedule="schedule"
      @prev-week="changeWeek(-1)"
      @next-week="changeWeek(1)"
      @day-select="currentDate = $event"
    />
    
    <div class="schedule-container">
      <ScheduleDay
        :title="formatDate(prevDate)"
        :items="getScheduleForDate(prevDate)"
        day-type="prev-day"
        :clickable="true"
        @day-click="changeDay(-1)"
        @item-click="openModal($event, prevDate)"
        @add-click="openAddLessonModal(prevDate)"
      />

      <ScheduleDay
        :title="formatDate(currentDate)"
        :items="getScheduleForDate(currentDate)"
        day-type="current-day"
        @item-click="openModal($event, currentDate)"
        @add-click="openAddLessonModal(currentDate)"
      />

      <ScheduleDay
        :title="formatDate(nextDate)"
        :items="getScheduleForDate(nextDate)"
        day-type="next-day"
        :clickable="true"
        @day-click="changeDay(1)"
        @item-click="openModal($event, nextDate)"
        @add-click="openAddLessonModal(nextDate)"
      />
    </div>

    <LessonModal
      v-if="isModalOpen"
      :lesson="selectedItem"
      :date="selectedDate"
      :comments="getCommentsForLesson(selectedItem, selectedDate)"
      :subject-descriptions="subjectDescriptions"
      @close="closeModal"
      @delete="deleteLesson"
      @add-to-calendar="addToCalendar"
      @add-comment="addComment"
    />

    <AddLessonModal
      v-if="isAddModalOpen"
      :date="addLessonDate"
      @close="closeAddModal"
      @save="saveNewLesson"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import WeekNavigation from '../components/Schedule/WeekNavigation.vue';
import ScheduleDay from '../components/Schedule/ScheduleDay.vue';
import LessonModal from '../components/Schedule/LessonModal.vue';
import AddLessonModal from '../components/Schedule/AddLessonModal.vue';
import { 
  getMonday, 
  formatDate, 
  getDayName, 
  formatDateYMD 
} from '../utils/dateUtils';

const currentDate = ref(new Date());
const currentWeekStart = ref(getMonday(new Date()));
const isModalOpen = ref(false);
const isAddModalOpen = ref(false);
const selectedItem = ref(null);
const selectedDate = ref(null);
const addLessonDate = ref(null);

// Данные расписания с комментариями
const schedule = ref({
  "monday": [
    {
      'dates': ['2025-08-01','2025-08-08'],
      'subject_name': 'Математика',
      'teacher_name': 'Иванов И.И.',
      'room': '101'
    }
  ],
  "tuesday": [
    {
      'dates': ['2025-08-02','2025-08-09'],
      'subject_name': 'Физика',
      'teacher_name': 'Петров П.П.',
      'room': '202'
    },
    {
      'dates': ['2025-08-23','2025-08-10'],
      'subject_name': 'Химия',
      'teacher_name': 'Сидоров С.С.',
      'room': '303'
    }
  ],
  "wednesday": [],
  "thursday": [],
  "friday": [],
  "saturday": [
    {
      'dates': ['2025-08-02','2025-08-09'],
      'subject_name': 'Физика',
      'teacher_name': 'Петров П.П.',
      'room': '202'
    },
    {
      'dates': ['2025-08-23','2025-08-10'],
      'subject_name': 'Химия',
      'teacher_name': 'Сидоров С.С.',
      'room': '303'
    }
  ],
  "sunday": [],
  "comments": [
    {
      'lesson_id': 0,
      'date': '2025-08-23',
      'comment': 'comment'
    }
  ],
});

// Описания предметов
const subjectDescriptions = {
  'Математика': 'Изучение чисел, структур, пространства и изменений. Включает алгебру, геометрию, математический анализ.',
  'Физика': 'Наука о природе, изучающая материю, её движение и поведение в пространстве и времени.',
  'Химия': 'Наука о веществах, их составе, строении, свойствах и превращениях.'
};

// Дни текущей недели
const weekDays = computed(() => {
  const days = [];
  for (let i = 0; i < 7; i++) {
    const date = new Date(currentWeekStart.value);
    date.setDate(date.getDate() + i);
    days.push({ date });
  }
  return days;
});

// Обновляем текущую неделю при изменении даты
watch(currentDate, (newDate) => {
  currentWeekStart.value = getMonday(newDate);
});

// Вычисляемые даты для предыдущего и следующего дня
const prevDate = computed(() => {
  const date = new Date(currentDate.value);
  date.setDate(date.getDate() - 1);
  return date;
});

const nextDate = computed(() => {
  const date = new Date(currentDate.value);
  date.setDate(date.getDate() + 1);
  return date;
});

// Функции навигации
const changeDay = (days) => {
  const newDate = new Date(currentDate.value);
  newDate.setDate(newDate.getDate() + days);
  currentDate.value = newDate;
};

const changeWeek = (weeks) => {
  const newDate = new Date(currentWeekStart.value);
  newDate.setDate(newDate.getDate() + (weeks * 7));
  currentWeekStart.value = newDate;
  currentDate.value = new Date(newDate);
};

// Получение расписания для конкретной даты
const getScheduleForDate = (date) => {
  const dayName = getDayName(date);
  const dateStr = formatDateYMD(date);
  
  const daySchedule = schedule.value[dayName] || [];
  
  // Фильтруем занятия по датам
  return daySchedule.filter(item => {
    return item.dates.includes(dateStr);
  });
};

// Получение комментариев для конкретного занятия
const getCommentsForLesson = (lesson, date) => {
  if (!lesson || !date) return [];
  
  const dateStr = formatDateYMD(date);
  const lessonId = generateLessonId(lesson, dateStr);
  
  return schedule.value.comments?.filter(comment => 
    comment.lesson_id === lessonId && comment.date === dateStr
  ) || [];
};

// Генерация ID для занятия
const generateLessonId = (lesson, dateStr) => {
  return `${lesson.subject_name}-${lesson.teacher_name}-${lesson.room}-${dateStr}`.hashCode();
};

// Добавление комментария
const addComment = (commentData) => {
  if (!schedule.value.comments) {
    schedule.value.comments = [];
  }
  schedule.value.comments.push(commentData);
};

// Открытие модального окна с деталями
const openModal = (item, date) => {
  selectedItem.value = item;
  selectedDate.value = date;
  isModalOpen.value = true;
};

// Закрытие модального окна с деталями
const closeModal = () => {
  isModalOpen.value = false;
  selectedItem.value = null;
  selectedDate.value = null;
};

// Открытие модального окна добавления занятия
const openAddLessonModal = (date) => {
  addLessonDate.value = date;
  isAddModalOpen.value = true;
};

// Закрытие модального окна добавления занятия
const closeAddModal = () => {
  isAddModalOpen.value = false;
  addLessonDate.value = null;
};

// Сохранение нового занятия
const saveNewLesson = (lessonData) => {
  const dayName = getDayName(addLessonDate.value);
  
  if (!schedule.value[dayName]) {
    schedule.value[dayName] = [];
  }
  
  schedule.value[dayName].push(lessonData);
  closeAddModal();
};

// Удаление занятия
const deleteLesson = () => {
  if (!selectedItem.value || !selectedDate.value) return;
  
  const dayName = getDayName(selectedDate.value);
  const dateStr = formatDateYMD(selectedDate.value);
  
  schedule.value[dayName] = schedule.value[dayName].filter(item => 
    !(item.subject_name === selectedItem.value.subject_name &&
      item.teacher_name === selectedItem.value.teacher_name &&
      item.room === selectedItem.value.room &&
      item.dates.includes(dateStr))
  );
  
  closeModal();
};

// Добавление в календарь
const addToCalendar = () => {
  alert('Функция добавления в календарь будет реализована позже!');
};

// Хэш-функция для генерации ID
String.prototype.hashCode = function() {
  let hash = 0;
  for (let i = 0; i < this.length; i++) {
    const char = this.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return hash;
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playpen+Sans:wght@100..800&family=Stick&display=swap');

.schedule-app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: "Stick", sans-serif;
}

.title {
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 30px;
  color: #4a2d7c;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.schedule-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 25px;
}

@media (max-width: 768px) {
  .schedule-container {
    flex-direction: column;
    gap: 20px;
  }
  
  .title {
    font-size: 28px;
    margin-bottom: 25px;
  }
}
</style>