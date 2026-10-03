import api from './api'

export const flatmateService = {
  // Browse flatmate profiles with filters
  browseFlatmates: async (params = {}) => {
    const searchParams = new URLSearchParams()
    if (params.city) searchParams.append('city', params.city)
    if (params.university) searchParams.append('university', params.university)
    if (params.min_budget) searchParams.append('min_budget', params.min_budget)
    if (params.max_budget) searchParams.append('max_budget', params.max_budget)
    if (params.gender && params.gender !== 'ANY') searchParams.append('gender', params.gender)
    if (params.min_match !== undefined && params.min_match !== null && params.min_match !== '') {
      searchParams.append('min_match', params.min_match)
    }
    if (params.tags && params.tags.length > 0) searchParams.append('tags', params.tags.join(','))
    if (params.page) searchParams.append('page', params.page)
    if (params.limit) searchParams.append('limit', params.limit)

    const query = searchParams.toString()
    return await api.get(`/flatmates${query ? `?${query}` : ''}`)
  },

  // Get current user's profile
  getMyProfile: async () => {
    return await api.get('/flatmates/me')
  },

  // Create or update profile
  saveMyProfile: async (data) => {
    return await api.post('/flatmates', data)
  },

  // Deactivate profile
  deactivateMyProfile: async () => {
    return await api.delete('/flatmates/me')
  },

  // Get a specific flatmate profile by ID
  getProfileById: async (id) => {
    return await api.get(`/flatmates/${id}`)
  },
}

export default flatmateService
