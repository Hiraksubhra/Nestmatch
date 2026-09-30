import api from './api'

export const authService = {
  async register(userData) {
    return api.post('/auth/register', userData)
  },

  async login(credentials) {
    return api.post('/auth/login', credentials)
  },

  async refresh(refreshToken) {
    return api.post('/auth/refresh', { refresh_token: refreshToken })
  },

  async logout() {
    return api.post('/auth/logout')
  },

  async getMe() {
    return api.get('/users/me')
  },

  async updateMe(userData) {
    return api.put('/users/me', userData)
  },
}
