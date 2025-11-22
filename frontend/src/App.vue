<script setup>
import { RouterView } from 'vue-router'
import { NConfigProvider } from 'naive-ui'

const themeOverrides = {
  common: {
    primaryColor: '#FF6B35',
    primaryColorHover: '#FF8A65',
    primaryColorPressed: '#E55A2B',
    primaryColorSuppl: '#FF8A65',
    borderRadius: '6px'
  },
  Button: {
    colorPrimary: '#FF6B35',
    colorHoverPrimary: '#FF8A65',
    colorPressedPrimary: '#E55A2B',
    borderPrimary: '#FF6B35',
    borderRadius: '80px',
    borderRadiusMedium: '10px',
    heightMedium: '40px'
  },
  Input: {
    borderRadius: '6px',
    border: '1px solid #E0E0E0',
    borderFocus: '1px solid #FF6B35',
    borderHover: '1px solid #FF8A65',
    boxShadowFocus: '0 0 0 2px rgba(255, 107, 53, 0.2)'
  }
}
</script>

<template>
  <div class="page-wrapper">
    <NConfigProvider :theme-overrides="themeOverrides">
      <RouterView />
    </NConfigProvider>
  </div>
</template>

<style scoped>
  .page-wrapper {
    max-width: 400px;
    min-height: 100vh;
    margin: 0 auto;
  }
</style>
