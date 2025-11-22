import { defineStore } from 'pinia'
import axios from 'axios'

export const baseUrl = 'http://127.0.0.1:5000/'

export const useDataStore = defineStore('data', {
  state: () => ({
    auth_key: '',
    role: '',
    excursions: [],
    residentExcursions: [],
    excursionDetail: [],
    profileData: [],
    reservationsData: [],
  }),
  actions: {
    setTokenRole(auth_key, role) {
      this.auth_key = auth_key
      this.role = role
    },
    clearTokenRole() {
      this.auth_key = ''
      this.role = ''
    },
    deletEvent() {
      this.residentExcursions = []
    },
    async PostNewUser(jsonData) {
      try {
        const response = await axios.post(`${baseUrl}/api/user/register`, jsonData, {
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
    getProfileData: (state) => state.profileData,
    getExcursions: (state) => state.excursions,
    getExcursionDetail: (state) => state.excursionDetail,
    getResidentEvents: (state) => state.residentExcursions,
  },
  persist: {
    key: 'data-store',
    storage: localStorage,
    paths: ['auth_key', 'excursions'],
  },
})
