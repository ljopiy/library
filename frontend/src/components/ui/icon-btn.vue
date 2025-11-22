<template>
  <button><slot>a</slot></button>
</template>

<script setup>

</script>

<style scoped>
button{
  all: unset;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
  transition: all 0.3s ease;
  border-radius: 100%;
  min-height: 30px;
  min-width: 30px;
}

button:hover {
  background-color: rgba(186, 186, 186, 0.568);
}

button:active {
  background-color: rgb(190, 190, 190);
}
</style>
