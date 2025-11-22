<template>
  <div class="page-wrapper">
    <div class="header">
      <iconBtn><img src='../../public/assets/icon/icon-arrow-black.svg'></img></iconBtn>
    </div>
    <div class="book">
      <div class="book-photo">
        <img class="photo-main" src="../../public/assets/book1.svg" alt="Фото книги"></img>
        <div class="phots">
          <button><img class="photo-mini photo-mini_active" src="../../public/assets/book1.svg" alt="Фото книги"></img></button>
          <button><img class="photo-mini photo-mini_active" src="../../public/assets/book1.svg" alt="Фото книги"></img></button>
          <button><img class="photo-mini photo-mini_active" src="../../public/assets/book1.svg" alt="Фото книги"></img></button>
          <button><img class="photo-mini photo-mini_active" src="../../public/assets/book1.svg" alt="Фото книги"></img></button>
        </div>
      </div>
      <div class="book-description">
        <h2>Отношения. Как лев чуть не убил меня, что я пропуск забыла</h2>
        <p>Умение создавать и поддерживать отношения, без преувеличения, самый важный навык. Из отношений соткана вся жизнь. Близость с людьми является источником как истинного счастья и радости, так и самых глубоких ран и разочарований. Настоящие отношения — основа удовлетворения жизнью и долголетия (научно доказано Гарвардским исследованием).</p>

        <p>Что же мы делаем, чтобы научиться строить отношения? Как учим этому своих детей? В школьной программе такого предмета нет. Нам приходиться учиться и учить на собственных ошибках, перенимая не самый успешный опыт близкого окружения. Пора это исправить!
        </p>
        <button>Читать полностью</button>
        <p class="unactive">Типа продолжение</p>
      </div>
      <div class="book-info">
        <div>
          <p>Издательство</p>
          <p>Smart Reading</p>
        </div>
        <div>
          <p>ISBN:</p>
          <p>9785604800904</p>
        </div>
        <div>
          <p>Серия:</p>
          <p>Чему не учат в школе</p>
        </div>
        <div>
          <p>Жанр:</p>
          <p>Роман</p>
        </div>
        <div>
          <p>Год издания:</p>
          <p>2023</p>
        </div>
      </div>
      <div class="reviews">
        <h3>Отзывы</h3>
        <ul>
          <reviewCard></reviewCard>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import iconBtn from '@/components/ui/icon-btn.vue';
import reviewCard from '@/components/shared/reviewCard.vue';
</script>

<style>
.header {
  padding: 10px 19px;
}

.header button {
  padding: 0;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

}

.reviews{
  display: flex;
  flex-direction: column;
}

.photo-main {
  width: 140px;
  height: 200px;
  display: flex;
  align-items: center;
}

.book-photo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.book-description {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.book-info {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

p {
  margin: 0;
  padding: 0;
}

.book-info div {
  display: flex;
  justify-content: space-between;
}
.book-description button {
  background-color: transparent;
  border: none;
  display: flex;
  color: orangered;
  padding: 0;
  width: 40%;
}

.unactive {
  display: none;
}

.book-description p {
  padding: 0;
  margin: 0;
}

.phots {
  display: flex;
  gap: 10px;
}

.photo-mini  {
  opacity: 0.5;
}

.phots button {
  background-color: transparent;
  border: 1px solid transparent;

}

.phots button:active {
  border: 1px solid #F35935;
  border-radius: 5px;
}

.book {
  display: flex;
  flex-direction: column;
  gap: 12px;
}


</style>
