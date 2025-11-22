import { defineStore } from 'pinia'
import axios from 'axios'

export const baseUrl = 'http://127.0.0.1:8000'

export const useDataStore = defineStore('data', {
  state: () => ({
    auth_key: '',
    role: '',
    books: [],
  }),
  actions: {
    async PostLoginUser(formData) {
      try {
        const response = await axios.post(`${baseUrl}/api/auth/login`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        console.log('Успешный вход:', response.data)

        if (response.data.token) {
          this.auth_key = response.data.token;
          this.role = response.data.role || 'user';
        }

        return response.data
      } catch (error) {
        console.error('Ошибка при входе:', error.response?.data || error.message)
        throw error
      }
    },
    async GetFilterBooks(props) {
      try {
        const response = await axios.get(`${baseUrl}/api/librarian/books?${props}`)
        console.log(response)
        console.log('Данные успешно получены:', response.data)
        this.books = response.data
      } catch (error) {
        console.error('Ошибка при получении данных:', error.response?.data || error.message)
        throw error
      }
    }
  },
  getters: {
    getBooks: (state) => state.books,
  },
  persist: {
    key: 'data-store',
    storage: localStorage,
    paths: ['auth_key', 'role', 'books'],
  },
})
