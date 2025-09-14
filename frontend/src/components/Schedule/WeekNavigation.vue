<template>
  <div class="week-navigation">
    <button @click="$emit('prev-week')" class="nav-button">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
      </svg>
      Предыдущая неделя
    </button>
    
    <div class="week-days">
      <button 
        v-for="day in weekDays" 
        :key="day.date.toString()"
        @click="$emit('day-select', day.date)"
        :class="{ 
          'active': isSameDay(day.date, currentDate),
          'has-events': hasEvents(day.date)
        }"
        class="day-button"
      >
        <div class="weekday">{{ formatWeekday(day.date) }}</div>
        <div class="day-number">{{ day.date.getDate() }}</div>
        <div v-if="hasEvents(day.date)" class="events-dot"></div>
      </button>
    </div>
    
    <button @click="$emit('next-week')" class="nav-button">
      Следующая неделя
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { formatWeekday, isSameDay, formatDateYMD } from '../../utils/dateUtils';

const props = defineProps({
  currentDate: Date,
  weekDays: Array,
  schedule: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['prev-week', 'next-week', 'day-select']);

// Функция проверки наличия событий для даты
const hasEvents = (date) => {
  try {
    if (!props.schedule || !Array.isArray(props.schedule)) {
      return false;
    }
    
    const dateStr = formatDateYMD(date);
    
    // Проверяем, есть ли уроки на эту дату
    return props.schedule.some(lesson => {
      if (!lesson || !lesson.dates || !Array.isArray(lesson.dates)) {
        return false;
      }
      return lesson.dates.includes(dateStr);
    });
    
  } catch (error) {
    console.error('Error in hasEvents:', error);
    return false;
  }
};
</script>

<style scoped>
/* Стили остаются без изменений */
@import url('https://fonts.googleapis.com/css2?family=Chiron+GoRound+TC:wght@200..900&family=Playpen+Sans:wght@100..800&family=Stick&display=swap');

.week-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background-color: #D3C5E5;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  font-family: "Chiron GoRound TC", sans-serif;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 12px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-family: "Chiron GoRound TC", sans-serif;
  color: #4a2d7c;
  font-weight: 600;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.nav-button:hover {
  background-color: rgba(74, 45, 124, 0.1);
  border-color: #4a2d7c;
}

.week-days {
  display: flex;
  gap: 8px;
}

.day-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 55px;
  height: 65px;
  border: none;
  background: white;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.3s;
  position: relative;
  font-family: "Chiron GoRound TC", sans-serif;
  border: 2px solid #ddd;
}

.day-button:hover {
  background: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.day-button.active {
  background: #4a2d7c;
  color: white;
  border-color: #4a2d7c;
}

.day-button.has-events {
  border-color: #4a2d7c;
}

.day-button .weekday {
  font-size: 12px;
  text-transform: capitalize;
  font-weight: 600;
}

.day-button .day-number {
  font-size: 18px;
  font-weight: bold;
}

.events-dot {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 8px;
  height: 8px;
  background: #ff4757;
  border-radius: 50%;
}

@media (max-width: 768px) {
  .week-navigation {
    flex-direction: column;
    gap: 15px;
    padding: 15px;
  }
  
  .week-days {
    order: -1;
    width: 100%;
    justify-content: space-between;
  }
  
  .day-button {
    width: 45px;
    height: 55px;
  }
  
  .nav-button {
    width: 100%;
    justify-content: center;
  }
}
</style>