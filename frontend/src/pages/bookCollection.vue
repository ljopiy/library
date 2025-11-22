<template>
  <div class="header">
    <h2>Коллекция книг</h2>
    <IconBtn class="btn">
      <img src="/public/assets/icon/filter.svg" alt="">
    </IconBtn>
  </div>
  <div class="book-feed">
    <BookCard/>
    <BookCard/>
    <BookCard/>
    <BookCard/>
    <BookCard/>
    <BookCard/>
    <BookCard/>
    <BookCard/>
    <BookCard/>
    <BookCard/>
    <BookCard/>

  </div>
  <Footer></Footer>
</template>

<script setup>
import IconBtn from '@/components/ui/icon-btn.vue';
import BookCard from '@/components/shared/bookCard.vue';
import Footer from '@/components/shared/footer.vue';


</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: center;
}

h2{
  flex: 1;
  text-align: center;
  margin-right: -35px;
}

.btn > img {
  width: 15px;
  height: 15px;
}

.book-feed {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
  margin-top: 20px;
}
</style>
