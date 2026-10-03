import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Flag,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  X,
  Lock,
  LogIn,
  ShieldCheck,
} from 'lucide-react'
import { Modal } from '../ui/Modal'
import { Button } from '../ui/Button'
import { reportService } from '../../services/reportService'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../constants/routes'

const DEFAULT_REASONS = [
  {
    key: 'INAPPROPRIATE_BEHAVIOUR',
    label: 'Inappropriate Behaviour',
    description: 'Rude, abusive, obscene language or inappropriate conduct.',
  },
  {
    key: 'HARASSMENT',
    label: 'Harassment or Bullying',
    description: 'Threatening communication, intimidation, or persistent unwanted contact.',
  },
  {
    key: 'FRAUD_OR_SCAM',
    label: 'Scam or Fraudulent Activity',
    description: 'Demanding cash deposits outside the platform or fake payment links.',
  },
  {
    key: 'MISLEADING_OR_FAKE',
    label: 'Misleading or Fake Profile / Listing',
    description: 'Impersonation, fabricated credentials, fake listing photos, or false terms.',
  },
  {
    key: 'SPAM',
    label: 'Spam or Advertising',
    description: 'Unsolicited promotional advertisements, commercial spam, or phishing.',
  },
  {
    key: 'OTHER',
    label: 'Other Safety Violation',
    description: 'Any other suspicious activity or concern violating community trust.',
  },
]

export const ReportUserModal = ({
  isOpen,
  onClose,
  reportedUser,
  contextType = 'user', // 'landlord' | 'student' | 'user'
  listingTitle = null,
}) => {
  const { isAuthenticated, user: currentUser } = useAuthStore()

  const [reasons, setReasons] = useState(DEFAULT_REASONS)
  const [selectedReason, setSelectedReason] = useState('INAPPROPRIATE_BEHAVIOUR')
  const [details, setDetails] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [isSuccess, setIsSuccess] = useState(false)

  // Fetch reasons on mount / open
  useEffect(() => {
    if (isOpen) {
      setError(null)
      setIsSuccess(false)
      setDetails('')
      setSelectedReason('INAPPROPRIATE_BEHAVIOUR')

      reportService
        .getReasons()
        .then((res) => {
          if (res?.data && res.data.length > 0) {
            setReasons(res.data)
          }
        })
        .catch(() => {
          // Keep default reasons if API call fails
        })
    }
  }, [isOpen])

  if (!isOpen) return null

  const isSelf = currentUser && reportedUser && currentUser.id === reportedUser.id
  const userName = reportedUser?.full_name || 'User'
  const userRole = reportedUser?.role ? reportedUser.role.toLowerCase() : contextType

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!reportedUser?.id) return

    setIsSubmitting(true)
    setError(null)

    try {
      await reportService.submitReport({
        reported_user_id: reportedUser.id,
        reason: selectedReason,
        details: details.trim() || undefined,
      })
      setIsSuccess(true)
    } catch (err) {
      setError(err?.message || 'Failed to submit report. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      className="max-w-lg"
    >
      {/* Not Logged In View */}
      {!isAuthenticated ? (
        <div className="text-center py-4 space-y-4">
          <div className="w-14 h-14 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center mx-auto border border-amber-200">
            <Lock size={26} />
          </div>
          <div>
            <h3 className="text-lg font-heading font-bold text-neutral-900">
              Sign In to Report
            </h3>
            <p className="text-sm text-neutral-600 mt-1 max-w-sm mx-auto">
              To keep our student housing community safe and protect against malicious flags, you must be signed in to submit a report.
            </p>
          </div>
          <div className="pt-2 flex flex-col gap-2">
            <Link
              to={ROUTES.LOGIN}
              onClick={onClose}
              className="w-full py-2.5 px-4 bg-primary hover:bg-primary-dark text-white rounded-xl text-sm font-semibold transition-colors flex items-center justify-center gap-2"
            >
              <LogIn size={16} /> Sign In
            </Link>
            <Button variant="ghost" onClick={onClose}>
              Cancel
            </Button>
          </div>
        </div>
      ) : isSelf ? (
        <div className="text-center py-6 space-y-3">
          <div className="w-12 h-12 rounded-full bg-neutral-100 text-neutral-600 flex items-center justify-center mx-auto">
            <AlertTriangle size={24} />
          </div>
          <h3 className="text-base font-semibold text-neutral-900">
            Cannot Report Yourself
          </h3>
          <p className="text-sm text-neutral-500">
            You cannot submit a moderation report against your own account.
          </p>
          <Button variant="outline" onClick={onClose} className="mt-4">
            Close
          </Button>
        </div>
      ) : isSuccess ? (
        /* Success Screen */
        <div className="text-center py-6 space-y-4 animate-in fade-in duration-200">
          <div className="w-14 h-14 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto border border-emerald-200">
            <ShieldCheck size={30} />
          </div>
          <div className="space-y-1">
            <h3 className="text-lg font-heading font-bold text-neutral-900">
              Report Submitted
            </h3>
            <p className="text-sm text-neutral-600 max-w-sm mx-auto">
              Thank you for keeping our community safe. Our moderation team has received your report regarding <span className="font-semibold text-neutral-900">{userName}</span> and will review it promptly.
            </p>
          </div>
          <div className="p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-xs text-neutral-500 text-left">
            <p className="font-medium text-neutral-700 mb-1">What happens next?</p>
            <ul className="list-disc list-inside space-y-0.5">
              <li>Our trust & safety team reviews account activity and communications.</li>
              <li>Appropriate moderation actions will be enforced.</li>
              <li>Your report remains 100% confidential.</li>
            </ul>
          </div>
          <Button
            variant="primary"
            onClick={onClose}
            className="w-full mt-2"
          >
            Done
          </Button>
        </div>
      ) : (
        /* Form View */
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Header */}
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-xl bg-red-50 text-red-600 flex items-center justify-center shrink-0 border border-red-200">
              <Flag size={20} />
            </div>
            <div>
              <h3 className="text-lg font-heading font-bold text-neutral-900">
                Report {userRole === 'landlord' ? 'Landlord' : 'Student'}
              </h3>
              <p className="text-xs text-neutral-500 mt-0.5">
                Flagging <span className="font-semibold text-neutral-800">{userName}</span>
                {listingTitle && (
                  <> for listing <span className="italic font-medium text-neutral-700">"{listingTitle}"</span></>
                )}
              </p>
            </div>
          </div>

          {/* Error Banner */}
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-xl flex items-start gap-2.5 text-xs text-red-700">
              <AlertTriangle size={16} className="shrink-0 mt-0.5 text-red-600" />
              <span>{error}</span>
            </div>
          )}

          {/* Reason Selection */}
          <div className="space-y-2">
            <label className="text-xs font-semibold text-neutral-800 uppercase tracking-wider block">
              Reason for Report <span className="text-red-500">*</span>
            </label>
            <div className="space-y-1.5 max-h-56 overflow-y-auto pr-1">
              {reasons.map((r) => {
                const isSelected = selectedReason === r.key
                return (
                  <label
                    key={r.key}
                    className={`flex items-start gap-3 p-3 rounded-xl border cursor-pointer transition-all text-left ${
                      isSelected
                        ? 'border-primary bg-primary/5 ring-1 ring-primary'
                        : 'border-neutral-200 hover:border-neutral-300 hover:bg-neutral-50/50'
                    }`}
                  >
                    <input
                      type="radio"
                      name="reportReason"
                      value={r.key}
                      checked={isSelected}
                      onChange={() => setSelectedReason(r.key)}
                      className="mt-1 text-primary focus:ring-primary h-4 w-4 border-neutral-300"
                    />
                    <div className="text-xs">
                      <span className="font-semibold text-neutral-900 block">
                        {r.label}
                      </span>
                      <span className="text-neutral-500 text-[11px] leading-snug mt-0.5 block">
                        {r.description}
                      </span>
                    </div>
                  </label>
                )
              })}
            </div>
          </div>

          {/* Details Textarea */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label
                htmlFor="report-details"
                className="text-xs font-semibold text-neutral-800 uppercase tracking-wider"
              >
                Additional Details <span className="text-neutral-400 font-normal">(Optional)</span>
              </label>
              <span className="text-[11px] text-neutral-400">
                {details.length}/1000
              </span>
            </div>
            <textarea
              id="report-details"
              rows={3}
              maxLength={1000}
              value={details}
              onChange={(e) => setDetails(e.target.value)}
              placeholder="Provide any additional context or specific messages to help our moderation team investigate..."
              className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-xs text-neutral-900 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary resize-none placeholder:text-neutral-400"
            />
          </div>

          {/* Privacy Note */}
          <div className="flex items-center gap-2 p-2.5 bg-neutral-50 border border-neutral-200 rounded-xl text-[11px] text-neutral-500">
            <ShieldAlert size={15} className="text-neutral-400 shrink-0" />
            <span>
              Reports are 100% confidential. The reported user will not be informed of who submitted this report.
            </span>
          </div>

          {/* Actions */}
          <div className="pt-2 flex items-center justify-end gap-2.5">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              size="sm"
              disabled={isSubmitting || !selectedReason}
              className="bg-red-600 hover:bg-red-700 text-white border-transparent"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Report'}
            </Button>
          </div>
        </form>
      )}
    </Modal>
  )
}
