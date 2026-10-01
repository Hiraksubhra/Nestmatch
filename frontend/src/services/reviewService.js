import api from './api'

export const reviewService = {
  // Get reviews summary and list for a listing
  getListingReviews: async (listingId) => {
    return await api.get(`/listings/${listingId}/reviews`)
  },

  // Submit a review for a listing
  submitReview: async (listingId, data) => {
    return await api.post(`/listings/${listingId}/reviews`, data)
  },
}

export default reviewService
