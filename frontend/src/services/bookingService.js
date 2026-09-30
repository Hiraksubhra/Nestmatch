import api from './api'

export const bookingService = {
  async createBooking(data) {
    const res = await api.post('/bookings', data)
    return res.data
  },

  async getBookings(status) {
    const params = status ? { status } : {}
    const res = await api.get('/bookings', { params })
    return res.data
  },

  async getBooking(id) {
    const res = await api.get(`/bookings/${id}`)
    return res.data
  },

  async acceptBooking(id) {
    const res = await api.put(`/bookings/${id}/accept`)
    return res.data
  },

  async declineBooking(id) {
    const res = await api.put(`/bookings/${id}/decline`)
    return res.data
  },

  async cancelBooking(id) {
    const res = await api.put(`/bookings/${id}/cancel`)
    return res.data
  }
}

export default bookingService
