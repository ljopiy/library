<template>
  <div class="card-wrapper">
    <div class="favorite">
      <img src="/public/assets/icon/heart.svg" alt="">
    </div>
    <div class="img">
      <img src="/public/assets/book1.png" alt="">
    </div>
    <div class="title">
      <h3>Дед мороз картавый нос</h3>
    </div>
    <div class="description">
      <p>Подарок на Новый год под ёлку от Маши Рупасовой / 3 книги</p>
    </div>
    <div class="rating">
      <div class="star">
        <img src="/public/assets/icon/feather.svg" alt="">
        <span>4,5</span>
      </div>
      <div class="comments">
        <img src="/public/assets/icon/comment-vector.svg" alt="">
        <span>1232</span>
      </div>
    </div>
    <NButton type="primary" style="width: 90%; height: 30px;">Забронировать</NButton>
  </div>
</template>

<script setup>
import { NButton } from 'naive-ui';
</script>

<style scoped>
.card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 170px;
  gap: 4px;
  padding: 10px 5px;
  background-color: #F3F3F3;
  border-radius: 14px;
  position: relative;
}

.img {
  margin-top: 20px;
}

.img > img {
  width: 90px;
}

.description > p {
  font-size: 10px;
}

span {
  font-size: 10px;
  color: #999;
}

.rating{
  display: flex;
  justify-content: flex-start;
  width: 90%;
  gap: 10px;
}

.star, .comments {
  display: flex;
  gap: 3px;
  align-items: center;
}

.favorite {
  position: absolute;
  right: 10px;
  top: 6px;
}


</style>
