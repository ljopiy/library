import { defineStore } from 'pinia'
import axios from 'axios'

export const baseUrl = 'http://127.0.0.1:8000'

export const useDataStore = defineStore('data', {
  state: () => ({
    auth_key: '',
    role: '',
    books: [],
    booksCopy: [],
    userInfo: [],
    orderList: [],
    newUserData: [],
    bookedList: []
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
    async PostLoginUser(formData) {
      try {
        this.clearTokenRole()
        const response = await axios.post(`${baseUrl}/api/auth/login`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        console.log('Успешный вход:', response.data)
        this.setTokenRole(response.data.access_token, response.data.role)
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
    },
    async GetCopiesBook(props){
        try {
          const response = await axios.get(`${baseUrl}/api/librarian/book_copies/book/${props}/`, {
          headers: {
            Authorization: `Bearer ${this.auth_key}`,
            'Content-Type': 'application/json',
          },
        })
        console.log(response)
        console.log('Данные успешно получены:', response.data)
        this.booksCopy = response.data
      } catch (error) {
        console.log(this.auth_key)
        console.error('Ошибка при получении данных:', error.response?.data || error.message)
        throw error
      }
    },
    async PostOrder(id){
      try {
        const response = await axios.post(`${baseUrl}/api/orders/`,
          { // данные запроса (body)
            copy_ids: [id] // или copy_id: id в зависимости от API
          },
          { // конфигурация (включая headers)
            headers: {
              Authorization: `Bearer ${this.auth_key}`,
              'Content-Type': 'application/json',
            }
          }
        )

        console.log('Заказ создан:', response.data)
        return response.data

      } catch (error) {
        console.error('Error creating order:', error.response?.data || error.message)
        throw error
      }
    },
    async GetUserInfo(props){
        try {
          const response = await axios.get(`${baseUrl}/api/me/`, {
          headers: {
            Authorization: `Bearer ${this.auth_key}`,
            'Content-Type': 'application/json',
          },
        })
        console.log(response)
        console.log('Данные успешно получены:', response.data)
        this.userInfo = response.data
      } catch (error) {
        console.log(this.auth_key)
        console.error('Ошибка при получении данных:', error.response?.data || error.message)
        throw error
      }
    },
    async updateUserInfo(email){
        try {
          const response = await axios.put(`${baseUrl}/api/me/`,
            {
              "full_name": this.userInfo.full_name || 'User', // реальное имя
              "email": email, // новый email
              "role": this.userInfo.role, // реальная роль
              "is_active": this.userInfo.is_active // реальный статус
            },
        {
          headers: {
            Authorization: `Bearer ${this.auth_key}`,
            'Content-Type': 'application/json',
          }
        })

        console.log('Данные обновлены:', response.data)
        return response.data

      } catch (error) {
        console.error('Error updating user:', error.response?.data || error.message)
        throw error
      }
    },
    async GetOrderList(){
        try {
          const response = await axios.get(`${baseUrl}/api/orders/my`, {
          headers: {
            Authorization: `Bearer ${this.auth_key}`,
            'Content-Type': 'application/json',
          },
        })
        console.log(response)
        console.log('Данные успешно получены:', response.data)
        this.orderList = response.data
      } catch (error) {
        console.log(this.auth_key)
        console.error('Ошибка при получении данных:', error.response?.data || error.message)
        throw error
      }
    },
    async getAllBooked(){
        try {
          const response = await axios.get(`${baseUrl}/api/orders/`, {
          headers: {
            Authorization: `Bearer ${this.auth_key}`,
            'Content-Type': 'application/json',
          },
        })
        console.log(response)
        console.log('Брони:', response.data)
        this.bookedList = response.data
      } catch (error) {
        console.log(this.auth_key)
        console.error('Ошибка при получении данных:', error.response?.data || error.message)
        throw error
      }
    },
    async deletOrder(id){
      try {
          const response = await axios.delete(`${baseUrl}/api/orders/${id}/cancel`, {
          headers: {
            Authorization: `Bearer ${this.auth_key}`,
            'Content-Type': 'application/json',
          },
        })
        console.log(response)
        console.log('Отменено', response.data)
      } catch (error) {
        console.log(this.auth_key)
        console.error('Ошибка отмены', error.response?.data || error.message)
        throw error
      }
    },
    async creatUser() {
      try {
        const formData = new FormData();
        formData.append('role', 'admin');

        const response = await axios.post(`${baseUrl}/api/auth/register`, formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        });
        console.log('Пользователь создан:', response.data);
        this.newUserData = response.data
        return response.data;
      } catch (error) {
        console.error('Ошибка при создании пользователя:', error.response?.data || error.message);
        throw error;
      }
    },
    // В вашем store (counter.js) добавьте этот метод в actions:
async createBook(bookData) {
  try {
    const response = await axios.post(`${baseUrl}/api/librarian/books/`, bookData, {
      headers: {
        Authorization: `Bearer ${this.auth_key}`,
        'Content-Type': 'application/json',
      }
    });

    console.log('Книга создана:', response.data);
    return response.data;

  } catch (error) {
    console.error('Ошибка при создании книги:', error.response?.data || error.message);
    throw error;
  }
},
  },

  getters: {
    getBooks: (state) => state.books,
    сopiesBook: (state) => state.booksCopy,
    orderListget: (state) => state.orderList,
    getNewUser: (state) => state.newUserData,
    booked: (state) => state.bookedList
  },
  persist: {
    key: 'data-store',
    storage: localStorage,
    paths: ['role', 'books'],
  },
})
