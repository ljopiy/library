<template>
  <div class="footer-wrapper">
    <div class="action-btn">
      <ul>
        <li>
          <IconBtn class="nav-btn">
              <img src="/assets/icon/search.svg" alt="">
          </IconBtn>
        </li>
        <li>
          <IconBtn class="nav-btn">
            <img src="/assets/icon/line.svg" alt="">
          </IconBtn>
        </li>
        <li>
          <IconBtn class="nav-btn">
            <img src="/assets/icon/main.svg" alt="">
          </IconBtn>
        </li>
        <li>
          <IconBtn class="nav-btn">
            <img src="/assets/icon/MapPin.svg" alt="">
          </IconBtn>
        </li>
        <li>
          <IconBtn class="nav-btn">
            <img src="/assets/icon/User.svg" alt="">
          </IconBtn>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import IconBtn from '../ui/icon-btn.vue';
</script>

<style scoped>
.footer-wrapper {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0; /* Растягиваем на всю ширину */
  width: 100%; /* Или можно использовать 100% */
}

.action-btn {
  background-color: white;
  display: flex;
  align-items: center;
  width: 100%; /* Используем 100% вместо 100vw */
  height: 90px;
  /* Убираем margin-left: -5px */
}

ul {
  display: flex;
  justify-content: space-around; /* Равномерное распределение */
  list-style-type: none;
  padding: 0;
  margin: 0;
  width: 100%; /* Растягиваем список на всю ширину */
}

/* Каждый элемент списка занимает равную ширину */
ul li {
  flex: 1;
  display: flex;
  justify-content: center;
}

.nav-btn {
  padding: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nav-btn:active {
  background-color: #f07f56a5;
}

/* Стили для текста под иконкой */
.nav-btn span {
  font-size: 12px;
  margin-top: 4px;
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn-content {
  color: #999;
  font-size: 10px;
}

.search-btn {
  border: 1px solid #F7742A;
  border-radius: 20px;
  padding: 8px 14px;
}

.search-btn:active {
  background-color: #f07f56a5;
}

li * img {
  width: 20px;
  height: 20px;
}
</style>
