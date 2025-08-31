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
        :show-add-button="false"
        @day-click="changeDay(-1)"
        @item-click="openModal($event, prevDate)"
      />

      <ScheduleDay
        :title="formatDate(currentDate)"
        :items="getScheduleForDate(currentDate)"
        day-type="current-day"
        :show-add-button="true"
        @item-click="openModal($event, currentDate)"
        @add-click="openAddLessonModal(currentDate)"
      />

      <ScheduleDay
        :title="formatDate(nextDate)"
        :items="getScheduleForDate(nextDate)"
        day-type="next-day"
        :clickable="true"
        :show-add-button="false"
        @day-click="changeDay(1)"
        @item-click="openModal($event, nextDate)"
      />
    </div>

    <LessonModal
      v-if="isModalOpen"
      :lesson="selectedItem"
      :date="selectedDate"
      :comments="getCommentsForLesson(selectedItem)"
      @close="closeModal"
      @delete="deleteLesson"
      @save="updateLesson"
    />

    <AddLessonModal
      v-if="isAddModalOpen"
      :date="addLessonDate"
      @close="closeAddModal"
      @save="addNewLesson"
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

// Данные расписания с lesson_id и comments
const schedule = ref({
  "monday": [
    {
      'lesson_id': 0,
      'dates': ['2025-08-01','2025-08-08'],
      'subject_name': 'Математика',
      'teacher_name': 'Иванов И.И.',
      'room': '101',
      'start_time': '09:00',
      'end_time': '10:30',
      'description': 'Изучение алгебры и геометрии'
    }
  ],
  "tuesday": [
    {
      'lesson_id': 1,
      'dates': ['2025-08-02','2025-08-09'],
      'subject_name': 'Физика',
      'teacher_name': 'Петров П.П.',
      'room': '202',
      'start_time': '11:00',
      'end_time': '12:30',
      'description': 'Механика и термодинамика'
    },
    {
      'lesson_id': 2,
      'dates': ['2025-08-03','2025-08-10'],
      'subject_name': 'Химия',
      'teacher_name': 'Сидоров С.С.',
      'room': '303',
      'start_time': '14:00',
      'end_time': '15:30',
      'description': 'Органическая химия'
    }
  ],
  "wednesday": [],
  "thursday": [],
  "friday": [],
  "saturday": [],
  "sunday": [],
  "comments": [
    {
      "lesson_id": 0,
      "date": '2025-08-08',
      "comment": "Заметка"
    }
  ]
});

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

// Получение комментариев для занятия
const getCommentsForLesson = (lesson) => {
  if (!lesson) return [];
  return schedule.value.comments?.filter(comment => comment.lesson_id === lesson.lesson_id) || [];
};

// Генерация нового ID для занятия
const generateNewLessonId = () => {
  let maxId = 0;
  Object.keys(schedule.value).forEach(day => {
    if (Array.isArray(schedule.value[day])) {
      schedule.value[day].forEach(lesson => {
        if (lesson.lesson_id > maxId) {
          maxId = lesson.lesson_id;
        }
      });
    }
  });
  return maxId + 1;
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

// Добавление нового занятия
const addNewLesson = (lessonData) => {
  const dayName = getDayName(addLessonDate.value);
  const dateStr = formatDateYMD(addLessonDate.value);
  
  if (!schedule.value[dayName]) {
    schedule.value[dayName] = [];
  }
  
  // Генерируем новый ID и добавляем дату
  const newLesson = {
    ...lessonData,
    lesson_id: generateNewLessonId(),
    dates: [dateStr]
  };
  
  schedule.value[dayName].push(newLesson);
  closeAddModal();
};

// Обновление существующего занятия
const updateLesson = (updatedLesson) => {
  const dayName = getDayName(selectedDate.value);
  
  const daySchedule = schedule.value[dayName];
  if (daySchedule) {
    const index = daySchedule.findIndex(item => item.lesson_id === selectedItem.value.lesson_id);
    
    if (index !== -1) {
      // Обновляем занятие, сохраняя lesson_id и dates
      daySchedule[index] = {
        ...daySchedule[index],
        ...updatedLesson
      };
    }
  }
  
  closeModal();
};

// Удаление занятия
const deleteLesson = () => {
  if (!selectedItem.value) return;
  
  const dayName = getDayName(selectedDate.value);
  
  const daySchedule = schedule.value[dayName];
  if (daySchedule) {
    // Удаляем занятие
    schedule.value[dayName] = daySchedule.filter(item => item.lesson_id !== selectedItem.value.lesson_id);
    
    // Удаляем связанные комментарии
    if (schedule.value.comments) {
      schedule.value.comments = schedule.value.comments.filter(comment => 
        comment.lesson_id !== selectedItem.value.lesson_id
      );
    }
  }
  
  closeModal();
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Chiron+GoRound+TC:wght@200..900&family=Playpen+Sans:wght@100..800&family=Stick&display=swap');

.schedule-app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: "Chiron GoRound TC", sans-serif;
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