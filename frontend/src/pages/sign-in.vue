<template>
  <div class="page-wrapper">
    <div class="header">
      <IconBtn><img src='../../public/assets/icon-arrow.svg'></IconBtn>
      <h2>Авторизация</h2>
    </div>
    <div class="login">
      <div class="hello">
        <h1>С возвращением!</h1>
        <p>Войди в систему, чтобы продолжить</p>
      </div>
      <div class="logo">
        <img src="../../public/assets/logo.svg" atl="Логотип"></img>
      </div>
      <form>
        <NInput placeholder="Логин"></NInput>
        <NInput placeholder="Пароль"></NInput>
        <button>Забыли свой пароль?</button>
      </form>
      <NButton>Войти</NButton>
    </div>
  </div>
</template>

<script setup>
import { NInput } from 'naive-ui';
import { NButton } from 'naive-ui';
import iconBtn from '@/components/ui/icon-btn.vue';
import IconBtn from '@/components/ui/icon-btn.vue';
</script>

<style scoped>
.page-wrapper {
  background-color: ;
}
</style>
