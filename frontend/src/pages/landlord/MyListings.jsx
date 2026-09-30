import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  Plus,
  Eye,
  Archive,
  AlertCircle,
  ShieldCheck,
  Clock,
  Building,
  CheckCircle,
  ExternalLink,
} from 'lucide-react'
import { listingService } from '../../services/listingService'
import { getImageUrl } from '../../lib/utils'

export const MyListings = () => {
  const location = useLocation()
  const [listings, setListings] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [actionMessage, setActionMessage] = useState(location.state?.message || null)

  const fetchMyListings = async () => {
    setIsLoading(true)
    try {
      const res = await listingService.getMyListings()
      if (res.success) {
        setListings(res.data || [])
      }
    } catch (err) {
      console.error('Failed to load landlord listings', err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchMyListings()
  }, [])

  const handleArchive = async (id) => {
    if (!window.confirm('Are you sure you want to deactivate and archive this listing?')) return
    try {
      await listingService.archiveListing(id)
      setActionMessage('Listing has been archived successfully.')
      fetchMyListings()
    } catch (err) {
      alert(err.message || 'Failed to archive listing')
    }
  }

  const getStatusBadge = (status, rejectionReason) => {
    switch (status) {
      case 'ACTIVE':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <ShieldCheck size={14} className="text-emerald-600" />
            Active & Verified
          </span>
        )
      case 'PENDING_VERIFICATION':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            <Clock size={14} className="text-amber-600" />
            Under Verification
          </span>
        )
      case 'REJECTED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
            <AlertCircle size={14} className="text-rose-600" />
            Rejected
          </span>
        )
      case 'ARCHIVED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-neutral-100 text-neutral-600 border border-neutral-200">
            Archived
          </span>
        )
      default:
        return (
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-neutral-100 text-neutral-700">
            {status}
          </span>
        )
    }
  }

  return (
    <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-6 border-b border-neutral-200 mb-8">
        <div>
          <h1 className="text-2xl sm:text-3xl font-heading font-bold text-neutral-900">My Properties</h1>
          <p className="text-sm text-neutral-500 mt-1">
            Manage your rental accommodations, view verification status, and track inquiries.
          </p>
        </div>
        <Link
          to="/landlord/create-listing"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary hover:bg-primary-dark text-white rounded-xl text-sm font-semibold transition-colors shadow-sm self-start sm:self-auto"
        >
          <Plus size={18} />
          Post New Property
        </Link>
      </div>

      {actionMessage && (
        <div className="mb-6 p-4 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center gap-2 text-sm text-emerald-800">
          <CheckCircle size={18} className="text-emerald-600 shrink-0" />
          <span>{actionMessage}</span>
        </div>
      )}

      {/* Listings Table / Cards */}
      {isLoading ? (
        <div className="p-12 text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary mx-auto mb-3" />
          <p className="text-sm text-neutral-500">Loading your properties...</p>
        </div>
      ) : listings.length > 0 ? (
        <div className="space-y-4">
          {listings.map((item) => (
            <div
              key={item.id}
              className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-card flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
            >
              <div className="flex items-center gap-4">
                <div className="w-20 h-20 rounded-xl bg-neutral-100 overflow-hidden shrink-0 border border-neutral-200">
                  <img
                    src={getImageUrl(
                      item.photos?.[0]?.url,
                      'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=300&q=80'
                    )}
                    alt={item.title}
                    onError={(e) => {
                      e.currentTarget.onerror = null
                      e.currentTarget.src =
                        'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=300&q=80'
                    }}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-semibold uppercase tracking-wider text-primary">
                      {item.property_type?.replace('_', ' ')}
                    </span>
                    {getStatusBadge(item.status, item.rejection_reason)}
                  </div>
                  <h3 className="font-heading font-semibold text-neutral-900 text-base">
                    {item.title}
                  </h3>
                  <p className="text-xs text-neutral-500 mt-0.5">
                    {item.locality ? `${item.locality}, ` : ''}{item.city} • ₹{Number(item.rent_amount).toLocaleString('en-IN')}/mo
                  </p>
                  {item.rejection_reason && item.status === 'REJECTED' && (
                    <p className="text-xs text-rose-600 mt-1.5 bg-rose-50 p-2 rounded-lg border border-rose-100">
                      Reason: {item.rejection_reason}
                    </p>
                  )}
                </div>
              </div>

              {/* Stats & Actions */}
              <div className="flex items-center gap-4 self-end sm:self-center">
                <div className="text-right text-xs text-neutral-500 hidden md:block">
                  <div className="flex items-center gap-1">
                    <Eye size={14} />
                    <span>{item.views_count} student views</span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Link
                    to={`/listings/${item.id}`}
                    className="p-2.5 text-neutral-600 hover:text-primary rounded-xl border border-neutral-200 hover:bg-neutral-50 text-xs font-medium flex items-center gap-1 transition-colors"
                  >
                    <ExternalLink size={14} />
                    View
                  </Link>

                  {item.status !== 'ARCHIVED' && (
                    <button
                      onClick={() => handleArchive(item.id)}
                      className="p-2.5 text-neutral-500 hover:text-rose-600 rounded-xl border border-neutral-200 hover:bg-rose-50 text-xs font-medium flex items-center gap-1 transition-colors"
                      title="Deactivate / Archive"
                    >
                      <Archive size={14} />
                      Archive
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-neutral-200 p-12 text-center">
          <Building className="mx-auto text-neutral-400 mb-3" size={48} />
          <h3 className="font-heading font-semibold text-lg text-neutral-900 mb-1">
            You haven't posted any accommodations yet
          </h3>
          <p className="text-sm text-neutral-500 max-w-sm mx-auto mb-6">
            Get your PG or student flat discovered by verified students looking for housing today.
          </p>
          <Link
            to="/landlord/create-listing"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary text-white rounded-xl text-sm font-semibold hover:bg-primary-dark transition-colors shadow-sm"
          >
            <Plus size={18} />
            Post First Accommodation
          </Link>
        </div>
      )}
    </div>
  )
}
