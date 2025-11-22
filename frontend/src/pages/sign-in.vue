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
</script>

<style scoped>
.page-wrapper {
  background-color: #F7742A;
}

form {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

form button {
  border: none;
  background-color: transparent;
  color: #CACACA;
  display: flex;
  justify-content: flex-end;
}

.header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 31px 24px;
}

.header h2 {
  color: white;
  margin: 0;
}

.header button {
  margin: 0;
  padding: 0;

}



.login {
  background-color: white;
  border-radius: 5%;
  padding: 24px;
  border: none;
  border-top: 2px solid white;
  display: flex;
  flex-direction: column;
  gap: 65px;
  padding-bottom: 20%;
}

h1 {
  padding: 0;
  margin: 0;
}

.hello {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

p {
  padding: 0;
  margin: 0;
}

.logo {
  display: flex;
  justify-content: center;
}
</style>
