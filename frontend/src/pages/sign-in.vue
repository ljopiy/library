<template>
  <div class="page-wrapper">
    <div class="header">
      <IconBtn><img src='../../public/assets/icon/icon-arrow.svg'></IconBtn>
      <h2>Авторизация</h2>
    </div>
    <div class="login">
      <div class="hello">
        <h1>С возвращением!</h1>
        <p>Войди в систему, чтобы продолжить</p>
      </div>
      <div class="logo">
        <img src="../../public/assets/icon/logo.svg" atl="Логотип"></img>
      </div>
      <form @submit.prevent="handleLogin">
        <NInput
          v-model:value="username"
          placeholder="Логин"
          :status="error ? 'error' : ''"
        ></NInput>
        <NInput
          v-model:value="password"
          type="password"
          placeholder="Пароль"
          :status="error ? 'error' : ''"
          show-password-on="click"
        ></NInput>
        <button type="button">Забыли свой пароль?</button>
      </form>
      <NButton
        type="primary"
        @click="handleLogin"
        :loading="loading"
      >Войти</NButton>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { NInput, NButton } from 'naive-ui';
import IconBtn from '@/components/ui/icon-btn.vue';
import { useDataStore } from '@/stores/counter';

const router = useRouter();
const dataStore = useDataStore();

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref(false);

const handleLogin = async () => {
  if (!username.value || !password.value) {
    error.value = true;
    return;
  }

  loading.value = true;
  error.value = false;

  try {
    const loginData = {
      username: username.value,
      password: password.value
    };

    const response = await dataStore.loginUser(loginData);

    // Сохраняем токен если он есть в ответе
    if (response.token) {
      dataStore.auth_key = response.token;
      dataStore.role = response.role || 'user';
    }

    // Перенаправляем на главную
    router.push('/');

  } catch (err) {
    error.value = true;
    console.error('Ошибка входа:', err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.page-wrapper {
  background-color: #F7742A;
  display: flex;
  flex-direction: column;

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
  border-radius: 20px 20px 0 0;

  padding: 24px;
  border: none;

  display: flex;
  flex-direction: column;
  gap: 65px;
  padding-bottom: 20%;
  flex: 1;
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
