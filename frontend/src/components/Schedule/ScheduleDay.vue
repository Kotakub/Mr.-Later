<template>
  <div 
    class="schedule-day"
    :class="[dayType, { 'clickable': clickable }]"
    @click="clickable && $emit('day-click')"
  >
    <h3>{{ title }}</h3>
    <div class="schedule-items">
      <ScheduleItem
        v-for="(item, index) in items"
        :key="`${item.subject_name}-${item.teacher_name}-${index}`"
        :item="item"
        :has-comments="hasCommentsForItem(item)"
        :show-attendance-button="showAttendanceButton"
        :current-date="currentDate"
        @item-click="$emit('item-click', item)"
        @attendance-toggle="$emit('attendance-toggle', $event)"
      />
      
      <AddLessonButton 
        v-if="showAddButton"
        @add-click="$emit('add-click')"
      />
      <div v-if="!items.length && !showAddButton" class="no-events">
        Нет занятий
      </div>
    </div>
  </div>
</template>

<script setup>
import ScheduleItem from './ScheduleItem.vue';
import AddLessonButton from './AddLessonButton.vue';

const props = defineProps({
  title: String,
  items: {
    type: Array,
    default: () => []
  },
  dayType: {
    type: String,
    default: 'current-day',
    validator: (value) => ['current-day', 'prev-day', 'next-day'].includes(value)
  },
  clickable: {
    type: Boolean,
    default: false
  },
  showAddButton: {
    type: Boolean,
    default: false
  },
  showAttendanceButton: {
    type: Boolean,
    default: true
  },
  currentDate: {
    type: Date,
    default: () => new Date()
  }
});

defineEmits(['day-click', 'item-click', 'add-click', 'attendance-toggle']);

// Заглушка для проверки комментариев
const hasCommentsForItem = (item) => {
  return false;
};
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Chiron+GoRound+TC:wght@200..900&family=Playpen+Sans:wght@100..800&family=Stick&display=swap');

.schedule-day {
  background-color: #D3C5E5;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 25px;
  font-family: "Chiron GoRound TC", sans-serif;
}

.schedule-day.clickable {
  cursor: pointer;
  transition: all 0.3s ease;
}

.schedule-day.clickable:hover {
  opacity: 1;
  transform: scale(1.02);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.current-day {
  flex: 1;
  max-width: 50%;
  background-color: #E6DDF0;
}

.prev-day, .next-day {
  flex: 0.5;
  opacity: 0.9;
}

h3 {
  margin-top: 0;
  color: #4a2d7c;
  text-align: center;
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: 700;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.schedule-items {
  margin-top: 15px;
  position: relative;
}

.no-events {
  text-align: center;
  color: #7a6f8c;
  padding: 40px 0;
  font-style: italic;
  font-size: 16px;
}

@media (max-width: 768px) {
  .schedule-day {
    padding: 20px;
  }
  
  .current-day, .prev-day, .next-day {
    max-width: 100%;
    width: 100%;
    margin-bottom: 20px;
  }
  
  h3 {
    font-size: 18px;
    margin-bottom: 15px;
  }
}
</style>