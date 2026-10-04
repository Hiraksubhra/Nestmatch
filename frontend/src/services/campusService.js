import api from './api'

export const campusService = {
  // Get list of campuses (optionally filtered by city)
  getCampuses: async (city = null) => {
    const params = city ? { city } : {}
    return api.get('/campuses', { params })
  },

  // Get details for a single campus
  getCampusById: async (id) => {
    return api.get(`/campuses/${id}`)
  },
}
