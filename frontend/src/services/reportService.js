import api from './api'

export const reportService = {
  /**
   * Fetch the list of predefined report reasons
   */
  getReasons: async () => {
    return await api.get('/reports/reasons')
  },

  /**
   * Submit a report against a user (student or landlord)
   * @param {Object} data - { reported_user_id: string, reason: string, details?: string }
   */
  submitReport: async (data) => {
    return await api.post('/reports', data)
  },
}
