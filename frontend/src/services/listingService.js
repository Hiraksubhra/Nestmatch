import api from './api'

export const listingService = {
  // Search / browse listings with filters
  searchListings: async (params = {}) => {
    return api.get('/listings', { params })
  },

  // Get single listing detail by ID
  getListingDetail: async (id) => {
    return api.get(`/listings/${id}`)
  },

  // Get all system amenities
  getAmenities: async () => {
    return api.get('/listings/amenities')
  },

  // Landlord: create new listing
  createListing: async (data) => {
    return api.post('/listings', data)
  },

  // Landlord: update listing
  updateListing: async (id, data) => {
    return api.put(`/listings/${id}`, data)
  },

  // Landlord: archive listing
  archiveListing: async (id) => {
    return api.delete(`/listings/${id}`)
  },

  // Landlord: get my listings
  getMyListings: async (page = 1, limit = 20) => {
    return api.get('/listings/my', { params: { page, limit } })
  },

  // Upload photo
  uploadPhoto: async (listingId, file, isCover = false) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/listings/${listingId}/photos?is_cover=${isCover}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // Delete photo
  deletePhoto: async (listingId, photoId) => {
    return api.delete(`/listings/${listingId}/photos/${photoId}`)
  },
}
