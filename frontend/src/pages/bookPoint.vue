<template>
  <div class="page-wrapper">
    <div class="header"><h1>BookPoint</h1></div>
    <div class="reki">
      <h4>Рекомендуем к прочтению</h4>
      <ul>
        <bookCard></bookCard>
        <bookCard></bookCard>
      </ul>
    </div>
    <div class="coworking">
      <h2>Наш коворкинг</h2>
      <ul>
        <li>
          <img src="../../public/assets/coworking.svg"></img>
        </li>
        <li>
          <img src="../../public/assets/coworking2.svg"></img>
        </li>
        <li>
          <img src="../../public/assets/coworking3.svg"></img>
        </li>
        <li>
          <img src="../../public/assets/coworking4.svg"></img>
        </li>
      </ul>
      <NButton type="primary">Забронировать</NButton>
    </div>
  </div>
</template>

<script setup>
import { NButton } from 'naive-ui';
import bookCard from '@/components/shared/bookCard.vue';
</script>

<style scoped>
ul {
  display: flex;
  overflow-x: scroll;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
    -ms-overflow-style: none;
}

li {
  list-style-type: none;
  scroll-snap-align: center;
  flex: 0 0 10px;
}

li img {
  width: 100vw;
}

</style>
