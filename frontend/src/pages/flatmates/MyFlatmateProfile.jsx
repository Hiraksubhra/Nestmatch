import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import {
  User,
  Sliders,
  MapPin,
  GraduationCap,
  Calendar,
  Sparkles,
  Tag,
  Check,
  AlertCircle,
  ArrowLeft,
  Trash2,
} from 'lucide-react'
import { flatmateService } from '../../services/flatmateService'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../constants/routes'
import { Button } from '../../components/ui/Button'

const ALL_LIFESTYLE_TAGS = [
  { id: 'early_riser', label: 'Early Riser' },
  { id: 'night_owl', label: 'Night Owl' },
  { id: 'vegetarian', label: 'Vegetarian' },
  { id: 'vegan', label: 'Vegan' },
  { id: 'non_smoker', label: 'Non-Smoker' },
  { id: 'studious', label: 'Studious / Quiet' },
  { id: 'social', label: 'Social & Outgoing' },
  { id: 'fitness', label: 'Fitness Enthusiast' },
  { id: 'pet_friendly', label: 'Pet Friendly' },
  { id: 'clean_freak', label: 'Very Clean / Tidy' },
  { id: 'music_lover', label: 'Music Lover' },
  { id: 'foodie', label: 'Foodie / Likes Cooking' },
]

export const MyFlatmateProfile = () => {
  const { user } = useAuthStore()
  const navigate = useNavigate()

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [successMsg, setSuccessMsg] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const [budgetMin, setBudgetMin] = useState('')
  const [budgetMax, setBudgetMax] = useState('')
  const [preferredCity, setPreferredCity] = useState('')
  const [preferredUniversity, setPreferredUniversity] = useState('')
  const [preferredLocality, setPreferredLocality] = useState('')
  const [moveInDate, setMoveInDate] = useState('')
  const [moveInFlexibility, setMoveInFlexibility] = useState(7)
  const [gender, setGender] = useState('ANY')
  const [bio, setBio] = useState('')
  const [lifestyleTags, setLifestyleTags] = useState([])
  const [isActive, setIsActive] = useState(true)

  useEffect(() => {
    flatmateService
      .getMyProfile()
      .then((res) => {
        if (res?.data) {
          const p = res.data
          setBudgetMin(p.budget_min ? String(p.budget_min) : '')
          setBudgetMax(String(p.budget_max || ''))
          setPreferredCity(p.preferred_city || '')
          setPreferredUniversity(p.preferred_university || '')
          setPreferredLocality(p.preferred_locality || '')
          setMoveInDate(p.move_in_date || '')
          setMoveInFlexibility(p.move_in_flexibility || 7)
          setGender(p.gender || 'ANY')
          setBio(p.bio || '')
          setLifestyleTags(p.lifestyle_tags || [])
          setIsActive(p.is_active !== false)
        }
      })
      .catch(() => {
        // No existing profile, defaults remain
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  const toggleTag = (tagId) => {
    if (lifestyleTags.includes(tagId)) {
      setLifestyleTags(lifestyleTags.filter((t) => t !== tagId))
    } else {
      setLifestyleTags([...lifestyleTags, tagId])
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrorMsg('')
    setSuccessMsg('')

    if (!budgetMax || Number(budgetMax) <= 0) {
      setErrorMsg('Please enter a valid maximum monthly budget.')
      return
    }

    setSaving(true)
    try {
      await flatmateService.saveMyProfile({
        budget_min: budgetMin ? Number(budgetMin) : undefined,
        budget_max: Number(budgetMax),
        preferred_city: preferredCity || undefined,
        preferred_university: preferredUniversity || undefined,
        preferred_locality: preferredLocality || undefined,
        move_in_date: moveInDate || undefined,
        move_in_flexibility: Number(moveInFlexibility),
        gender: gender !== 'ANY' ? gender : undefined,
        bio: bio || undefined,
        lifestyle_tags: lifestyleTags,
      })
      setSuccessMsg('Your flatmate profile has been updated successfully!')
      setTimeout(() => setSuccessMsg(''), 4000)
    } catch (err) {
      setErrorMsg(err.message || 'Failed to save profile')
    } finally {
      setSaving(false)
    }
  }

  const handleDeactivate = async () => {
    if (!window.confirm('Are you sure you want to deactivate your flatmate profile? Other students will no longer see you in roommate searches.')) {
      return
    }
    setSaving(true)
    try {
      await flatmateService.deactivateMyProfile()
      setIsActive(false)
      setSuccessMsg('Profile deactivated.')
    } catch (err) {
      setErrorMsg(err.message || 'Failed to deactivate profile')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 flex items-center justify-center">
        <div className="w-8 h-8 border-3 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back button */}
      <Link
        to={ROUTES.FLATMATES}
        className="inline-flex items-center gap-1.5 text-xs text-neutral-500 hover:text-neutral-800 font-medium mb-6 transition-colors"
      >
        <ArrowLeft size={14} /> Back to Browse Roommates
      </Link>

      <div className="bg-white rounded-2xl border border-neutral-200 shadow-sm overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-700 via-primary to-indigo-800 px-6 sm:px-8 py-6 text-white relative overflow-hidden border-b border-blue-400/30">
          <div className="absolute -right-8 -top-8 w-48 h-48 bg-sky-400/25 rounded-full blur-2xl pointer-events-none" />
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-1">
              <Sparkles size={20} className="text-sky-300" />
              <h1 className="text-xl sm:text-2xl font-heading font-bold text-white tracking-tight">
                My Roommate & Flatmate Profile
              </h1>
            </div>
            <p className="text-sky-100 text-xs sm:text-sm">
              Set your budget, location preferences, and lifestyle habits so compatible students can discover and connect with you.
            </p>
          </div>
        </div>


        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 sm:p-8 space-y-6">
          {errorMsg && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center gap-2">
              <AlertCircle size={16} />
              {errorMsg}
            </div>
          )}
          {successMsg && (
            <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-700 text-sm flex items-center gap-2">
              <Check size={16} />
              {successMsg}
            </div>
          )}

          {/* Budget Range */}
          <div>
            <h2 className="text-sm font-heading font-semibold text-neutral-900 mb-3 flex items-center gap-1.5">
              <span>1. Monthly Budget Range (₹)</span>
              <span className="text-red-500">*</span>
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs text-neutral-600 font-medium mb-1">
                  Minimum Budget (Optional)
                </label>
                <input
                  type="number"
                  placeholder="e.g. 6000"
                  value={budgetMin}
                  onChange={(e) => setBudgetMin(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                />
              </div>
              <div>
                <label className="block text-xs text-neutral-600 font-medium mb-1">
                  Maximum Budget (Required)
                </label>
                <input
                  type="number"
                  placeholder="e.g. 12000"
                  required
                  value={budgetMax}
                  onChange={(e) => setBudgetMax(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                />
              </div>
            </div>
          </div>

          {/* Location & University Preferences */}
          <div className="pt-4 border-t border-neutral-100">
            <h2 className="text-sm font-heading font-semibold text-neutral-900 mb-3">
              2. Target Location & Campus
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs text-neutral-600 font-medium mb-1">City</label>
                <div className="relative">
                  <MapPin size={14} className="absolute left-3 top-3 text-neutral-400" />
                  <input
                    type="text"
                    placeholder="e.g. Pune"
                    value={preferredCity}
                    onChange={(e) => setPreferredCity(e.target.value)}
                    className="w-full pl-9 pr-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs text-neutral-600 font-medium mb-1">University / College</label>
                <div className="relative">
                  <GraduationCap size={14} className="absolute left-3 top-3 text-neutral-400" />
                  <input
                    type="text"
                    placeholder="e.g. Pune University"
                    value={preferredUniversity}
                    onChange={(e) => setPreferredUniversity(e.target.value)}
                    className="w-full pl-9 pr-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs text-neutral-600 font-medium mb-1">Preferred Locality</label>
                <input
                  type="text"
                  placeholder="e.g. Kothrud, Viman Nagar"
                  value={preferredLocality}
                  onChange={(e) => setPreferredLocality(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                />
              </div>
            </div>
          </div>

          {/* Timeline & Gender */}
          <div className="pt-4 border-t border-neutral-100">
            <h2 className="text-sm font-heading font-semibold text-neutral-900 mb-3">
              3. Move-in Timeline & Demographics
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs text-neutral-600 font-medium mb-1">Target Move-in Date</label>
                <div className="relative">
                  <Calendar size={14} className="absolute left-3 top-3 text-neutral-400" />
                  <input
                    type="date"
                    value={moveInDate}
                    onChange={(e) => setMoveInDate(e.target.value)}
                    className="w-full pl-9 pr-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs text-neutral-600 font-medium mb-1">
                  Flexibility (± {moveInFlexibility} days)
                </label>
                <input
                  type="range"
                  min="0"
                  max="30"
                  value={moveInFlexibility}
                  onChange={(e) => setMoveInFlexibility(Number(e.target.value))}
                  className="w-full accent-primary mt-2"
                />
              </div>
              <div>
                <label className="block text-xs text-neutral-600 font-medium mb-1">My Gender</label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none bg-white"
                >
                  <option value="ANY">Prefer not to say</option>
                  <option value="FEMALE">Female</option>
                  <option value="MALE">Male</option>
                  <option value="NON_BINARY">Non-Binary</option>
                </select>
              </div>
            </div>
          </div>

          {/* Lifestyle Habits Selection */}
          <div className="pt-4 border-t border-neutral-100">
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-sm font-heading font-semibold text-neutral-900">
                4. Lifestyle & Habit Tags
              </h2>
              <span className="text-xs text-neutral-400">
                {lifestyleTags.length} selected
              </span>
            </div>
            <p className="text-xs text-neutral-500 mb-3">
              These tags power our compatibility score algorithm to match you with compatible peers.
            </p>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {ALL_LIFESTYLE_TAGS.map((tag) => {
                const active = lifestyleTags.includes(tag.id)
                return (
                  <button
                    key={tag.id}
                    type="button"
                    onClick={() => toggleTag(tag.id)}
                    className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium border text-left transition-all ${
                      active
                        ? 'bg-primary-50 border-primary text-primary-800 shadow-xs'
                        : 'bg-neutral-50 border-neutral-200 text-neutral-700 hover:bg-neutral-100'
                    }`}
                  >
                    <span>{tag.label}</span>
                    {active && <Check size={14} className="text-primary shrink-0 ml-1" />}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Bio */}
          <div className="pt-4 border-t border-neutral-100">
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs text-neutral-700 font-semibold">
                5. About Me & Roommate Preferences
              </label>
              <span className={`text-[11px] ${bio.length > 260 ? 'text-amber-600 font-bold' : 'text-neutral-400'}`}>
                {bio.length} / 280
              </span>
            </div>
            <textarea
              rows={3}
              maxLength={280}
              placeholder="Tell potential roommates about your course, schedule, cleanliness habits, and what you're looking for in a flatmate..."
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              className="w-full p-3 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
            />
          </div>

          {/* Form Actions */}
          <div className="pt-6 border-t border-neutral-100 flex flex-col sm:flex-row items-center justify-between gap-4">
            {isActive ? (
              <button
                type="button"
                onClick={handleDeactivate}
                className="text-xs text-red-600 hover:text-red-700 font-medium flex items-center gap-1.5 transition-colors"
              >
                <Trash2 size={13} /> Deactivate Profile
              </button>
            ) : (
              <span className="text-xs text-neutral-400 italic">Profile currently inactive</span>
            )}

            <div className="flex items-center gap-3 w-full sm:w-auto">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate(ROUTES.FLATMATES)}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="primary"
                disabled={saving}
                className="w-full sm:w-auto"
              >
                {saving ? 'Saving Profile...' : 'Save Flatmate Profile'}
              </Button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}

export default MyFlatmateProfile
