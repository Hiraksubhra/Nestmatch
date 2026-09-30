import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Building2,
  MapPin,
  CheckCircle2,
  Upload,
  ArrowRight,
  ArrowLeft,
  Loader2,
  ShieldCheck,
  AlertCircle,
} from 'lucide-react'
import { listingService } from '../../services/listingService'

const STEPS = [
  { id: 1, name: 'Basic Details' },
  { id: 2, name: 'Location' },
  { id: 3, name: 'Amenities & Rules' },
  { id: 4, name: 'Photos & Submit' },
]

export const CreateListing = () => {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState(1)
  const [amenitiesList, setAmenitiesList] = useState([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [photoFiles, setPhotoFiles] = useState([])
  const [photoPreviews, setPhotoPreviews] = useState([])

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    property_type: 'PG',
    rent_amount: '',
    deposit_amount: '',
    rent_period: 'MONTHLY',
    city: 'Pune',
    locality: '',
    address_line1: '',
    state: 'Maharashtra',
    pincode: '',
    university_name: '',
    university_distance_km: '',
    gender_preference: 'ANY',
    furnished_status: 'FURNISHED',
    available_from: '',
    min_stay_months: 3,
    max_occupancy: 1,
    amenity_ids: [],
  })

  useEffect(() => {
    listingService.getAmenities()
      .then((res) => {
        if (res.success && res.data) {
          setAmenitiesList(res.data)
        }
      })
      .catch(() => {})
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const toggleAmenity = (id) => {
    setFormData((prev) => {
      const exists = prev.amenity_ids.includes(id)
      return {
        ...prev,
        amenity_ids: exists
          ? prev.amenity_ids.filter((item) => item !== id)
          : [...prev.amenity_ids, id],
      }
    })
  }

  const handlePhotoSelect = (e) => {
    const files = Array.from(e.target.files || [])
    if (files.length === 0) return

    setPhotoFiles((prev) => [...prev, ...files])
    const newPreviews = files.map((file) => URL.createObjectURL(file))
    setPhotoPreviews((prev) => [...prev, ...newPreviews])
  }

  const removePhoto = (index) => {
    setPhotoFiles((prev) => prev.filter((_, i) => i !== index))
    setPhotoPreviews((prev) => prev.filter((_, i) => i !== index))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
      const parsedRent = parseFloat(formData.rent_amount)
      if (isNaN(parsedRent) || parsedRent <= 0) {
        setError('Please enter a valid monthly rent amount greater than 0.')
        setIsSubmitting(false)
        return
      }

      const payload = {
        title: formData.title.trim(),
        description: formData.description?.trim() || null,
        property_type: formData.property_type,
        rent_amount: parsedRent,
        deposit_amount: formData.deposit_amount ? (parseFloat(formData.deposit_amount) || null) : null,
        rent_period: formData.rent_period,
        city: formData.city.trim(),
        locality: formData.locality?.trim() || 'Central',
        address_line1: formData.address_line1?.trim() || null,
        state: formData.state?.trim() || null,
        pincode: formData.pincode?.trim() || null,
        gender_preference: formData.gender_preference,
        furnished_status: formData.furnished_status,
        available_from: formData.available_from?.trim() || null,
        min_stay_months: parseInt(formData.min_stay_months, 10) || 3,
        max_occupancy: parseInt(formData.max_occupancy, 10) || 1,
        amenity_ids: formData.amenity_ids || [],
        university_proximity: formData.university_name?.trim()
          ? [
              {
                name: formData.university_name.trim(),
                distance_km: parseFloat(formData.university_distance_km) || 1.0,
              },
            ]
          : null,
      }

      const res = await listingService.createListing(payload)
      if (res.success && res.data) {
        const listingId = res.data.id

        // Upload any photos selected
        for (let i = 0; i < photoFiles.length; i++) {
          try {
            await listingService.uploadPhoto(listingId, photoFiles[i], i === 0)
          } catch (uploadErr) {
            console.error('Failed to upload photo', uploadErr)
          }
        }

        navigate('/landlord/my-listings', {
          state: { message: 'Listing submitted successfully for verification!' },
        })
      }
    } catch (err) {
      console.error('Listing submission failed:', err)
      const validationDetails = err.details?.validation_errors
        ? err.details.validation_errors
            .map((v) => `${v.field.replace('body -> ', '')}: ${v.message}`)
            .join(' | ')
        : null

      setError(
        validationDetails
          ? `Please check your inputs: ${validationDetails}`
          : (err.message || 'Failed to submit listing. Please verify all required fields.')
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
      {/* Wizard Progress Header */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-heading font-bold text-neutral-900 mb-2">
          Post a New Student Accommodation
        </h1>
        <p className="text-sm text-neutral-500">
          List your PG, flat, or student room to reach thousands of university students safely.
        </p>

        {/* Steps Breadcrumbs */}
        <div className="mt-6 grid grid-cols-4 gap-2">
          {STEPS.map((step) => (
            <div
              key={step.id}
              className={`pb-2 border-b-2 text-xs font-semibold tracking-wide ${
                currentStep === step.id
                  ? 'border-primary text-primary'
                  : currentStep > step.id
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-neutral-200 text-neutral-400'
              }`}
            >
              Step {step.id}: {step.name}
            </div>
          ))}
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-center gap-3 text-sm text-rose-700">
          <AlertCircle size={18} className="shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Wizard Form Cards */}
      <div className="bg-white p-6 sm:p-8 rounded-2xl border border-neutral-200 shadow-card">
        {/* Step 1: Basic Details */}
        {currentStep === 1 && (
          <div className="space-y-5">
            <h2 className="text-lg font-heading font-semibold text-neutral-900 border-b pb-2">
              Property & Pricing Basics
            </h2>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                Listing Title *
              </label>
              <input
                type="text"
                name="title"
                required
                placeholder="e.g. Spacious Single AC Room near Symbiosis Viman Nagar"
                value={formData.title}
                onChange={handleChange}
                className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Property Type *
                </label>
                <select
                  name="property_type"
                  value={formData.property_type}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                >
                  <option value="PG">Paying Guest (PG)</option>
                  <option value="APARTMENT">Full Apartment / Flat</option>
                  <option value="SHARED_ROOM">Shared Room</option>
                  <option value="STUDIO">Studio Room</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Monthly Rent (₹) *
                </label>
                <input
                  type="number"
                  name="rent_amount"
                  required
                  placeholder="8500"
                  value={formData.rent_amount}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Security Deposit (₹)
                </label>
                <input
                  type="number"
                  name="deposit_amount"
                  placeholder="15000"
                  value={formData.deposit_amount}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Rent Frequency
                </label>
                <select
                  name="rent_period"
                  value={formData.rent_period}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                >
                  <option value="MONTHLY">Monthly</option>
                  <option value="SEMESTER">Per Semester</option>
                  <option value="YEARLY">Yearly</option>
                </select>
              </div>
            </div>

            <div className="pt-4 flex justify-end">
              <button
                type="button"
                onClick={() => {
                  if (!formData.title || !formData.rent_amount) {
                    setError('Please provide a listing title and monthly rent.')
                    return
                  }
                  setError(null)
                  setCurrentStep(2)
                }}
                className="px-6 py-2.5 bg-primary text-white rounded-xl text-sm font-semibold hover:bg-primary-dark transition-colors flex items-center gap-2"
              >
                Next: Location
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Location */}
        {currentStep === 2 && (
          <div className="space-y-5">
            <h2 className="text-lg font-heading font-semibold text-neutral-900 border-b pb-2">
              Location & Campus Proximity
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  City *
                </label>
                <input
                  type="text"
                  name="city"
                  required
                  placeholder="e.g. Pune, Bengaluru"
                  value={formData.city}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Locality / Neighborhood *
                </label>
                <input
                  type="text"
                  name="locality"
                  required
                  placeholder="e.g. Viman Nagar, Shivajinagar"
                  value={formData.locality}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Street Address
                </label>
                <input
                  type="text"
                  name="address_line1"
                  placeholder="Building No, Street name"
                  value={formData.address_line1}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  State
                </label>
                <input
                  type="text"
                  name="state"
                  placeholder="Maharashtra"
                  value={formData.state}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Pincode
                </label>
                <input
                  type="text"
                  name="pincode"
                  placeholder="411014"
                  value={formData.pincode}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Nearby College / University
                </label>
                <input
                  type="text"
                  name="university_name"
                  placeholder="e.g. Symbiosis International / Pune University"
                  value={formData.university_name}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Distance to Campus (km)
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="university_distance_km"
                  placeholder="1.2"
                  value={formData.university_distance_km}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>
            </div>

            <div className="pt-4 flex justify-between">
              <button
                type="button"
                onClick={() => setCurrentStep(1)}
                className="px-5 py-2.5 border border-neutral-300 rounded-xl text-sm font-semibold text-neutral-700 hover:bg-neutral-50 transition-colors flex items-center gap-2"
              >
                <ArrowLeft size={16} />
                Back
              </button>
              <button
                type="button"
                onClick={() => {
                  if (!formData.city || !formData.locality) {
                    setError('Please specify both City and Locality.')
                    return
                  }
                  setError(null)
                  setCurrentStep(3)
                }}
                className="px-6 py-2.5 bg-primary text-white rounded-xl text-sm font-semibold hover:bg-primary-dark transition-colors flex items-center gap-2"
              >
                Next: Rules & Amenities
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Rules & Amenities */}
        {currentStep === 3 && (
          <div className="space-y-6">
            <h2 className="text-lg font-heading font-semibold text-neutral-900 border-b pb-2">
              Rules, Preferences & Amenities
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Gender Preference *
                </label>
                <select
                  name="gender_preference"
                  value={formData.gender_preference}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                >
                  <option value="ANY">Any / Co-ed</option>
                  <option value="MALE">Male (Boys Only)</option>
                  <option value="FEMALE">Female (Girls Only)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Furnishing Status *
                </label>
                <select
                  name="furnished_status"
                  value={formData.furnished_status}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                >
                  <option value="FURNISHED">Fully Furnished</option>
                  <option value="SEMI">Semi-Furnished</option>
                  <option value="UNFURNISHED">Unfurnished</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Minimum Stay (Months)
                </label>
                <input
                  type="number"
                  name="min_stay_months"
                  value={formData.min_stay_months}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                  Max Occupants Per Room
                </label>
                <input
                  type="number"
                  name="max_occupancy"
                  value={formData.max_occupancy}
                  onChange={handleChange}
                  className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm"
                />
              </div>
            </div>

            {/* Amenities Checkboxes */}
            {amenitiesList.length > 0 && (
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-2">
                  Select Included Amenities
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                  {amenitiesList.map((amenity) => {
                    const isChecked = formData.amenity_ids.includes(amenity.id)
                    return (
                      <button
                        type="button"
                        key={amenity.id}
                        onClick={() => toggleAmenity(amenity.id)}
                        className={`p-3 rounded-xl border text-left text-xs font-medium transition-all flex items-center justify-between ${
                          isChecked
                            ? 'bg-primary/5 border-primary text-primary'
                            : 'bg-neutral-50 border-neutral-200 text-neutral-700 hover:bg-neutral-100'
                        }`}
                      >
                        <span>{amenity.label}</span>
                        {isChecked && <CheckCircle2 size={16} className="text-primary" />}
                      </button>
                    )
                  })}
                </div>
              </div>
            )}

            <div className="pt-4 flex justify-between">
              <button
                type="button"
                onClick={() => setCurrentStep(2)}
                className="px-5 py-2.5 border border-neutral-300 rounded-xl text-sm font-semibold text-neutral-700 hover:bg-neutral-50 transition-colors flex items-center gap-2"
              >
                <ArrowLeft size={16} />
                Back
              </button>
              <button
                type="button"
                onClick={() => setCurrentStep(4)}
                className="px-6 py-2.5 bg-primary text-white rounded-xl text-sm font-semibold hover:bg-primary-dark transition-colors flex items-center gap-2"
              >
                Next: Photos & Submit
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        )}

        {/* Step 4: Photos, Description & Submit */}
        {currentStep === 4 && (
          <form onSubmit={handleSubmit} className="space-y-6">
            <h2 className="text-lg font-heading font-semibold text-neutral-900 border-b pb-2">
              Photos & Description
            </h2>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                Description / House Rules
              </label>
              <textarea
                name="description"
                rows={4}
                placeholder="Describe the room, sunlight, food timing, study environment, and house rules..."
                value={formData.description}
                onChange={handleChange}
                className="w-full p-3 bg-neutral-50 border border-neutral-200 rounded-xl text-sm resize-none"
              />
            </div>

            {/* Photo Upload Area */}
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-1.5">
                Upload Accommodation Photos
              </label>
              <div className="border-2 border-dashed border-neutral-300 rounded-2xl p-6 text-center hover:border-primary transition-colors bg-neutral-50 cursor-pointer relative">
                <input
                  type="file"
                  multiple
                  accept="image/*"
                  onChange={handlePhotoSelect}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <Upload size={32} className="mx-auto text-neutral-400 mb-2" />
                <p className="text-sm font-medium text-neutral-800">
                  Click or drag images to upload
                </p>
                <p className="text-xs text-neutral-400 mt-1">PNG, JPG, or WEBP up to 5MB each</p>
              </div>

              {photoPreviews.length > 0 && (
                <div className="mt-4 grid grid-cols-3 sm:grid-cols-4 gap-3">
                  {photoPreviews.map((url, idx) => (
                    <div key={idx} className="relative aspect-video rounded-xl overflow-hidden border border-neutral-200 group">
                      <img src={url} alt={`Preview ${idx + 1}`} className="w-full h-full object-cover" />
                      <button
                        type="button"
                        onClick={() => removePhoto(idx)}
                        className="absolute top-1 right-1 p-1 bg-neutral-900/80 text-white rounded-full text-xs hover:bg-rose-600 transition-colors"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="p-4 rounded-xl bg-blue-50 border border-blue-100 flex items-start gap-3 text-xs text-blue-800">
              <ShieldCheck size={20} className="text-primary shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold mb-0.5">Verification Guarantee</p>
                <p>
                  Our campus ops team verifies every property prior to making it public. Once approved, your listing
                  receives a verified badge.
                </p>
              </div>
            </div>

            <div className="pt-4 flex justify-between">
              <button
                type="button"
                onClick={() => setCurrentStep(3)}
                className="px-5 py-2.5 border border-neutral-300 rounded-xl text-sm font-semibold text-neutral-700 hover:bg-neutral-50 transition-colors flex items-center gap-2"
              >
                <ArrowLeft size={16} />
                Back
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-6 py-2.5 bg-primary text-white rounded-xl text-sm font-semibold hover:bg-primary-dark transition-colors flex items-center gap-2 disabled:opacity-50"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 size={16} className="animate-spin" />
                    Submitting...
                  </>
                ) : (
                  <>
                    Submit for Verification
                    <CheckCircle2 size={16} />
                  </>
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
