import React from 'react'
import { Link } from 'react-router-dom'
import { MapPin, ShieldCheck, Heart, UserCheck } from 'lucide-react'
import { AmenityIcon } from './AmenityIcon'
import { getImageUrl } from '../../lib/utils'

// Default fallback images for student rooms
const DEFAULT_IMAGES = [
  'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=800&q=80',
]

export const ListingCard = ({ listing, onBookmarkToggle, isBookmarked = false }) => {
  const fallbackPhoto = DEFAULT_IMAGES[Math.abs(listing.title?.length || 0) % DEFAULT_IMAGES.length]
  const rawPhoto =
    listing.photos?.find((p) => p.is_cover)?.url ||
    listing.photos?.[0]?.url

  const coverPhoto = getImageUrl(rawPhoto, fallbackPhoto)

  const formattedRent = Number(listing.rent_amount || 0).toLocaleString('en-IN')

  const universityInfo = Array.isArray(listing.university_proximity) && listing.university_proximity.length > 0
    ? listing.university_proximity[0]
    : null

  return (
    <div className="group bg-white rounded-2xl border border-neutral-200 overflow-hidden shadow-card hover:shadow-card-hover transition-all duration-300 flex flex-col">
      {/* Photo Container */}
      <div className="relative aspect-[4/3] w-full overflow-hidden bg-neutral-100">
        <Link to={`/listings/${listing.id}`}>
          <img
            src={coverPhoto}
            alt={listing.title}
            onError={(e) => {
              e.currentTarget.onerror = null
              e.currentTarget.src = fallbackPhoto
            }}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />
        </Link>

        {/* Badges Overlay */}
        <div className="absolute top-3 left-3 flex flex-wrap gap-1.5 items-center">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide uppercase bg-primary text-white shadow-sm">
            {listing.property_type?.replace('_', ' ')}
          </span>
          {listing.status === 'ACTIVE' && (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
              <ShieldCheck size={12} className="text-emerald-600" />
              Verified
            </span>
          )}
        </div>

        {/* Gender Badge */}
        <div className="absolute bottom-3 left-3">
          <span className="px-2 py-0.5 rounded-md text-xs font-medium bg-neutral-900/80 text-white backdrop-blur-sm">
            {listing.gender_preference === 'ANY' ? 'All Genders' : `${listing.gender_preference} Only`}
          </span>
        </div>

        {/* Bookmark CTA */}
        {onBookmarkToggle && (
          <button
            onClick={(e) => {
              e.preventDefault()
              onBookmarkToggle(listing.id)
            }}
            className="absolute top-3 right-3 p-2 rounded-full bg-white/90 hover:bg-white text-neutral-600 hover:text-rose-500 shadow-sm backdrop-blur-sm transition-colors"
            title="Save listing"
          >
            <Heart size={16} className={isBookmarked ? 'fill-rose-500 text-rose-500' : ''} />
          </button>
        )}
      </div>

      {/* Details Container */}
      <div className="p-4 flex-1 flex flex-col justify-between">
        <div>
          {/* Location & Proximity */}
          <div className="flex items-center gap-1 text-xs text-neutral-500 mb-1.5">
            <MapPin size={14} className="text-neutral-400 shrink-0" />
            <span className="truncate">
              {listing.locality ? `${listing.locality}, ` : ''}{listing.city}
            </span>
            {universityInfo && (
              <span className="ml-auto font-medium text-primary text-[11px] bg-primary/10 px-2 py-0.5 rounded">
                {universityInfo.distance_km} km to {universityInfo.name}
              </span>
            )}
          </div>

          {/* Title */}
          <Link to={`/listings/${listing.id}`}>
            <h3 className="font-heading font-semibold text-neutral-900 text-base leading-snug group-hover:text-primary transition-colors line-clamp-1">
              {listing.title}
            </h3>
          </Link>

          {/* Key Amenities Preview */}
          <div className="mt-2.5 flex flex-wrap gap-1.5">
            {listing.amenities?.slice(0, 3).map((amenity) => (
              <AmenityIcon
                key={amenity.id || amenity.name}
                name={amenity.name}
                icon={amenity.icon}
                label={amenity.label}
              />
            ))}
            {(listing.amenities?.length || 0) > 3 && (
              <span className="text-[11px] text-neutral-400 self-center">
                +{(listing.amenities?.length || 0) - 3} more
              </span>
            )}
          </div>
        </div>

        {/* Pricing and Action */}
        <div className="mt-4 pt-3 border-t border-neutral-100 flex items-baseline justify-between">
          <div>
            <span className="text-xs text-neutral-500">Rent</span>
            <div className="flex items-baseline gap-1">
              <span className="font-heading font-bold text-lg text-neutral-900">
                ₹{formattedRent}
              </span>
              <span className="text-xs text-neutral-500">/mo</span>
            </div>
          </div>

          <Link
            to={`/listings/${listing.id}`}
            className="text-xs font-semibold text-primary hover:text-primary-dark hover:underline"
          >
            View Details &rarr;
          </Link>
        </div>
      </div>
    </div>
  )
}
