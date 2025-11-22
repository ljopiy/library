import { defineStore } from 'pinia'
import axios from 'axios'

export const baseUrl = 'http://127.0.0.1:8000/'

export const useDataStore = defineStore('data', {
  state: () => ({
    auth_key: '',
    role: '',
    books: [],
  }),
  actions: {
    async PostNewUser(jsonData) {
      try {
        const response = await axios.post(`${baseUrl}/api/auth/login`, jsonData, {
          headers: {
            'Content-Type': 'application/json',
          },
        })
        console.log('Успешная регистрация:', response.data)
      } catch (error) {
        console.error('Ошибка при регистрации:', error.response?.data || error.message)
        throw error
      }
    },
  },
  getters: {
  },
  persist: {
    key: 'data-store',
    storage: localStorage,
    paths: ['auth_key', 'excursions'],
  },
})
