import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Bookmark, BookmarkX, Heart, MapPin, Home, ArrowRight, Sparkles } from 'lucide-react'
import { savedListingService } from '../../services/savedListingService'
import { ROUTES } from '../../constants/routes'
import { Button } from '../../components/ui/Button'
import { Badge } from '../../components/ui/Badge'

export const SavedListings = () => {
  const [savedItems, setSavedItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [removingId, setRemovingId] = useState(null)

  const loadSaved = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await savedListingService.getSavedListings(1, 50)
      setSavedItems(res.data || [])
    } catch (err) {
      setError(err.message || 'Failed to load saved listings')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadSaved()
  }, [])

  const handleRemove = async (listingId, e) => {
    e.preventDefault()
    e.stopPropagation()
    setRemovingId(listingId)
    try {
      await savedListingService.toggleSaveListing(listingId)
      setSavedItems((prev) => prev.filter((item) => item.listing_id !== listingId))
    } catch (err) {
      alert(err.message || 'Failed to remove saved listing')
    } finally {
      setRemovingId(null)
    }
  }

  return (
    <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8 pb-4 border-b border-neutral-200">
        <div>
          <h1 className="text-2xl font-heading font-bold text-neutral-900 flex items-center gap-2">
            <Bookmark className="text-primary fill-primary/20" size={24} /> Saved Listings
          </h1>
          <p className="text-sm text-neutral-500 mt-1">
            Properties you've bookmarked for easy comparison and later review.
          </p>
        </div>
        <Link
          to={ROUTES.SEARCH}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-primary hover:text-primary-dark transition-colors"
        >
          Explore more listings <ArrowRight size={13} />
        </Link>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 bg-white rounded-xl border border-neutral-200">
          <div className="w-8 h-8 border-3 border-primary border-t-transparent rounded-full animate-spin mb-3"></div>
          <p className="text-neutral-500 text-sm">Loading your bookmarked places...</p>
        </div>
      ) : error ? (
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm text-center">
          {error}
        </div>
      ) : savedItems.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 bg-white rounded-2xl border border-neutral-200 text-center px-4">
          <div className="w-16 h-16 rounded-full bg-primary-50 text-primary flex items-center justify-center mb-4">
            <Heart size={32} className="text-primary" />
          </div>
          <h2 className="text-lg font-heading font-semibold text-neutral-900 mb-1">
            No saved listings yet
          </h2>
          <p className="text-sm text-neutral-500 max-w-md mb-6">
            Click the heart icon on any listing card or detail page to save properties here for quick access later.
          </p>
          <Link to={ROUTES.SEARCH}>
            <Button variant="primary">Start Browsing Homes</Button>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {savedItems.map((item) => {
            const listing = item.listing
            if (!listing) return null
            const coverPhoto =
              listing.photos?.find((p) => p.is_cover)?.url ||
              listing.photos?.[0]?.url ||
              'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80'

            return (
              <div
                key={item.listing_id}
                className="bg-white rounded-2xl border border-neutral-200 overflow-hidden hover:shadow-lg transition-all flex flex-col justify-between group"
              >
                <div>
                  {/* Photo Container */}
                  <div className="relative h-48 w-full overflow-hidden bg-neutral-100">
                    <img
                      src={coverPhoto}
                      alt={listing.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div className="absolute top-3 left-3 flex items-center gap-1.5">
                      <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-black/60 text-white backdrop-blur-sm">
                        {listing.property_type}
                      </span>
                    </div>

                    {/* Unsave Button */}
                    <button
                      type="button"
                      onClick={(e) => handleRemove(item.listing_id, e)}
                      disabled={removingId === item.listing_id}
                      className="absolute top-3 right-3 w-9 h-9 rounded-full bg-white/90 hover:bg-white text-red-500 hover:text-red-600 flex items-center justify-center shadow-md transition-all"
                      title="Remove from saved"
                    >
                      <Heart size={18} className="fill-red-500 text-red-500" />
                    </button>
                  </div>

                  {/* Body Content */}
                  <div className="p-4 sm:p-5">
                    <div className="flex items-baseline justify-between mb-1">
                      <span className="text-lg font-bold text-neutral-900">
                        ₹{Number(listing.rent_amount).toLocaleString()}
                        <span className="text-xs font-normal text-neutral-500"> / month</span>
                      </span>
                      {listing.deposit_amount && (
                        <span className="text-xs text-neutral-400">
                          Dep: ₹{Number(listing.deposit_amount).toLocaleString()}
                        </span>
                      )}
                    </div>

                    <h3 className="font-heading font-semibold text-neutral-900 text-base line-clamp-1 group-hover:text-primary transition-colors mb-1">
                      {listing.title}
                    </h3>

                    <p className="text-xs text-neutral-500 flex items-center gap-1 mb-3">
                      <MapPin size={12} className="text-neutral-400 shrink-0" />
                      {listing.locality ? `${listing.locality}, ` : ''}
                      {listing.city}
                    </p>

                    <div className="flex flex-wrap gap-1.5 text-[11px] text-neutral-600">
                      <span className="bg-neutral-100 px-2 py-0.5 rounded font-medium">
                        {listing.furnished_status}
                      </span>
                      <span className="bg-neutral-100 px-2 py-0.5 rounded font-medium capitalize">
                        {listing.gender_preference?.toLowerCase()} Only
                      </span>
                    </div>
                  </div>
                </div>

                {/* Footer Action */}
                <div className="p-4 pt-0">
                  <Link
                    to={ROUTES.LISTING_DETAIL.replace(':id', listing.id)}
                    className="block w-full"
                  >
                    <Button variant="outline" size="sm" className="w-full font-medium">
                      View Property Details
                    </Button>
                  </Link>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default SavedListings
