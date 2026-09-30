import api from './api'

export const messagingService = {
  async getConversations() {
    const res = await api.get('/conversations')
    return res.data
  },

  async getConversation(id) {
    const res = await api.get(`/conversations/${id}`)
    return res.data
  },

  async startConversation(data) {
    const res = await api.post('/conversations', data)
    return res.data
  },

  async getMessages(conversationId, params = {}) {
    const res = await api.get(`/conversations/${conversationId}/messages`, { params })
    return res.data
  },

  async sendMessage(conversationId, data) {
    const res = await api.post(`/conversations/${conversationId}/messages`, data)
    return res.data
  },

  async markAsRead(conversationId) {
    const res = await api.put(`/conversations/${conversationId}/read`)
    return res.data
  },

  getWebSocketUrl(conversationId) {
    const token = localStorage.getItem('access_token')
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const wsBase = apiUrl.replace(/^http/, 'ws')
    return `${wsBase}/api/v1/conversations/ws/${conversationId}?token=${encodeURIComponent(token || '')}`
  }
}

export default messagingService
