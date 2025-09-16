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
const commentsData = ref([]);

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
      return null; // Возвращаем null вместо выброса ошибки
    }

    // Добавляем токен в заголовки axios по умолчанию
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    // Парсим payload из JWT токена
    const payload = JSON.parse(atob(token.split('.')[1]));
    
    return {
      email: payload.sub,
      login: payload.sub.split('@')[0] 
    };

  } catch (err) {
    console.error('Error parsing token:', err);
    localStorage.removeItem('auth_token');
    return null;
  }
};

// Функция для проверки, смотрим ли мы свое расписание
const checkScheduleOwnership = () => {
  const viewedLogin = route.params.login;
  const currentUserLogin = currentUser.value?.login;
  
  if (viewedLogin && currentUserLogin) {
    isViewingOwnSchedule.value = viewedLogin === currentUserLogin;
    saveButtonVisible.value = !isViewingOwnSchedule.value && checkAuth();
  } else {
    isViewingOwnSchedule.value = false;
    saveButtonVisible.value = checkAuth() && viewedLogin !== currentUserLogin;
  }
};

const checkAuth = () => {
  return !!localStorage.getItem('auth_token');
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
  checkScheduleOwnership();
  await loadSchedule();
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
    if (!tokenUser) {
      currentUser.value = null;
      return;
    }

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
      currentUser.value = null;
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
    
    // Обновляем локальное состояние
    const dateStr = formatDateYMD(date);
    if (attended) {
      if (!lesson.attendances) lesson.attendances = [];
      if (!lesson.attendances.includes(dateStr)) {
        lesson.attendances.push(dateStr);
      }
    } else {
      if (lesson.attendances) {
        lesson.attendances = lesson.attendances.filter(d => d !== dateStr);
      }
    }
    
  } catch (err) {
    console.error('Error handling attendance toggle:', err);
  }
};

// Загрузка расписания
const loadSchedule = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    const viewedLogin = route.params.login;

    // Убираем авторизационный заголовок для GET запросов если нет токена
    const config = {};
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers = { Authorization: `Bearer ${token}` };
    }

    const response = await axios.get(
      `${API_BASE_URL}/get_schedule/${viewedLogin}`,
      config
    );
    if (response.data && response.data.comments) {
      commentsData.value = response.data.comments;
      delete response.data.comments;
    }

    if (response.data && typeof response.data === 'object' && !Array.isArray(response.data)) {
      scheduleData.value = Object.values(response.data).flat();
    } else {
      scheduleData.value = response.data;
    }
    
  } catch (err) {
    if (err.response?.status === 404) {
      scheduleData.value = [];
    } else {
      error.value = 'Ошибка загрузки расписания';
      console.error('Error loading schedule:', err);
    }
  } finally {
    isLoading.value = false;
  }
};


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
    return lesson.dates && Array.isArray(lesson.dates) && lesson.dates.includes(dateStr);
  }).map(lesson => {
    const comment = commentsData.value.find(c => 
      c.lesson_id === lesson.id && c.lesson_date === dateStr
    );
    
    return {
      id: lesson.id,
      dates: lesson.dates,
      attendances: lesson.attendances || [],
      subject_name: lesson.subject_name,
      teacher_name: lesson.teacher_name,
      start_time: formatTime(new Date('1970-01-01T' + lesson.startTime)),
      end_time: formatTime(new Date('1970-01-01T' + lesson.endTime)),
      start_date: lesson.startDate,
      end_date: lesson.endDate,
      repeat: lesson.repeat,
      dayOfWeek: lesson.dayOfWeek,
      room: lesson.room || '',
      description: comment ? comment.text : '' // Добавляем комментарий
    };
  });
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
  if (!checkAuth()) {
    alert('Для редактирования расписания необходимо войти в систему');
    router.push('/authorization');
    return;
  }
  
  if (!isViewingOwnSchedule.value) {
    alert('Вы можете редактировать только свое расписание');
    return;
  }
  
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
  if (!checkAuth()) {
    alert('Для добавления занятий необходимо войти в систему');
    router.push('/authorization');
    return;
  }
  
  if (!isViewingOwnSchedule.value) {
    alert('Вы можете добавлять занятия только в свое расписание');
    return;
  }
  
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
      repeat: lessonData.repeat || 'none',
      dayOfWeek: getDayName(addLessonDate.value),
      room: lessonData.room || ''
    };

    console.log('Sending lesson data:', lessonPayload); // Для отладки

    await axios.post(`${API_BASE_URL}/add_lesson`, lessonPayload);
    await loadSchedule();
    closeAddModal();
    
  } catch (err) {
    error.value = 'Ошибка добавления урока';
    console.error('Error adding lesson:', err);
    console.error('Response data:', err.response?.data); // Для отладки
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
      startDate: updatedLesson.start_date, // Добавьте это
      endDate: updatedLesson.end_date,     // И это
      repeat: updatedLesson.repeat || 'none',
      dayOfWeek: updatedLesson.dayOfWeek
    };

    Object.keys(lessonPayload).forEach(key => {
      if (lessonPayload[key] === undefined || lessonPayload[key] === null) {
        delete lessonPayload[key];
      }
    });

    await axios.put(
      `${API_BASE_URL}/edit_lesson/${selectedItem.value.id}`,
      lessonPayload
    );
    
    // Отправляем комментарий, если он не пустой

    
      try {
        const commentPayload = {
          lesson_id: selectedItem.value.id, // было lesson_id
          lesson_date: formatDateYMD(selectedDate.value),
          text: updatedLesson.description.trim()
        };
        
        await axios.put(`${API_BASE_URL}/edit_comment`, commentPayload);
      } catch (commentErr) {
        console.warn('Comment updаte failed:', commentErr);
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
    <Navigation 
      :user="currentUser" 
      @logout="handleLogout" 
    />
    
    <div class="schedule-content">
      <h1 class="title">Расписание занятий {{ route.params.login }}</h1>
      
      <!-- Индикатор загрузки -->
      <div v-if="isLoadingUser" class="loading">Загрузка информации о пользователе...</div>
      <div v-else-if="isLoading" class="loading">Загрузка расписания...</div>
      
      <!-- Сообщение об ошибке -->
      <div v-if="error" class="error">{{ error }}</div>
      
      <div v-if="!isLoading">
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
            :show-attendance-button="false"
            @day-click="changeDay(-1)"
            @item-click="openModal($event, prevDate)"
          />

          <ScheduleDay
            :title="formatDate(currentDate)"
            :items="getScheduleForDate(currentDate)"
            day-type="current-day"
            :show-add-button="isViewingOwnSchedule"
            :show-attendance-button="isViewingOwnSchedule"
            @item-click="openModal($event, currentDate)"
            @add-click="openAddLessonModal(currentDate)"
          />

          <ScheduleDay
            :title="formatDate(nextDate)"
            :items="getScheduleForDate(nextDate)"
            day-type="next-day"
            :clickable="true"
            :show-add-button="false"
            :show-attendance-button="false"
            @day-click="changeDay(1)"
            @item-click="openModal($event, nextDate)"
          />
        </div>

        <!-- Модальные окна показываем только владельцу -->
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
      </div> <!-- Закрывающий тег для v-if="!isLoading" -->
      
      <button 
        v-if="saveButtonVisible" 
        class="save-schedule-button"
        @click="saveOtherSchedule"
      >
        Сохранить это расписание
      </button>
    </div> <!-- Закрывающий тег для .schedule-content -->
  </div> <!-- Закрывающий тег для .schedule-app -->
</template>

<style scoped>
.schedule-app {
  min-height: 100vh;
  font-family: "Chiron GoRound TC", sans-serif;
}

.schedule-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 100px 20px 30px;
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
    padding: 90px 15px 20px;
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