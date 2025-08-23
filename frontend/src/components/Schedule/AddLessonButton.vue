<template>
  <div class="add-lesson-button" @click="$emit('add-click')">
    <div class="plus-icon">+</div>
    <span>Добавить занятие</span>
  </div>
</template>

<script setup>
defineEmits(['add-click']);
</script>

<style scoped>
.add-lesson-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 18px;
  border: 2px dashed #9f8cb9;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 15px;
  font-family: "Stick", sans-serif;
  color: #4a2d7c;
  font-weight: 600;
}

.add-lesson-button:hover {
  border-color: #4a2d7c;
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.plus-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #4a2d7c;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.add-lesson-button:hover .plus-icon {
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .add-lesson-button {
    flex-direction: column;
    text-align: center;
    gap: 8px;
    padding: 15px;
  }
}
</style>