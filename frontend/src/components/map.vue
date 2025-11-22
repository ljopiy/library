<template>
  <div class="interactive-map-container">
    <div class="map-wrapper">
      <!-- Основное изображение карты -->
      <img
        ref="mapImage"
        src="/assets/map.jpg"
        alt="План помещения"
        usemap="#roomMap"
        class="map-image"
        @load="onImageLoad"
      />

      <!-- HTML Image Map -->
      <map name="roomMap">
        <area
          v-for="area in areas"
          :key="area.id"
          :shape="area.shape"
          :coords="area.coords"
          :alt="area.title"
          @mouseover="handleAreaHover(area.id)"
          @mouseout="handleAreaOut"
          @click="handleAreaClick(area.id)"
          :class="{ 'area-highlighted': hoveredArea === area.id }"
        />
      </map>

      <!-- Всплывающая подсказка -->
      <div
        v-if="tooltip.visible && hoveredArea"
        class="tooltip"
        :style="{
          left: tooltip.x + 'px',
          top: tooltip.y + 'px'
        }"
      >
        {{ getAreaTitle(hoveredArea) }}
      </div>
    </div>

    <!-- Панель информации о выбранной зоне -->
    <div v-if="selectedArea" class="info-panel">
      <h3>Информация о помещении</h3>
      <div class="info-content">
        <h4>{{ selectedArea.title }}</h4>
        <p v-if="selectedArea.description">{{ selectedArea.description }}</p>
        <p v-if="selectedArea.area"><strong>Площадь:</strong> {{ selectedArea.area }} м²</p>
        <p v-if="selectedArea.capacity"><strong>Вместимость:</strong> {{ selectedArea.capacity }} чел.</p>
        <p v-if="selectedArea.equipment"><strong>Оборудование:</strong> {{ selectedArea.equipment }}</p>
      </div>
      <button @click="selectedArea = null" class="close-btn">Закрыть</button>
    </div>

    <!-- Дебаг информация (можно удалить в продакшене) -->
    <div v-if="debugMode" class="debug-info">
      <h4>Отладка:</h4>
      <p>Наведено на: {{ hoveredArea || 'нет' }}</p>
      <p>Выбрано: {{ selectedArea?.title || 'нет' }}</p>
      <p>Координаты курсора: X: {{ mousePosition.x }}, Y: {{ mousePosition.y }}</p>
      <button @click="toggleDebug" class="debug-btn">Скрыть отладку</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';

// Состояния
const hoveredArea = ref(null);
const selectedArea = ref(null);
const debugMode = ref(true); // Поставьте false чтобы скрыть отладку

// Данные для тултипа
const tooltip = reactive({
  visible: false,
  x: 0,
  y: 0
});

// Позиция курсора
const mousePosition = reactive({
  x: 0,
  y: 0
});


{/* <map name="image-map">
    <area target="" alt="10" title="10" href="" coords="406,434,678,426,677,318,596,313,596,229,402,232,403,290" shape="poly">
    <area target="" alt="5" title="5" href="" coords="159,232,156,99,305,94,310,233,160,233" shape="poly">
    <area target="" alt="7" title="7" href="" coords="159,294,158,242,219,241,220,294,192,295" shape="poly">
    <area target="" alt="9" title="9" href="" coords="323,227,319,97,594,98,595,225,322,231" shape="poly">
    <area target="" alt="14" title="14" href="" coords="322,235,397,234,403,431,324,434" shape="poly">
    <area target="" alt="11" title="11" href="" coords="682,259,611,299" shape="rect">
    <area target="" alt="12" title="12" href="" coords="694,258,924,433" shape="rect">
    <area target="" alt="13" title="13" href="" coords="692,139,924,247" shape="rect">
    <area target="" alt="13.2" title="13.2" href="" coords="693,50,784,133" shape="rect">
    <area target="" alt="13.1" title="13.1" href="" coords="792,52,921,132" shape="rect">
</map> --> */}

// Данные о зонах помещения
const areas = ref([
  {
    id: 'event hall',
    shape: 'poly',
    coords: '406,434,678,426,677,318,596,313,596,229,402,232,403,290',
    title: 'Событийный зал',
    description: 'Многофункциональный зал оборудованный мультимедийной техникой',
    area: 25,
    capacity: 2,
    equipment: 'Компьютер, телефон, принтер'
  },
  {
    id: 'Chiled',
    shape: 'poly',
    coords: '159,232,156,99,305,94,310,233,160,233',
    title: 'Абонемент для детей',
    description: 'Игровая комната',
    area: 20,
    capacity: 6,
    equipment: 'Телевизор, маркерная доска'
  },
  {
    id: 'Wardrobe',
    shape: 'poly',
    coords: '159,294,158,242,219,241,220,294,192,295',
    title: 'Гардеробная',
    description: 'Место для хранения вашей верхней одежды',
    area: 30,
    capacity: 12,
    equipment: 'Проектор, конференц-система'
  },
  {
    id: 'sub',
    shape: 'poly',
    coords: '323,227,319,97,594,98,595,225,322,231',
    title: 'Абонемент',
    description: 'Загадочное пространство, приходи и узнай сам!',
    area: 18,
    capacity: 8,
    equipment: 'Микроволновка, холодильник, кофемашина'
  },
  {
    id: 'Reading hall',
    shape: 'poly',
    coords: '322,235,397,234,403,431,324,434',
    title: 'Читальный зал',
    description: 'Пространство для чтения, стилизованное под вагон поезда',
    area: 4,
    capacity: 1,
    equipment: 'Компьютер, монитор'
  },
  {
    id: 'Books room',
    shape: 'rect',
    coords: '682,259,611,299',
    title: 'Хранилище книг',
    description: 'Спальная комната книг, просьба беспокоить как можно чаще!',
    area: 4,
    capacity: 1,
    equipment: 'Компьютер, монитор'
  },
    {
    id: 'Youth room',
    shape: 'rect',
    coords: '694,258,924,433',
    title: 'Молодёжный зал',
    description: 'Многофункциональный зал с амфитеатром',
    area: 4,
    capacity: 1,
    equipment: 'Компьютер, монитор'
  },
  {
    id: 'Arts room',
    shape: 'rect',
    coords: '692,139,924,247',
    title: 'Зал искусств',
    description: 'Арт-галерея, многофункциональное пространство',
    area: 4,
    capacity: 1,
    equipment: 'Компьютер, монитор'
  },
  {
    id: 'Media',
    shape: 'rect',
    coords: '693,50,784,133',
    title: 'Медиа среда',
    description: 'Здесь создаются инфо поводы!',
    area: 4,
    capacity: 1,
    equipment: 'Компьютер, монитор'
  },
  {
    id: 'Project office',
    shape: 'rect',
    coords: '792,52,921,132',
    title: 'Проектный офис',
    description: 'Место где идея становиться реальностью!',
    area: 4,
    capacity: 1,
    equipment: 'Компьютер, монитор'
  }
]);

// Получение заголовка зоны
const getAreaTitle = (areaId) => {
  const area = areas.value.find(a => a.id === areaId);
  return area ? area.title : '';
};

// Обработчики событий
const handleAreaHover = (areaId) => {
  hoveredArea.value = areaId;
  tooltip.visible = true;
};

const handleAreaOut = () => {
  tooltip.visible = false;
  hoveredArea.value = null;
};

const handleAreaClick = (areaId) => {
  const area = areas.value.find(a => a.id === areaId);
  if (area) {
    selectedArea.value = area;
  }
};

// Отслеживание движения курсора для тултипа
const handleMouseMove = (event) => {
  mousePosition.x = event.clientX;
  mousePosition.y = event.clientY;

  if (tooltip.visible) {
    tooltip.x = event.clientX + 10;
    tooltip.y = event.clientY - 10;
  }
};

// Когда изображение загружено
const onImageLoad = () => {
  console.log('Изображение карты загружено');
};

// Переключение режима отладки
const toggleDebug = () => {
  debugMode.value = !debugMode.value;
};

// Инициализация
onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove);
});
</script>

<style scoped>
.interactive-map-container {
  display: flex;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.map-wrapper {
  position: relative;
  flex: 3;
}

.map-image {
  width: 100%;
  height: auto;
  border: 2px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Стили для тултипа */
.tooltip {
  position: fixed;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  pointer-events: none;
  z-index: 1000;
  white-space: nowrap;
}

/* Панель информации */
.info-panel {
  flex: 1;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  border: 1px solid #ddd;
  min-width: 250px;
}

.info-content h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.info-content p {
  margin: 5px 0;
  font-size: 14px;
  color: #666;
}

.close-btn {
  margin-top: 15px;
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.close-btn:hover {
  background: #0056b3;
}

/* Отладочная информация */
.debug-info {
  position: fixed;
  bottom: 20px;
  left: 20px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 15px;
  border-radius: 4px;
  font-size: 12px;
  z-index: 1000;
}

.debug-btn {
  margin-top: 10px;
  padding: 5px 10px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 10px;
}

/* Стили для областей (работают ограниченно) */
area {
  cursor: pointer;
  outline: none;
}

/* Медиа-запросы для мобильных устройств */
@media (max-width: 768px) {
  .interactive-map-container {
    flex-direction: column;
  }

  .info-panel {
    min-width: auto;
  }

  .debug-info {
    position: relative;
    bottom: auto;
    left: auto;
    margin-top: 20px;
  }
}
</style>
