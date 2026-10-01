import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Calendar,
  CheckCircle,
  XCircle,
  Clock,
  User,
  Phone,
  Mail,
  Building,
  MessageSquare,
  ShieldCheck,
  AlertCircle
} from 'lucide-react'
import { bookingService } from '../../services/bookingService'
import { formatCurrency, getImageUrl } from '../../lib/utils'

export const LandlordBookings = () => {
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
      console.error('Failed to load landlord bookings:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAccept = async (id) => {
    if (!window.confirm('Accept this student booking request? Contact details will be shared with the student.')) return

    try {
      setActionLoading(id)
      await bookingService.acceptBooking(id)
      setMessage({ type: 'success', text: 'Booking request accepted! The student has been notified.' })
      await loadBookings()
    } catch (err) {
      setMessage({ type: 'error', text: err.message || 'Failed to accept booking.' })
    } finally {
      setActionLoading(null)
    }
  }

  const handleDecline = async (id) => {
    if (!window.confirm('Are you sure you want to decline this booking request?')) return

    try {
      setActionLoading(id)
      await bookingService.declineBooking(id)
      setMessage({ type: 'success', text: 'Booking request declined.' })
      await loadBookings()
    } catch (err) {
      setMessage({ type: 'error', text: err.message || 'Failed to decline booking.' })
    } finally {
      setActionLoading(null)
    }
  }

  const filtered = bookings.filter((b) => {
    if (filter === 'ALL') return true
    if (filter === 'PENDING') return b.status === 'PENDING'
    if (filter === 'ACCEPTED') return b.status === 'ACCEPTED'
    if (filter === 'DECLINED') return b.status === 'DECLINED' || b.status === 'CANCELLED'
    return true
  })

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl sm:text-3xl font-heading font-bold text-neutral-900">
            Booking Requests
          </h1>
          <p className="text-sm text-neutral-600 mt-1">
            Review and respond to student accommodation requests for your listed properties.
          </p>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-1.5 bg-neutral-100 p-1 rounded-xl">
          {['ALL', 'PENDING', 'ACCEPTED', 'DECLINED'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition ${
                filter === f ? 'bg-white text-primary shadow-sm' : 'text-neutral-600 hover:text-neutral-900'
              }`}
            >
              {f === 'ALL' ? 'All' : f === 'PENDING' ? 'Pending' : f === 'ACCEPTED' ? 'Accepted' : 'Declined/Past'}
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

      {loading ? (
        <div className="p-12 text-center text-neutral-400">Loading booking requests...</div>
      ) : filtered.length === 0 ? (
        <div className="bg-white border border-neutral-200 rounded-2xl p-12 text-center space-y-4 max-w-md mx-auto">
          <Calendar size={48} className="mx-auto text-neutral-300" />
          <h3 className="text-lg font-semibold text-neutral-800">No requests found</h3>
          <p className="text-xs text-neutral-500">
            Booking requests from interested students will appear here for your review and approval.
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {filtered.map((b) => (
            <div
              key={b.id}
              className="bg-white border border-neutral-200 rounded-2xl p-6 shadow-sm transition hover:shadow-md"
            >
              <div className="flex flex-col lg:flex-row items-start justify-between gap-6">
                <div className="flex-1">
                  {/* Top Bar: Property & Status */}
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <div className="flex items-center gap-2">
                      <Building size={16} className="text-primary" />
                      <Link
                        to={`/listings/${b.listing_id}`}
                        className="font-bold text-neutral-900 hover:text-primary transition"
                      >
                        {b.listing?.title || 'Listing'}
                      </Link>
                    </div>

                    {b.status === 'PENDING' && (
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-50 text-amber-700 border border-amber-200 rounded-full text-xs font-semibold">
                        <Clock size={13} className="text-amber-600" />
                        Awaiting Your Decision
                      </span>
                    )}
                    {b.status === 'ACCEPTED' && (
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full text-xs font-semibold">
                        <CheckCircle size={13} className="text-emerald-600" />
                        Accepted & Confirmed
                      </span>
                    )}
                    {b.status === 'DECLINED' && (
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-rose-50 text-rose-700 border border-rose-200 rounded-full text-xs font-semibold">
                        <XCircle size={13} className="text-rose-600" />
                        Declined
                      </span>
                    )}
                    {b.status === 'CANCELLED' && (
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-neutral-100 text-neutral-600 border border-neutral-200 rounded-full text-xs font-semibold">
                        Cancelled by Student
                      </span>
                    )}
                  </div>

                  {/* Student Snapshot */}
                  <div className="flex items-center gap-3 p-3 bg-neutral-50 rounded-xl mb-4">
                    <div className="w-10 h-10 rounded-full bg-primary/10 text-primary font-bold flex items-center justify-center shrink-0">
                      {b.student?.full_name?.charAt(0) || 'S'}
                    </div>
                    <div>
                      <span className="text-xs text-neutral-400 block">Prospective Student Tenant</span>
                      <span className="font-semibold text-sm text-neutral-900">{b.student?.full_name}</span>
                    </div>
                  </div>

                  {/* Key Metrics */}
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 p-3 border border-neutral-100 rounded-xl text-xs mb-4">
                    <div>
                      <span className="text-neutral-400 block">Requested Move-in</span>
                      <span className="font-semibold text-neutral-900">
                        {new Date(b.move_in_date).toLocaleDateString([], {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                        })}
                      </span>
                    </div>
                    <div>
                      <span className="text-neutral-400 block">Stay Duration</span>
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
                    <p className="text-xs text-neutral-600 italic bg-neutral-50/50 p-2.5 rounded-lg border border-neutral-100 mb-4">
                      "{b.message}"
                    </p>
                  )}

                  {/* Revealed student contacts when ACCEPTED */}
                  {b.status === 'ACCEPTED' && b.student_contact && (
                    <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl mb-4 space-y-2">
                      <div className="flex items-center gap-1.5 text-emerald-800 font-bold text-xs uppercase tracking-wide">
                        <ShieldCheck size={16} className="text-emerald-600" />
                        <span>Student Contact Information</span>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-emerald-950">
                        <div className="flex items-center gap-2">
                          <Phone size={14} className="text-emerald-600" />
                          <span>{b.student_contact.phone}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Mail size={14} className="text-emerald-600" />
                          <span>{b.student_contact.email}</span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex flex-wrap items-center gap-3 pt-2">
                    <Link
                      to="/messages"
                      className="inline-flex items-center gap-1.5 px-4 py-2 bg-primary/10 hover:bg-primary/20 text-primary text-xs font-semibold rounded-xl transition"
                    >
                      <MessageSquare size={14} />
                      Message Student
                    </Link>

                    {b.status === 'PENDING' && (
                      <div className="flex items-center gap-2 ml-auto">
                        <button
                          onClick={() => handleDecline(b.id)}
                          disabled={actionLoading === b.id}
                          className="px-4 py-2 border border-rose-200 hover:bg-rose-50 text-rose-600 text-xs font-semibold rounded-xl transition"
                        >
                          Decline
                        </button>
                        <button
                          onClick={() => handleAccept(b.id)}
                          disabled={actionLoading === b.id}
                          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-xl transition shadow-sm"
                        >
                          {actionLoading === b.id ? 'Accepting...' : 'Accept Request'}
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default LandlordBookings
