<template>
  <div class="page-wrapper">
    <div class="header">
      <img src="../../public/assets/icon/icon-user-orange.svg"></img>
      <h1>Алина Хусяинова</h1>
    </div>
    <div class="likes">
      <button>Избранное</button>
      <ul>
        <bookCard></bookCard>
        <bookCard></bookCard>
      </ul>
    </div>
    <div class="rezerv">
      <NButton><p>Забронированные книги</p></NButton>
    </div>
    <div class="reviews">
      <NButton><p>Отзывы</p></NButton>
    </div>
    <div class="alerts">
      <h2>Уведомления</h2>
      <Alert></Alert>
      <Alert></Alert>
      <Alert></Alert>
    </div>
  </div>
</template>

<script setup>
import bookCard from '@/components/shared/bookCard.vue';
import { NButton } from 'naive-ui';
import Alert from '@/components/shared/alert.vue';
</script>

<style scoped>
.rezerv button {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  box-shadow: 2px 2px 4px 0px rgba(34, 60, 80, 0.2);
  background-color: #F3F3F3;
}
.reviews button {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  background-color: #F3F3F3;
}
.reviews button p {
  color: black;
}
.page-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.likes {
  background-color: #F3F3F3;
  display: flex;
  flex-direction: column;
  gap: 7px;
  padding: 10px 5px;
  box-shadow: 2px 2px 4px 0px rgba(34, 60, 80, 0.2);

}
.likes ul {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 2px;
}
.likes button {
  width: 30%;
  border: none;
  padding-left: 13px;
}
.header {
  display: flex;
  padding: 0;
  margin: 0;
  gap: 10px;

}
.alerts {
  background-color: #F3F3F3;
  padding: 9px 26px;
  display: flex;
  gap: 10px;
  flex-direction: column;
  border-radius: 5px;
  box-shadow: 2px 2px 4px 0px rgba(34, 60, 80, 0.2);

}
</style>
