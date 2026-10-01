import api from './api'

export const savedListingService = {
  // Get current user's saved listings
  getSavedListings: async (page = 1, limit = 20) => {
    return await api.get(`/listings/saved?page=${page}&limit=${limit}`)
  },

  // Toggle save/unsave listing
  toggleSaveListing: async (listingId) => {
    return await api.post(`/listings/${listingId}/save`)
  },
}

export default savedListingService
