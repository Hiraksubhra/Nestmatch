import React, { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import {
  MapPin,
  ShieldCheck,
  Calendar,
  Users,
  Home,
  Clock,
  Sparkles,
  ArrowLeft,
  Share2,
  Heart,
  Phone,
  MessageSquare,
  AlertCircle,
  Building,
  Lock,
  LogIn,
  CheckCircle,
  X,
  CreditCard,
} from 'lucide-react'
import { ROUTES } from '../../constants/routes'
import { listingService } from '../../services/listingService'
import { messagingService } from '../../services/messagingService'
import { bookingService } from '../../services/bookingService'
import { AmenityIcon } from '../../components/listings/AmenityIcon'
import { useAuthStore } from '../../store/authStore'
import { getImageUrl, formatCurrency } from '../../lib/utils'

const DEFAULT_IMAGES = [
  'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=1200&q=80',
  'https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=800&q=80',
]

export const ListingDetail = () => {
  const { id } = useParams()
  const { user, isAuthenticated } = useAuthStore()

  const [listing, setListing] = useState(null)
  const [selectedPhotoIndex, setSelectedPhotoIndex] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()
  const [inquirySent, setInquirySent] = useState(false)
  const [inquiryText, setInquiryText] = useState('')
  const [inquirySubmitting, setInquirySubmitting] = useState(false)

  // Booking Modal States
  const [isBookingModalOpen, setIsBookingModalOpen] = useState(false)
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  const [moveInDate, setMoveInDate] = useState(tomorrow.toISOString().split('T')[0])
  const [durationMonths, setDurationMonths] = useState(3)
  const [bookingMessage, setBookingMessage] = useState('')
  const [bookingSubmitting, setBookingSubmitting] = useState(false)
  const [bookingError, setBookingError] = useState(null)
  const [bookingSuccess, setBookingSuccess] = useState(false)

  useEffect(() => {
    setIsLoading(true)
    listingService
      .getListingDetail(id)
      .then((res) => {
        if (res.success && res.data) {
          setListing(res.data)
          if (res.data.min_stay_months) {
            setDurationMonths(res.data.min_stay_months)
          }
        }
      })
      .catch((err) => {
        setError(err.message || 'Failed to load listing details')
      })
      .finally(() => {
        setIsLoading(false)
      })
  }, [id])

  if (isLoading) {
    return (
      <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4" />
        <p className="text-neutral-500">Loading accommodation details...</p>
      </div>
    )
  }

  if (error || !listing) {
    return (
      <div className="max-w-md mx-auto my-16 p-8 bg-white rounded-2xl border border-neutral-200 text-center">
        <AlertCircle size={48} className="text-rose-500 mx-auto mb-3" />
        <h2 className="text-xl font-heading font-bold text-neutral-900 mb-2">Listing Not Found</h2>
        <p className="text-sm text-neutral-600 mb-6">{error || 'This listing may have been deactivated or removed.'}</p>
        <Link
          to="/search"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary text-white rounded-xl text-sm font-medium hover:bg-primary-dark transition-colors"
        >
          <ArrowLeft size={16} />
          Back to Search
        </Link>
      </div>
    )
  }

  const photos =
    listing.photos && listing.photos.length > 0
      ? listing.photos.map((p, idx) => getImageUrl(p.url, DEFAULT_IMAGES[idx % DEFAULT_IMAGES.length]))
      : DEFAULT_IMAGES

  const universityInfo =
    Array.isArray(listing.university_proximity) && listing.university_proximity.length > 0
      ? listing.university_proximity[0]
      : null

  const handleInquirySubmit = async (e) => {
    e.preventDefault()
    if (!inquiryText.trim() || inquirySubmitting) return

    try {
      setInquirySubmitting(true)
      const conv = await messagingService.startConversation({
        listing_id: listing.id,
        initial_message: inquiryText.trim()
      })
      navigate(`/messages/${conv.id}`)
    } catch (err) {
      console.error('Failed to start conversation:', err)
      alert(err.message || 'Failed to send inquiry')
    } finally {
      setInquirySubmitting(false)
    }
  }

  const handleBookingSubmit = async (e) => {
    e.preventDefault()
    setBookingError(null)

    try {
      setBookingSubmitting(true)
      await bookingService.createBooking({
        listing_id: listing.id,
        move_in_date: moveInDate,
        duration_months: parseInt(durationMonths, 10),
        message: bookingMessage.trim() || undefined
      })
      setBookingSuccess(true)
    } catch (err) {
      setBookingError(err.message || 'Failed to submit booking request')
    } finally {
      setBookingSubmitting(false)
    }
  }

  return (
    <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back breadcrumb */}
      <div className="mb-6 flex items-center justify-between">
        <Link
          to="/search"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-neutral-600 hover:text-primary transition-colors"
        >
          <ArrowLeft size={16} />
          Back to Search Results
        </Link>
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              if (navigator.share) {
                navigator.share({ title: listing.title, url: window.location.href })
              } else {
                navigator.clipboard.writeText(window.location.href)
                alert('Listing link copied to clipboard!')
              }
            }}
            className="p-2 rounded-xl border border-neutral-200 hover:bg-neutral-50 text-neutral-600 transition-colors"
            title="Share"
          >
            <Share2 size={18} />
          </button>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Photos + Info */}
        <div className="lg:col-span-2 space-y-8">
          {/* Photo Gallery */}
          <div className="space-y-3">
            <div className="relative aspect-[16/10] w-full rounded-2xl overflow-hidden bg-neutral-900 border border-neutral-200 shadow-sm">
              <img
                src={photos[selectedPhotoIndex] || photos[0]}
                alt={listing.title}
                onError={(e) => {
                  e.currentTarget.onerror = null
                  e.currentTarget.src = DEFAULT_IMAGES[0]
                }}
                className="w-full h-full object-cover"
              />
              <div className="absolute top-4 left-4 flex gap-2">
                <span className="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-primary text-white shadow-md">
                  {listing.property_type?.replace('_', ' ')}
                </span>
                {listing.status === 'ACTIVE' && (
                  <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500 text-white shadow-md">
                    <ShieldCheck size={14} />
                    Verified Property
                  </span>
                )}
              </div>
            </div>

            {/* Thumbnail Strip */}
            {photos.length > 1 && (
              <div className="flex gap-2 overflow-x-auto pb-2">
                {photos.map((url, idx) => (
                  <button
                    key={idx}
                    onClick={() => setSelectedPhotoIndex(idx)}
                    className={`relative w-20 h-16 rounded-xl overflow-hidden shrink-0 border-2 transition-all ${
                      selectedPhotoIndex === idx
                        ? 'border-primary ring-2 ring-primary/20 scale-95'
                        : 'border-transparent opacity-70 hover:opacity-100'
                    }`}
                  >
                    <img
                      src={url}
                      alt={`Thumbnail ${idx + 1}`}
                      onError={(e) => {
                        e.currentTarget.onerror = null
                        e.currentTarget.src = DEFAULT_IMAGES[idx % DEFAULT_IMAGES.length]
                      }}
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Title & Location Header */}
          <div className="bg-white p-6 rounded-2xl border border-neutral-200 shadow-sm space-y-4">
            <div>
              <div className="flex items-center gap-2 text-sm text-neutral-500 mb-2">
                <MapPin size={16} className="text-primary shrink-0" />
                <span>
                  {listing.address_line1 ? `${listing.address_line1}, ` : ''}
                  {listing.locality ? `${listing.locality}, ` : ''}
                  {listing.city} {listing.pincode ? `- ${listing.pincode}` : ''}
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-heading font-bold text-neutral-900 leading-tight">
                {listing.title}
              </h1>
            </div>

            {universityInfo && (
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-primary/10 text-primary font-medium text-sm">
                <Sparkles size={16} />
                <span>
                  Only {universityInfo.distance_km} km from {universityInfo.name}
                </span>
              </div>
            )}

            {/* Key Specs Pills */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-neutral-100">
              <div className="bg-neutral-50 p-3 rounded-xl">
                <span className="text-xs text-neutral-500 block">Gender</span>
                <span className="font-heading font-semibold text-neutral-900 text-sm">
                  {listing.gender_preference === 'ANY' ? 'All Genders' : `${listing.gender_preference} Only`}
                </span>
              </div>
              <div className="bg-neutral-50 p-3 rounded-xl">
                <span className="text-xs text-neutral-500 block">Furnishing</span>
                <span className="font-heading font-semibold text-neutral-900 text-sm">
                  {listing.furnished_status}
                </span>
              </div>
              <div className="bg-neutral-50 p-3 rounded-xl">
                <span className="text-xs text-neutral-500 block">Min Stay</span>
                <span className="font-heading font-semibold text-neutral-900 text-sm">
                  {listing.min_stay_months} Months
                </span>
              </div>
              <div className="bg-neutral-50 p-3 rounded-xl">
                <span className="text-xs text-neutral-500 block">Occupancy</span>
                <span className="font-heading font-semibold text-neutral-900 text-sm">
                  Max {listing.max_occupancy} Person(s)
                </span>
              </div>
            </div>
          </div>

          {/* Description */}
          {listing.description && (
            <div className="bg-white p-6 rounded-2xl border border-neutral-200 shadow-sm space-y-3">
              <h2 className="text-lg font-heading font-semibold text-neutral-900">About this accommodation</h2>
              <p className="text-neutral-700 text-sm leading-relaxed whitespace-pre-line">{listing.description}</p>
            </div>
          )}

          {/* Amenities Grid */}
          <div className="bg-white p-6 rounded-2xl border border-neutral-200 shadow-sm space-y-4">
            <h2 className="text-lg font-heading font-semibold text-neutral-900">Amenities & Services Included</h2>
            {listing.amenities && listing.amenities.length > 0 ? (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {listing.amenities.map((amenity) => (
                  <div
                    key={amenity.id || amenity.name}
                    className="flex items-center gap-2.5 p-3 rounded-xl bg-neutral-50 border border-neutral-100"
                  >
                    <AmenityIcon name={amenity.name} icon={amenity.icon} size={18} className="bg-transparent p-0" />
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-neutral-500">Contact the landlord for specific amenity details.</p>
            )}
          </div>
        </div>

        {/* Right Column: Pricing & Inquiry Card */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-neutral-200 shadow-card sticky top-24 space-y-6">
            <div>
              <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">Monthly Rent</span>
              <div className="flex items-baseline gap-1 mt-1">
                <span className="font-heading font-bold text-3xl text-neutral-900">
                  ₹{Number(listing.rent_amount).toLocaleString('en-IN')}
                </span>
                <span className="text-sm text-neutral-500">/{listing.rent_period?.toLowerCase() || 'month'}</span>
              </div>
              {listing.deposit_amount && (
                <div className="mt-2 text-xs text-neutral-600 flex justify-between pb-3 border-b border-neutral-100">
                  <span>Security Deposit:</span>
                  <span className="font-medium text-neutral-900">
                    ₹{Number(listing.deposit_amount).toLocaleString('en-IN')}
                  </span>
                </div>
              )}
            </div>

            {/* Inquire Box */}
            <div className="space-y-3">
              <h3 className="text-sm font-semibold text-neutral-900">Contact Landlord Directly</h3>

              {!isAuthenticated ? (
                <div className="p-5 bg-gradient-to-br from-neutral-50 to-neutral-100/70 border border-neutral-200 rounded-2xl text-center space-y-3">
                  <div className="w-12 h-12 rounded-full bg-primary/10 text-primary flex items-center justify-center mx-auto">
                    <Lock size={22} />
                  </div>
                  <div>
                    <h4 className="font-heading font-semibold text-neutral-900 text-sm">
                      Sign in to contact landlord
                    </h4>
                    <p className="text-xs text-neutral-500 mt-1 leading-relaxed">
                      To prevent spam and protect our student community, please sign in to send inquiries or schedule viewings.
                    </p>
                  </div>
                  <div className="pt-1 space-y-2">
                    <Link
                      to={ROUTES.LOGIN}
                      state={{ from: { pathname: `/listings/${id}` } }}
                      className="w-full py-2.5 px-4 bg-primary hover:bg-primary-dark text-white rounded-xl text-sm font-semibold transition-colors shadow-sm flex items-center justify-center gap-2"
                    >
                      <LogIn size={16} />
                      Sign in to Send Inquiry
                    </Link>
                    <p className="text-xs text-neutral-500">
                      New to NestMatch?{' '}
                      <Link
                        to={ROUTES.REGISTER}
                        state={{ from: { pathname: `/listings/${id}` } }}
                        className="text-primary font-medium hover:underline"
                      >
                        Create free account
                      </Link>
                    </p>
                  </div>
                </div>
              ) : user?.id === listing.landlord_id ? (
                <div className="p-4 bg-primary/5 border border-primary/20 rounded-xl space-y-2 text-center">
                  <Building size={24} className="text-primary mx-auto" />
                  <p className="text-sm font-semibold text-neutral-900">Your Property Listing</p>
                  <p className="text-xs text-neutral-600">
                    You are the owner of this accommodation. You can manage photos, price, or availability from your portal.
                  </p>
                  <Link
                    to={ROUTES.MY_LISTINGS}
                    className="mt-2 w-full inline-flex items-center justify-center py-2 px-3 bg-white border border-primary/30 text-primary hover:bg-primary hover:text-white rounded-xl text-xs font-semibold transition-colors"
                  >
                    Manage in My Listings
                  </Link>
                </div>
              ) : user?.role === 'LANDLORD' ? (
                <div className="p-4 bg-neutral-50 border border-neutral-200 rounded-xl text-center space-y-1.5">
                  <p className="text-xs font-semibold text-neutral-700">Landlord Account Active</p>
                  <p className="text-xs text-neutral-500 leading-relaxed">
                    You are signed in as a landlord. Student inquiries and visit requests can only be sent from student accounts.
                  </p>
                </div>
              ) : inquirySent ? (
                <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-center space-y-2">
                  <ShieldCheck size={28} className="text-emerald-600 mx-auto" />
                  <p className="text-sm font-semibold text-emerald-800">Inquiry Sent to Landlord!</p>
                  <p className="text-xs text-emerald-600">
                    The property owner has received your message and will respond shortly via in-app chat.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  <button
                    onClick={() => {
                      setIsBookingModalOpen(true)
                      setBookingSuccess(false)
                      setBookingError(null)
                    }}
                    className="w-full py-3.5 bg-primary hover:bg-primary-dark text-white rounded-xl text-sm font-bold transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2"
                  >
                    <Calendar size={18} />
                    Request to Book Property
                  </button>

                  <div className="relative flex py-1 items-center">
                    <div className="flex-grow border-t border-neutral-200"></div>
                    <span className="flex-shrink mx-3 text-neutral-400 text-xs uppercase font-medium">Or Ask Questions</span>
                    <div className="flex-grow border-t border-neutral-200"></div>
                  </div>

                  <form onSubmit={handleInquirySubmit} className="space-y-3">
                    <textarea
                      rows={3}
                      placeholder="Hi! I am a student interested in renting this place. Is it available for a viewing?"
                      value={inquiryText}
                      onChange={(e) => setInquiryText(e.target.value)}
                      required
                      className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary resize-none"
                    />
                    <button
                      type="submit"
                      disabled={inquirySubmitting}
                      className="w-full py-2.5 bg-white border border-primary text-primary hover:bg-primary/5 rounded-xl text-sm font-semibold transition-colors flex items-center justify-center gap-2"
                    >
                      <MessageSquare size={16} />
                      {inquirySubmitting ? 'Starting Chat...' : 'Send Message to Landlord'}
                    </button>
                  </form>
                </div>
              )}
            </div>

            {/* NestMatch Scam-Free Guarantee */}
            <div className="p-4 rounded-xl bg-blue-50 border border-blue-100 text-xs text-blue-900 space-y-1.5">
              <div className="flex items-center gap-1.5 font-semibold text-blue-800">
                <ShieldCheck size={16} className="text-primary" />
                <span>NestMatch Student Protection</span>
              </div>
              <p className="text-blue-700 leading-relaxed">
                Never pay cash or wire funds outside NestMatch. Verified listings are protected by our rent protection
                policy.
              </p>
            </div>

            {/* Landlord Profile Snapshot */}
            {listing.landlord && (
              <div className="pt-4 border-t border-neutral-100 flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-primary/10 text-primary font-bold flex items-center justify-center shrink-0">
                  {listing.landlord.full_name?.charAt(0) || 'L'}
                </div>
                <div className="truncate">
                  <span className="text-xs text-neutral-400 block">Listed by</span>
                  <span className="font-semibold text-neutral-900 text-sm truncate block">
                    {listing.landlord.full_name}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Request to Book Modal */}
      {isBookingModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-neutral-100 relative animate-in fade-in zoom-in-95 duration-200">
            <button
              onClick={() => setIsBookingModalOpen(false)}
              className="absolute top-4 right-4 p-1.5 text-neutral-400 hover:text-neutral-700 rounded-lg hover:bg-neutral-100"
            >
              <X size={18} />
            </button>

            {bookingSuccess ? (
              <div className="py-6 text-center space-y-4">
                <div className="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
                  <CheckCircle size={32} />
                </div>
                <h3 className="text-xl font-bold font-heading text-neutral-900">
                  Booking Request Submitted!
                </h3>
                <p className="text-sm text-neutral-600 leading-relaxed">
                  Your request for <span className="font-semibold">{listing.title}</span> has been sent to the landlord.
                  You can track the approval status and view confirmed contacts in your dashboard.
                </p>
                <div className="pt-4 flex flex-col sm:flex-row gap-3 justify-center">
                  <button
                    onClick={() => {
                      setIsBookingModalOpen(false)
                      navigate('/bookings')
                    }}
                    className="px-5 py-2.5 bg-primary text-white rounded-xl text-sm font-semibold hover:bg-primary-dark transition shadow-sm"
                  >
                    View My Bookings
                  </button>
                  <button
                    onClick={() => setIsBookingModalOpen(false)}
                    className="px-5 py-2.5 border border-neutral-200 text-neutral-700 rounded-xl text-sm font-medium hover:bg-neutral-50 transition"
                  >
                    Stay on Listing
                  </button>
                </div>
              </div>
            ) : (
              <form onSubmit={handleBookingSubmit} className="space-y-4">
                <div className="flex items-center gap-2 text-primary font-bold text-lg border-b border-neutral-100 pb-3">
                  <Calendar size={22} />
                  <span>Request to Book Accommodation</span>
                </div>

                {bookingError && (
                  <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 flex items-center gap-2">
                    <AlertCircle size={16} className="shrink-0" />
                    <span>{bookingError}</span>
                  </div>
                )}

                <div className="bg-neutral-50 p-3 rounded-xl flex items-center justify-between text-xs">
                  <div>
                    <span className="text-neutral-400 block">Property</span>
                    <span className="font-semibold text-neutral-900 truncate block max-w-xs">{listing.title}</span>
                  </div>
                  <div className="text-right">
                    <span className="text-neutral-400 block">Rent</span>
                    <span className="font-bold text-primary">{formatCurrency(listing.rent_amount)}/mo</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-neutral-700 mb-1">
                      Requested Move-in Date *
                    </label>
                    <input
                      type="date"
                      min={tomorrow.toISOString().split('T')[0]}
                      value={moveInDate}
                      onChange={(e) => setMoveInDate(e.target.value)}
                      required
                      className="w-full p-2.5 bg-neutral-50 border border-neutral-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-neutral-700 mb-1">
                      Stay Duration (Months) *
                    </label>
                    <select
                      value={durationMonths}
                      onChange={(e) => setDurationMonths(e.target.value)}
                      className="w-full p-2.5 bg-neutral-50 border border-neutral-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
                    >
                      {[1, 2, 3, 6, 9, 12].map((m) => (
                        <option key={m} value={m}>
                          {m} Month{m > 1 ? 's' : ''}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Pricing Estimate */}
                <div className="p-3 bg-primary/5 border border-primary/20 rounded-xl text-xs space-y-1.5">
                  <div className="flex justify-between text-neutral-600">
                    <span>Rent ({durationMonths} months × {formatCurrency(listing.rent_amount)})</span>
                    <span>{formatCurrency(listing.rent_amount * durationMonths)}</span>
                  </div>
                  {listing.deposit_amount && (
                    <div className="flex justify-between text-neutral-600">
                      <span>Security Deposit (refundable)</span>
                      <span>{formatCurrency(listing.deposit_amount)}</span>
                    </div>
                  )}
                  <div className="border-t border-primary/20 pt-1 flex justify-between font-bold text-neutral-900 text-sm">
                    <span>Total Estimate</span>
                    <span className="text-primary">
                      {formatCurrency(listing.rent_amount * durationMonths + (listing.deposit_amount || 0))}
                    </span>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-neutral-700 mb-1">
                    Introduction / Note to Landlord (Optional)
                  </label>
                  <textarea
                    rows={2}
                    placeholder="Tell the landlord about your college/course, move-in flexibility, or requirements..."
                    value={bookingMessage}
                    onChange={(e) => setBookingMessage(e.target.value)}
                    className="w-full p-2.5 bg-neutral-50 border border-neutral-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary resize-none"
                  />
                </div>

                <div className="pt-2 flex items-center justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => setIsBookingModalOpen(false)}
                    className="px-4 py-2 border border-neutral-200 text-neutral-600 rounded-xl text-xs font-semibold hover:bg-neutral-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={bookingSubmitting}
                    className="px-5 py-2.5 bg-primary hover:bg-primary-dark text-white rounded-xl text-xs font-bold transition shadow-sm flex items-center gap-1.5"
                  >
                    {bookingSubmitting ? 'Submitting...' : 'Confirm & Request Booking'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
