import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import NaiveUI from 'naive-ui'

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
    borderRadius: '8px',
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

import App from './App.vue'
import router from './router'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(NaiveUI, {
  themeOverrides: themeOverrides
})

app.mount('#app')
