import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import {
  Users,
  Search,
  SlidersHorizontal,
  MapPin,
  GraduationCap,
  Calendar,
  Sparkles,
  MessageCircle,
  Tag,
  Check,
  RotateCcw,
  UserCheck,
  ArrowRight,
} from 'lucide-react'
import { flatmateService } from '../../services/flatmateService'
import { messagingService } from '../../services/messagingService'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../constants/routes'
import { Button } from '../../components/ui/Button'
import { Badge } from '../../components/ui/Badge'
import { Modal } from '../../components/ui/Modal'

const POPULAR_TAGS = [
  'early_riser',
  'night_owl',
  'vegetarian',
  'non_smoker',
  'studious',
  'pet_friendly',
  'fitness',
  'social',
  'clean_freak',
  'quiet',
]

const formatTag = (tag) => {
  return tag
    .split('_')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
}

export const BrowseFlatmates = () => {
  const { user, isAuthenticated } = useAuthStore()
  const navigate = useNavigate()

  const [profiles, setProfiles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [myProfile, setMyProfile] = useState(null)

  // Filters
  const [city, setCity] = useState('')
  const [university, setUniversity] = useState('')
  const [maxBudget, setMaxBudget] = useState('')
  const [gender, setGender] = useState('ANY')
  const [selectedTags, setSelectedTags] = useState([])

  // Connect Modal
  const [connectTarget, setConnectTarget] = useState(null)
  const [connectMessage, setConnectMessage] = useState('')
  const [connecting, setConnecting] = useState(false)
  const [connectSuccess, setConnectSuccess] = useState(false)

  // Fetch current user's profile to know if they have one
  useEffect(() => {
    if (isAuthenticated && user?.role === 'STUDENT') {
      flatmateService
        .getMyProfile()
        .then((res) => {
          if (res?.data) setMyProfile(res.data)
        })
        .catch(() => {
          setMyProfile(null)
        })
    }
  }, [isAuthenticated, user])

  // Fetch flatmates
  const loadProfiles = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await flatmateService.browseFlatmates({
        city: city || undefined,
        university: university || undefined,
        max_budget: maxBudget ? Number(maxBudget) : undefined,
        gender: gender !== 'ANY' ? gender : undefined,
        tags: selectedTags,
      })
      setProfiles(res.data || [])
    } catch (err) {
      setError(err.message || 'Failed to load flatmate profiles')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadProfiles()
  }, [gender])

  const handleSearchSubmit = (e) => {
    e.preventDefault()
    loadProfiles()
  }

  const toggleTag = (tag) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((t) => t !== tag))
    } else {
      setSelectedTags([...selectedTags, tag])
    }
  }

  const handleResetFilters = () => {
    setCity('')
    setUniversity('')
    setMaxBudget('')
    setGender('ANY')
    setSelectedTags([])
    flatmateService.browseFlatmates().then((res) => setProfiles(res.data || []))
  }

  const handleOpenConnect = (profile) => {
    if (!isAuthenticated) {
      navigate(ROUTES.LOGIN, { state: { from: '/flatmates' } })
      return
    }
    setConnectTarget(profile)
    setConnectMessage(
      `Hi ${profile.user?.full_name || 'there'}! I saw your flatmate profile on NestMatch and noticed we have great compatibility. Would you like to connect and look for a place together?`
    )
    setConnectSuccess(false)
  }

  const handleSendConnect = async () => {
    if (!connectTarget) return
    setConnecting(true)
    try {
      const res = await messagingService.getOrCreateConversation({
        landlord_id: connectTarget.user_id,
        initial_message: connectMessage,
      })
      const convId = res.data?.id
      setConnectSuccess(true)
      setTimeout(() => {
        setConnectTarget(null)
        if (convId) {
          navigate(`${ROUTES.MESSAGES}/${convId}`)
        } else {
          navigate(ROUTES.MESSAGES)
        }
      }, 900)
    } catch (err) {
      alert(err.message || 'Failed to start conversation')
    } finally {
      setConnecting(false)
    }
  }

  return (
    <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Top Banner / Hero */}
      <div className="bg-gradient-to-r from-primary-600 via-primary-500 to-indigo-600 rounded-2xl p-6 sm:p-8 text-white shadow-lg mb-8 relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-xs font-semibold uppercase tracking-wider text-white mb-3">
            <Sparkles size={14} /> Social Roommate Discovery
          </div>
          <h1 className="text-2xl sm:text-3xl font-heading font-bold text-white mb-2">
            Find Compatible Roommates
          </h1>
          <p className="text-primary-100 text-sm sm:text-base leading-relaxed mb-4">
            Match with fellow university students by lifestyle habits, campus proximity, budget, and move-in schedules.
          </p>

          {isAuthenticated && user?.role === 'STUDENT' ? (
            myProfile ? (
              <div className="flex flex-wrap items-center gap-3">
                <span className="text-xs bg-white/20 backdrop-blur px-3 py-1.5 rounded-lg font-medium">
                  ✓ Your Profile Active ({myProfile.preferred_city || 'India'})
                </span>
                <Link
                  to={ROUTES.MY_FLATMATE_PROFILE}
                  className="inline-flex items-center gap-1.5 text-xs font-semibold bg-white text-primary px-3 py-1.5 rounded-lg hover:bg-neutral-100 transition-colors shadow-sm"
                >
                  Edit My Profile <ArrowRight size={13} />
                </Link>
              </div>
            ) : (
              <Link
                to={ROUTES.MY_FLATMATE_PROFILE}
                className="inline-flex items-center gap-2 bg-white text-primary-700 hover:bg-primary-50 font-semibold px-4 py-2 rounded-xl text-sm transition-all shadow-md hover:shadow-lg"
              >
                <UserCheck size={16} /> Create My Roommate Profile
              </Link>
            )
          ) : !isAuthenticated ? (
            <Link
              to={ROUTES.REGISTER}
              className="inline-flex items-center gap-2 bg-white text-primary-700 hover:bg-primary-50 font-semibold px-4 py-2 rounded-xl text-sm transition-all shadow-md"
            >
              Sign up to Match & Connect
            </Link>
          ) : null}
        </div>
      </div>

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Left Filter Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl border border-neutral-200 p-5 shadow-sm sticky top-20">
            <div className="flex items-center justify-between pb-4 border-b border-neutral-100 mb-4">
              <h2 className="font-heading font-semibold text-neutral-900 flex items-center gap-2 text-base">
                <SlidersHorizontal size={16} className="text-primary" /> Filter Profiles
              </h2>
              <button
                type="button"
                onClick={handleResetFilters}
                className="text-xs text-neutral-500 hover:text-primary flex items-center gap-1 font-medium transition-colors"
              >
                <RotateCcw size={12} /> Reset
              </button>
            </div>

            <form onSubmit={handleSearchSubmit} className="space-y-4">
              {/* City */}
              <div>
                <label className="block text-xs font-semibold text-neutral-700 mb-1">
                  City
                </label>
                <div className="relative">
                  <MapPin size={15} className="absolute left-3 top-3 text-neutral-400" />
                  <input
                    type="text"
                    placeholder="e.g. Pune, Bangalore"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="w-full pl-9 pr-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                  />
                </div>
              </div>

              {/* University */}
              <div>
                <label className="block text-xs font-semibold text-neutral-700 mb-1">
                  University / College
                </label>
                <div className="relative">
                  <GraduationCap size={15} className="absolute left-3 top-3 text-neutral-400" />
                  <input
                    type="text"
                    placeholder="e.g. Pune University"
                    value={university}
                    onChange={(e) => setUniversity(e.target.value)}
                    className="w-full pl-9 pr-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                  />
                </div>
              </div>

              {/* Max Budget */}
              <div>
                <label className="block text-xs font-semibold text-neutral-700 mb-1">
                  Max Monthly Budget (₹)
                </label>
                <input
                  type="number"
                  placeholder="e.g. 12000"
                  value={maxBudget}
                  onChange={(e) => setMaxBudget(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                />
              </div>

              {/* Gender Preference */}
              <div>
                <label className="block text-xs font-semibold text-neutral-700 mb-1">
                  Gender
                </label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none bg-white"
                >
                  <option value="ANY">Any Gender</option>
                  <option value="FEMALE">Female Only</option>
                  <option value="MALE">Male Only</option>
                </select>
              </div>

              {/* Lifestyle Tags */}
              <div>
                <label className="block text-xs font-semibold text-neutral-700 mb-2">
                  Lifestyle Habits
                </label>
                <div className="flex flex-wrap gap-1.5">
                  {POPULAR_TAGS.map((tag) => {
                    const active = selectedTags.includes(tag)
                    return (
                      <button
                        key={tag}
                        type="button"
                        onClick={() => toggleTag(tag)}
                        className={`text-xs px-2.5 py-1 rounded-full font-medium transition-all ${
                          active
                            ? 'bg-primary text-white shadow-xs'
                            : 'bg-neutral-100 text-neutral-600 hover:bg-neutral-200'
                        }`}
                      >
                        {formatTag(tag)}
                      </button>
                    )
                  })}
                </div>
              </div>

              <Button type="submit" variant="primary" className="w-full text-sm mt-2">
                Apply Filters
              </Button>
            </form>
          </div>
        </div>

        {/* Right Flatmates Grid */}
        <div className="lg:col-span-3">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-heading font-semibold text-neutral-900">
              Compatible Roommates {profiles.length > 0 && `(${profiles.length})`}
            </h2>
            {selectedTags.length > 0 && (
              <span className="text-xs text-primary font-medium">
                Filtering by {selectedTags.length} habit{selectedTags.length > 1 ? 's' : ''}
              </span>
            )}
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 bg-white rounded-xl border border-neutral-200">
              <div className="w-8 h-8 border-3 border-primary border-t-transparent rounded-full animate-spin mb-3"></div>
              <p className="text-neutral-500 text-sm">Matching compatible students...</p>
            </div>
          ) : error ? (
            <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm text-center">
              {error}
            </div>
          ) : profiles.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 bg-white rounded-xl border border-neutral-200 text-center px-4">
              <div className="w-14 h-14 rounded-full bg-primary-50 text-primary flex items-center justify-center mb-3">
                <Users size={28} />
              </div>
              <h3 className="text-base font-semibold text-neutral-900 mb-1">
                No flatmate profiles found
              </h3>
              <p className="text-sm text-neutral-500 max-w-md mb-4">
                Try loosening your filters or clearing tags to discover more students looking for roommates.
              </p>
              <Button variant="outline" onClick={handleResetFilters}>
                Clear All Filters
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {profiles.map((p) => {
                const userName = p.user?.full_name || 'Student'
                const initials = userName
                  .split(' ')
                  .map((n) => n[0])
                  .join('')
                  .toUpperCase()
                  .slice(0, 2)

                const score = p.compatibility_score || 75
                const scoreColor =
                  score >= 80
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    : score >= 60
                    ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                    : 'bg-neutral-50 text-neutral-600 border-neutral-200'

                return (
                  <div
                    key={p.id}
                    className="bg-white rounded-xl border border-neutral-200 hover:border-primary/40 hover:shadow-md transition-all p-5 flex flex-col justify-between"
                  >
                    <div>
                      {/* Header with Avatar & Compatibility Badge */}
                      <div className="flex items-start justify-between gap-3 mb-3">
                        <div className="flex items-center gap-3">
                          {p.user?.avatar_url ? (
                            <img
                              src={p.user.avatar_url}
                              alt={userName}
                              className="w-12 h-12 rounded-full object-cover border border-neutral-200"
                            />
                          ) : (
                            <div className="w-12 h-12 rounded-full bg-primary-100 text-primary-700 font-bold flex items-center justify-center text-sm">
                              {initials}
                            </div>
                          )}
                          <div>
                            <h3 className="font-heading font-semibold text-neutral-900 text-base">
                              {userName}
                            </h3>
                            <div className="flex items-center gap-2 text-xs text-neutral-500">
                              {p.gender && <span className="capitalize">{p.gender.toLowerCase()}</span>}
                              {p.preferred_city && (
                                <>
                                  <span>•</span>
                                  <span className="flex items-center gap-0.5">
                                    <MapPin size={11} /> {p.preferred_city}
                                  </span>
                                </>
                              )}
                            </div>
                          </div>
                        </div>

                        {/* Compatibility Score */}
                        <div
                          className={`px-2.5 py-1 rounded-full border text-xs font-semibold flex items-center gap-1 ${scoreColor}`}
                          title="Estimated lifestyle & budget compatibility"
                        >
                          <Sparkles size={12} /> {score}% Match
                        </div>
                      </div>

                      {/* University & Locality */}
                      {p.preferred_university && (
                        <p className="text-xs text-neutral-600 flex items-center gap-1.5 mb-2 font-medium">
                          <GraduationCap size={13} className="text-neutral-400" />
                          {p.preferred_university}
                          {p.preferred_locality && ` (${p.preferred_locality})`}
                        </p>
                      )}

                      {/* Budget & Move In */}
                      <div className="grid grid-cols-2 gap-2 my-3 p-2.5 rounded-lg bg-neutral-50 border border-neutral-100 text-xs">
                        <div>
                          <span className="text-neutral-400 block font-normal">Monthly Budget</span>
                          <span className="font-semibold text-neutral-800">
                            {p.budget_min ? `₹${Number(p.budget_min).toLocaleString()} - ` : 'Up to '}
                            ₹{Number(p.budget_max).toLocaleString()}
                          </span>
                        </div>
                        <div>
                          <span className="text-neutral-400 block font-normal">Move-in Date</span>
                          <span className="font-semibold text-neutral-800 flex items-center gap-1">
                            <Calendar size={12} className="text-neutral-400" />
                            {p.move_in_date ? p.move_in_date : 'Flexible'}
                          </span>
                        </div>
                      </div>

                      {/* Bio */}
                      {p.bio && (
                        <p className="text-xs text-neutral-600 line-clamp-2 italic mb-3">
                          "{p.bio}"
                        </p>
                      )}

                      {/* Lifestyle Tag Pills */}
                      {p.lifestyle_tags && p.lifestyle_tags.length > 0 && (
                        <div className="flex flex-wrap gap-1 mb-4">
                          {p.lifestyle_tags.map((t) => (
                            <span
                              key={t}
                              className="text-[11px] px-2 py-0.5 bg-neutral-100 text-neutral-700 rounded-md font-medium"
                            >
                              {formatTag(t)}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Connect CTA */}
                    <div className="pt-3 border-t border-neutral-100 mt-2">
                      <Button
                        variant="primary"
                        size="sm"
                        className="w-full flex items-center justify-center gap-1.5"
                        onClick={() => handleOpenConnect(p)}
                      >
                        <MessageCircle size={14} /> Connect with {userName.split(' ')[0]}
                      </Button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>

      {/* Connect Message Modal */}
      {connectTarget && (
        <Modal
          isOpen={!!connectTarget}
          onClose={() => setConnectTarget(null)}
          title={`Connect with ${connectTarget.user?.full_name || 'Student'}`}
        >
          {connectSuccess ? (
            <div className="py-6 text-center">
              <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3">
                <Check size={24} />
              </div>
              <h3 className="font-semibold text-neutral-900 mb-1">Message Sent!</h3>
              <p className="text-xs text-neutral-500">Redirecting to your conversation...</p>
            </div>
          ) : (
            <div className="space-y-4">
              <p className="text-xs text-neutral-600">
                Start a direct conversation thread with {connectTarget.user?.full_name} to discuss room sharing, location preferences, and visit listings together.
              </p>

              <div>
                <label className="block text-xs font-semibold text-neutral-700 mb-1">
                  Introductory Message
                </label>
                <textarea
                  rows={4}
                  value={connectMessage}
                  onChange={(e) => setConnectMessage(e.target.value)}
                  className="w-full p-3 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                  placeholder="Introduce yourself..."
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <Button
                  variant="outline"
                  onClick={() => setConnectTarget(null)}
                  disabled={connecting}
                >
                  Cancel
                </Button>
                <Button
                  variant="primary"
                  onClick={handleSendConnect}
                  disabled={connecting || !connectMessage.trim()}
                >
                  {connecting ? 'Connecting...' : 'Send Message'}
                </Button>
              </div>
            </div>
          )}
        </Modal>
      )}
    </div>
  )
}

export default BrowseFlatmates
