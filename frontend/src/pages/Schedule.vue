<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRouter, useRoute  } from 'vue-router';
import axios from 'axios';
import WeekNavigation from '../components/Schedule/WeekNavigation.vue';
import ScheduleDay from '../components/Schedule/ScheduleDay.vue';
import LessonModal from '../components/Schedule/LessonModal.vue';
import AddLessonModal from '../components/Schedule/AddLessonModal.vue';
import Navigation from '../components/Schedule/Navigation.vue';
import { 
  getMonday, 
  formatDate, 
  getDayName, 
  formatDateYMD,
  formatTime 
} from '../utils/dateUtils';

const router = useRouter();
const API_BASE_URL = 'http://localhost:8000';

// Состояния
const currentDate = ref(new Date());
const currentWeekStart = ref(getMonday(new Date()));
const isModalOpen = ref(false);
const isAddModalOpen = ref(false);
const selectedItem = ref(null);
const selectedDate = ref(null);
const addLessonDate = ref(null);
const isLoading = ref(false);
const error = ref(null);
const isViewingOwnSchedule = ref(true);
const saveButtonVisible = ref(false);
const route = useRoute();

// Данные с бэкенда
const scheduleData = ref([]);

// Текущий пользователь
const currentUser = ref(null);
const isLoadingUser = ref(true);

// Функция для выхода из аккаунта
const handleLogout = () => {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user_data');
  router.push('/authorization');
};

// Функция для получения информации о пользователе из токена
const getCurrentUserFromToken = () => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      throw new Error('No token found');
    }

    // Добавляем токен в заголовки axios по умолчанию
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    // Парсим payload из JWT токена
    const payload = JSON.parse(atob(token.split('.')[1]));
    
    // В вашем токене в sub хранится email, но нам нужен login
    // Будем получать информацию о пользователе через защищенный эндпоинт
    return {
      email: payload.sub,
      // Временно используем email как login, пока не получим данные с сервера
      login: payload.sub.split('@')[0] 
    };

  } catch (err) {
    console.error('Error parsing token:', err);
    localStorage.removeItem('auth_token');
    router.push('/auth');
    return null;
  }
};

// Функция для проверки, смотрим ли мы свое расписание
const checkScheduleOwnership = () => {
  
  const viewedLogin = route.params.login;
  
  if (viewedLogin && currentUser.value) {
    isViewingOwnSchedule.value = viewedLogin === currentUser.value.login;
    saveButtonVisible.value = !isViewingOwnSchedule.value;
  } else {
    isViewingOwnSchedule.value = true;
    saveButtonVisible.value = false;
  }
};

// Функция для сохранения чужого расписания
const saveOtherSchedule = async () => {
  try {
    const viewedLogin = route.params.login;
    
    if (!currentUser.value || !viewedLogin) return;
    
    const saveData = {
      my_login: currentUser.value.login,
      save_login: viewedLogin
    };
    
    const response = await axios.patch(`${API_BASE_URL}/save_schedule`, saveData);
    
    // Показываем уведомление об успехе
    alert(`Расписание успешно сохранено!`);
    
    // Перезагружаем свое расписание
    // await loadSchedule();
    router.push(`/schedule/${currentUser.value.login}`);
    
    } catch (err) {
      error.value = 'Ошибка сохранения расписания';
      console.error('Error saving schedule:', err);
    }
};

// Наблюдаем за изменениями маршрута
watch(() => router.currentRoute.value.params, () => {
  checkScheduleOwnership();
  if (currentUser.value) {
    loadSchedule();
  }
});

// Проверяем при монтировании и после загрузки пользователя
onMounted(async () => {
  await getCurrentUserInfo();
  if (currentUser.value) {
    checkScheduleOwnership();
    await loadSchedule();
  }
});

watch(currentUser, () => {
  if (currentUser.value) {
    checkScheduleOwnership();
  }
});

// Функция для получения полной информации о пользователе
const getCurrentUserInfo = async () => {
  try {
    const tokenUser = getCurrentUserFromToken();
    if (!tokenUser) return;

    // Используем защищенный роут для получения информации о пользователе
    const response = await axios.get(`${API_BASE_URL}/protected`);
    currentUser.value = {
      login: response.data.user.login,
      email: response.data.user.email,
      id: response.data.user.id
    };

  } catch (err) {
    console.error('Error getting user info:', err);
    if (err.response?.status === 401) {
      localStorage.removeItem('auth_token');
      router.push('/auth');
    }
  } finally {
    isLoadingUser.value = false;
  }
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

// Обработка отметки посещения
const handleAttendanceToggle = async (attendanceData) => {
  try {
    const { lesson, date, attended } = attendanceData;
    
    // Отправляем запрос на сервер для сохранения отметки посещения
    const attendancePayload = {
      lesson_id: lesson.lesson_id,
      date: formatDateYMD(date),
      attended: attended,
      user_login: currentUser.value.login
    };

    await axios.post(`${API_BASE_URL}/attendance`, attendancePayload);
    
    // Обновляем локальное состояние если нужно
    console.log(`Посещение отмечено: ${attended ? 'присутствовал' : 'отсутствовал'}`);
    
  } catch (err) {
    console.error('Error saving attendance:', err);
    // Можно показать уведомление об ошибке
  }
};

// Загрузка расписания
const loadSchedule = async () => {
  if (!currentUser.value) return;

  try {
    isLoading.value = true;
    error.value = null;
    const viewedLogin = route.params.login;

    const response = await axios.get(
      `${API_BASE_URL}/get_schedule/${viewedLogin}`
    );
    
    // Преобразуем объект в массив уроков
    if (response.data && typeof response.data === 'object' && !Array.isArray(response.data)) {
      // Если это объект с днями недели, преобразуем в массив
      scheduleData.value = Object.values(response.data).flat();
    } else {
      scheduleData.value = response.data;
    }
    
  } catch (err) {
    if (err.response?.status === 401) {
      // Неавторизован - перенаправляем на страницу входа
      localStorage.removeItem('auth_token');
      router.push('/auth');
    } else if (err.response?.status === 404) {
      // У пользователя нет расписания - это нормально
      scheduleData.value = [];
    } else {
      error.value = 'Ошибка загрузки расписания';
      console.error('Error loading schedule:', err);
    }
  } finally {
    isLoading.value = false;
  }
};

// Загрузка при монтировании
onMounted(async () => {
  await getCurrentUserInfo();
  if (currentUser.value) {
    await loadSchedule();
  }
});

watch(currentWeekStart, () => {
  if (currentUser.value) {
    loadSchedule();
  }
});

// Получение расписания для конкретной даты
const getScheduleForDate = (date) => {
  if (!scheduleData.value.length) return [];

  const dateStr = formatDateYMD(date);
  
  return scheduleData.value.filter(lesson => {
    // Проверяем, есть ли дата в массиве dates урока
    return lesson.dates && Array.isArray(lesson.dates) && lesson.dates.includes(dateStr);
  }).map(lesson => ({
    lesson_id: lesson.id,
    dates: lesson.dates,
    subject_name: lesson.subject_name,
    teacher_name: lesson.teacher_name,
    start_time: formatTime(new Date('1970-01-01T' + lesson.startTime)),
    end_time: formatTime(new Date('1970-01-01T' + lesson.endTime)),
    repeat: lesson.repeat,
    dayOfWeek: lesson.dayOfWeek,
    room: lesson.room || '', // Добавляем поле room
    description: lesson.description || '' // Добавляем поле description
  }));
};

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

// Открытие модального окна с деталями
const openModal = (item, date) => {
  selectedItem.value = item;
  selectedDate.value = date;
  isModalOpen.value = true;
};

// Закрытие модального окна
const closeModal = () => {
  isModalOpen.value = false;
  selectedItem.value = null;
  selectedDate.value = null;
};

// Открытие модального окна добавления
const openAddLessonModal = (date) => {
  addLessonDate.value = date;
  isAddModalOpen.value = true;
};

// Закрытие модального окна добавления
const closeAddModal = () => {
  isAddModalOpen.value = false;
  addLessonDate.value = null;
};

// Добавление нового урока
const addNewLesson = async (lessonData) => {
  try {
    const lessonPayload = {
      user_login: currentUser.value.login,
      teacher_name: lessonData.teacher_name,
      subject_name: lessonData.subject_name,
      startDate: formatDateYMD(addLessonDate.value),
      endDate: lessonData.end_date || formatDateYMD(addLessonDate.value),
      startTime: lessonData.start_time + ':00',
      endTime: lessonData.end_time + ':00',
      repeat: lessonData.repeat || false,
      dayOfWeek: getDayName(addLessonDate.value),
      room: lessonData.room || ''
    };

    await axios.post(`${API_BASE_URL}/add_lesson`, lessonPayload);
    await loadSchedule();
    closeAddModal();
    
  } catch (err) {
    error.value = 'Ошибка добавления урока';
    console.error('Error adding lesson:', err);
  }
};

// Обновление урока
const updateLesson = async (updatedLesson) => {
  try {
    const lessonPayload = {
      teacher_name: updatedLesson.teacher_name,
      subject_name: updatedLesson.subject_name,
      room: updatedLesson.room,
      startTime: updatedLesson.start_time + ':00',
      endTime: updatedLesson.end_time + ':00',
      repeat: updatedLesson.repeat || 'none',
      dayOfWeek: updatedLesson.dayOfWeek
    };

    // Убираем пустые поля
    Object.keys(lessonPayload).forEach(key => {
      if (lessonPayload[key] === undefined || lessonPayload[key] === null) {
        delete lessonPayload[key];
      }
    });

    await axios.put(
      `${API_BASE_URL}/edit_lesson/${selectedItem.value.lesson_id}`,
      lessonPayload
    );
    
    // Отправляем комментарий, если он не пустой
    if (updatedLesson.comment && updatedLesson.comment.trim() !== '') {
      try {
        const commentPayload = {
          lesson_id: selectedItem.value.lesson_id,
          date: formatDateYMD(selectedDate.value),
          comment: updatedLesson.comment.trim()
        };
        
        await axios.put(`${API_BASE_URL}/edit_comment`, commentPayload);
      } catch (commentErr) {
        console.warn('Comment update failed:', commentErr);
        // Продолжаем даже если комментарий не сохранился
      }
    }
    
    await loadSchedule();
    closeModal();
    
  } catch (err) {
    error.value = 'Ошибка обновления урока';
    console.error('Error updating lesson:', err);
  }
};

// Удаление урока
const deleteLesson = async () => {
  try {
    await axios.delete(
      `${API_BASE_URL}/delete_lesson/${selectedItem.value.lesson_id}`
    );
    await loadSchedule();
    closeModal();
    
  } catch (err) {
    error.value = 'Ошибка удаления урока';
    console.error('Error deleting lesson:', err);
  }
};
</script>

<template>
  <div class="schedule-app">
    <!-- Добавляем навигационную панель -->
    <Navigation 
      :user="currentUser" 
      @logout="handleLogout" 
    />
    
    <div class="schedule-content">
      <h1 class="title">Расписание занятий</h1>
      
      <!-- Индикатор загрузки -->
      <div v-if="isLoadingUser" class="loading">Загрузка информации о пользователе...</div>
      <div v-else-if="isLoading" class="loading">Загрузка расписания...</div>
      
      <!-- Сообщение об ошибке -->
      <div v-if="error" class="error">{{ error }}</div>
      
      <div v-if="currentUser && !isLoading">
        <WeekNavigation
          :current-date="currentDate"
          :week-days="weekDays"
          :schedule="scheduleData"
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
          :comments="[]"
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
      
      <button 
        v-if="saveButtonVisible" 
        class="save-schedule-button"
        @click="saveOtherSchedule"
      >
        Сохранить расписание
      </button>
    </div>
  </div>
</template>

<style scoped>
.schedule-app {
  min-height: 100vh;
  font-family: "Chiron GoRound TC", sans-serif;
}

.schedule-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 100px 20px 30px; /* Увеличиваем верхний отступ для панели */
  box-sizing: border-box;
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

.loading {
  text-align: center;
  padding: 20px;
  color: #4a2d7c;
  font-size: 18px;
}

.error {
  text-align: center;
  padding: 20px;
  color: #ff0000;
  background-color: #ffe6e6;
  border-radius: 5px;
  margin-bottom: 20px;
}

.save-schedule-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 45px 75px;
  background-color: #4a2d7c;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-family: "Chiron GoRound TC", sans-serif;
  font-weight: 600;
  font-size: 100%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  z-index: 1000;
}

.save-schedule-button:hover {
  background-color: #3a225f;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .schedule-content {
    padding: 90px 15px 20px; /* Адаптивный отступ */
  }
  
  .schedule-container {
    flex-direction: column;
    gap: 20px;
  }
  
  .title {
    font-size: 28px;
    margin-bottom: 25px;
  }
  
  .save-schedule-button {
    bottom: 20px;
    right: 20px;
    padding: 12px 20px;
    font-size: 14px;
  }
}
</style>