import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Calendar,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  MessageSquare,
  Building,
  Phone,
  Mail,
  ShieldCheck,
  ChevronRight,
  MapPin
} from 'lucide-react'
import { bookingService } from '../../services/bookingService'
import { messagingService } from '../../services/messagingService'
import { formatCurrency, getImageUrl } from '../../lib/utils'

export const StudentBookings = () => {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('ALL')
  const [actionLoading, setActionLoading] = useState(null)
  const [message, setMessage] = useState(null)

  useEffect(() => {
    loadBookings()
  }, [])

  const loadBookings = async () => {
    try {
      setLoading(true)
      const data = await bookingService.getBookings()
      setBookings(data)
    } catch (err) {
      console.error('Failed to load bookings:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (bookingId) => {
    if (!window.confirm('Are you sure you want to cancel this booking request?')) return

    try {
      setActionLoading(bookingId)
      await bookingService.cancelBooking(bookingId)
      setMessage({ type: 'success', text: 'Booking request cancelled successfully.' })
      await loadBookings()
    } catch (err) {
      setMessage({ type: 'error', text: err.message || 'Failed to cancel booking request.' })
    } finally {
      setActionLoading(null)
    }
  }

  const filteredBookings = bookings.filter((b) => {
    if (filter === 'ALL') return true
    if (filter === 'PENDING') return b.status === 'PENDING'
    if (filter === 'ACCEPTED') return b.status === 'ACCEPTED'
    if (filter === 'ARCHIVED') return b.status === 'DECLINED' || b.status === 'CANCELLED'
    return true
  })

  const getStatusBadge = (status) => {
    switch (status) {
      case 'PENDING':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-50 text-amber-700 border border-amber-200 rounded-full text-xs font-semibold">
            <Clock size={13} className="animate-spin text-amber-600" />
            Pending Landlord Review
          </span>
        )
      case 'ACCEPTED':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full text-xs font-semibold">
            <CheckCircle size={13} className="text-emerald-600" />
            Booking Confirmed
          </span>
        )
      case 'DECLINED':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-rose-50 text-rose-700 border border-rose-200 rounded-full text-xs font-semibold">
            <XCircle size={13} className="text-rose-600" />
            Declined by Landlord
          </span>
        )
      case 'CANCELLED':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-neutral-100 text-neutral-600 border border-neutral-200 rounded-full text-xs font-semibold">
            Cancelled
          </span>
        )
      default:
        return null
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl sm:text-3xl font-heading font-bold text-neutral-900">
            My Booking Requests
          </h1>
          <p className="text-sm text-neutral-600 mt-1">
            Track and manage your accommodation requests, move-in schedules, and confirmed landlord contacts.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 bg-neutral-100 p-1 rounded-xl">
          {['ALL', 'PENDING', 'ACCEPTED', 'ARCHIVED'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition ${
                filter === f ? 'bg-white text-primary shadow-sm' : 'text-neutral-600 hover:text-neutral-900'
              }`}
            >
              {f === 'ALL'
                ? 'All'
                : f === 'PENDING'
                ? 'Pending'
                : f === 'ACCEPTED'
                ? 'Confirmed'
                : 'Declined/Past'}
            </button>
          ))}
        </div>
      </div>

      {message && (
        <div
          className={`p-4 rounded-xl mb-6 text-sm flex items-center justify-between ${
            message.type === 'success'
              ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
              : 'bg-rose-50 text-rose-800 border border-rose-200'
          }`}
        >
          <span>{message.text}</span>
          <button onClick={() => setMessage(null)} className="text-xs font-bold hover:underline">
            Dismiss
          </button>
        </div>
      )}

      {/* Bookings List */}
      {loading ? (
        <div className="p-12 text-center text-neutral-400">Loading your bookings...</div>
      ) : filteredBookings.length === 0 ? (
        <div className="bg-white border border-neutral-200 rounded-2xl p-12 text-center space-y-4 max-w-md mx-auto">
          <Calendar size={48} className="mx-auto text-neutral-300" />
          <h3 className="text-lg font-semibold text-neutral-800">No bookings in this category</h3>
          <p className="text-xs text-neutral-500">
            Browse verified listings and click "Request to Book" to reserve your student home.
          </p>
          <Link
            to="/search"
            className="inline-block px-5 py-2.5 bg-primary text-white text-sm font-semibold rounded-xl hover:bg-primary-dark transition shadow-sm"
          >
            Find Accommodations
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {filteredBookings.map((b) => {
            const photoUrl =
              b.listing?.photos && b.listing.photos.length > 0
                ? getImageUrl(b.listing.photos[0].url)
                : '/placeholder.jpg'

            return (
              <div
                key={b.id}
                className="bg-white border border-neutral-200 rounded-2xl p-6 shadow-sm transition hover:shadow-md"
              >
                <div className="flex flex-col lg:flex-row gap-6 items-start">
                  {/* Listing Thumbnail */}
                  <img
                    src={photoUrl}
                    alt={b.listing?.title || 'Listing'}
                    className="w-full lg:w-48 h-36 object-cover rounded-xl shrink-0 border border-neutral-100"
                  />

                  {/* Booking Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                      <h2 className="text-lg font-bold font-heading text-neutral-900 truncate">
                        {b.listing?.title || 'Property'}
                      </h2>
                      {getStatusBadge(b.status)}
                    </div>

                    <p className="text-xs text-neutral-500 flex items-center gap-1 mb-3">
                      <MapPin size={13} className="text-neutral-400" />
                      {b.listing?.locality}, {b.listing?.city}
                    </p>

                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 p-3 bg-neutral-50 rounded-xl text-xs mb-4">
                      <div>
                        <span className="text-neutral-400 block">Move-in Date</span>
                        <span className="font-semibold text-neutral-900">
                          {new Date(b.move_in_date).toLocaleDateString([], {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                          })}
                        </span>
                      </div>
                      <div>
                        <span className="text-neutral-400 block">Duration</span>
                        <span className="font-semibold text-neutral-900">
                          {b.duration_months} Month{b.duration_months > 1 ? 's' : ''}
                        </span>
                      </div>
                      <div>
                        <span className="text-neutral-400 block">Monthly Rent</span>
                        <span className="font-bold text-primary">
                          {formatCurrency(b.listing?.rent_amount || 0)}
                        </span>
                      </div>
                    </div>

                    {b.message && (
                      <p className="text-xs text-neutral-600 italic mb-4 bg-neutral-50/50 p-2.5 rounded-lg border border-neutral-100">
                        "{b.message}"
                      </p>
                    )}

                    {/* Unlocked Contact Details for ACCEPTED bookings */}
                    {b.status === 'ACCEPTED' && b.landlord_contact && (
                      <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl mb-4 space-y-2">
                        <div className="flex items-center gap-1.5 text-emerald-800 font-bold text-xs uppercase tracking-wide">
                          <ShieldCheck size={16} className="text-emerald-600" />
                          <span>Landlord Contact Revealed</span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-emerald-950">
                          <div className="flex items-center gap-2">
                            <Phone size={14} className="text-emerald-600" />
                            <span>{b.landlord_contact.phone}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Mail size={14} className="text-emerald-600" />
                            <span>{b.landlord_contact.email}</span>
                          </div>
                        </div>
                        <p className="text-[11px] text-emerald-700 pt-1">
                          You can now contact the landlord directly to schedule key pickup and move-in inspection.
                        </p>
                      </div>
                    )}

                    {/* Action buttons */}
                    <div className="flex flex-wrap items-center gap-3 pt-2">
                      <Link
                        to={`/messages`}
                        className="inline-flex items-center gap-1.5 px-4 py-2 bg-primary/10 hover:bg-primary/20 text-primary text-xs font-semibold rounded-xl transition"
                      >
                        <MessageSquare size={14} />
                        Chat with Landlord
                      </Link>

                      <Link
                        to={`/listings/${b.listing_id}`}
                        className="inline-flex items-center gap-1 px-4 py-2 border border-neutral-200 hover:bg-neutral-50 text-neutral-700 text-xs font-medium rounded-xl transition"
                      >
                        View Listing
                        <ChevronRight size={13} />
                      </Link>

                      {b.status === 'PENDING' && (
                        <button
                          onClick={() => handleCancel(b.id)}
                          disabled={actionLoading === b.id}
                          className="px-4 py-2 text-rose-600 hover:bg-rose-50 text-xs font-semibold rounded-xl transition border border-rose-200 ml-auto"
                        >
                          {actionLoading === b.id ? 'Cancelling...' : 'Cancel Request'}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default StudentBookings
