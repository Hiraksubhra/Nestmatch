import React, { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Search, SlidersHorizontal, RotateCcw, Building2, Home, MapPin, IndianRupee, Loader2, GraduationCap } from 'lucide-react'
import { listingService } from '../../services/listingService'
import { campusService } from '../../services/campusService'
import { ListingCard } from '../../components/listings/ListingCard'

const CITIES = ['All Cities', 'Pune', 'Bengaluru', 'Delhi NCR', 'Mumbai', 'Hyderabad', 'Kota', 'Noida', 'Chennai']
const PROPERTY_TYPES = [
  { label: 'All Types', value: '' },
  { label: 'PG / Hostel', value: 'PG' },
  { label: 'Apartment', value: 'APARTMENT' },
  { label: 'Shared Room', value: 'SHARED_ROOM' },
  { label: 'Studio', value: 'STUDIO' },
]

export const SearchResults = () => {
  const [searchParams, setSearchParams] = useSearchParams()

  const [listings, setListings] = useState([])
  const [amenitiesList, setAmenitiesList] = useState([])
  const [campusesList, setCampusesList] = useState([])
  const [totalCount, setTotalCount] = useState(0)
  const [totalPages, setTotalPages] = useState(1)
  const [isLoading, setIsLoading] = useState(true)
  const [showMobileFilters, setShowMobileFilters] = useState(false)

  // Draft Filters State (applied only when user clicks "Apply Filters")
  const [draftFilters, setDraftFilters] = useState({
    city: searchParams.get('city') || '',
    campus_id: searchParams.get('campus_id') || '',
    max_distance_km: searchParams.get('max_distance_km') || '',
    property_type: searchParams.get('property_type') || '',
    gender: searchParams.get('gender') || '',
    min_rent: searchParams.get('min_rent') || '',
    max_rent: searchParams.get('max_rent') || '',
    search: searchParams.get('search') || '',
    sort: searchParams.get('sort') || 'newest',
    amenities: searchParams.get('amenities')
      ? searchParams.get('amenities').split(',').filter(Boolean).map(Number)
      : [],
  })

  // Synchronize draft filters whenever searchParams changes externally
  useEffect(() => {
    setDraftFilters({
      city: searchParams.get('city') || '',
      campus_id: searchParams.get('campus_id') || '',
      max_distance_km: searchParams.get('max_distance_km') || '',
      property_type: searchParams.get('property_type') || '',
      gender: searchParams.get('gender') || '',
      min_rent: searchParams.get('min_rent') || '',
      max_rent: searchParams.get('max_rent') || '',
      search: searchParams.get('search') || '',
      sort: searchParams.get('sort') || 'newest',
      amenities: searchParams.get('amenities')
        ? searchParams.get('amenities').split(',').filter(Boolean).map(Number)
        : [],
    })
  }, [searchParams])

  // Active filters applied in the URL
  const activeCity = searchParams.get('city') || ''
  const activeCampusId = searchParams.get('campus_id') || ''
  const activeMaxDistanceKm = searchParams.get('max_distance_km') || ''
  const activePropertyType = searchParams.get('property_type') || ''
  const activeGender = searchParams.get('gender') || ''
  const activeMinRent = searchParams.get('min_rent') || ''
  const activeMaxRent = searchParams.get('max_rent') || ''
  const activeSearch = searchParams.get('search') || ''
  const activeSort = searchParams.get('sort') || 'newest'
  const activePage = parseInt(searchParams.get('page') || '1', 10)
  const activeAmenities = searchParams.get('amenities')
    ? searchParams.get('amenities').split(',').filter(Boolean).map(Number)
    : []

  // Load available amenities
  useEffect(() => {
    listingService.getAmenities()
      .then((res) => {
        if (res.success && res.data) {
          setAmenitiesList(res.data)
        }
      })
      .catch(() => {})
  }, [])

  // Load campuses (optionally for draft or active city)
  useEffect(() => {
    const cityFilter = draftFilters.city && draftFilters.city !== 'All Cities' ? draftFilters.city : null
    campusService.getCampuses(cityFilter)
      .then((res) => {
        if (res?.data) {
          setCampusesList(res.data)
        }
      })
      .catch(() => {})
  }, [draftFilters.city])

  // Fetch listings on URL searchParams change
  useEffect(() => {
    const fetchListings = async () => {
      setIsLoading(true)
      try {
        const params = {
          page: activePage,
          limit: 12,
          sort: activeSort,
        }
        if (activeCity && activeCity !== 'All Cities') params.city = activeCity
        if (activeCampusId) params.campus_id = activeCampusId
        if (activeMaxDistanceKm) params.max_distance_km = activeMaxDistanceKm
        if (activePropertyType) params.property_type = activePropertyType
        if (activeGender && activeGender !== 'ANY') params.gender_preference = activeGender
        if (activeMinRent) params.min_rent = activeMinRent
        if (activeMaxRent) params.max_rent = activeMaxRent
        if (activeSearch) params.search = activeSearch
        if (activeAmenities.length > 0) params.amenities = activeAmenities.join(',')

        const res = await listingService.searchListings(params)
        if (res.success) {
          setListings(res.data || [])
          setTotalCount(res.meta?.total || 0)
          setTotalPages(res.meta?.pages || 1)
        }
      } catch (err) {
        console.error('Failed to load listings', err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchListings()
  }, [searchParams])

  const handleApplyFilters = () => {
    const nextParams = new URLSearchParams()
    if (draftFilters.city && draftFilters.city !== 'All Cities') nextParams.set('city', draftFilters.city)
    if (draftFilters.campus_id) nextParams.set('campus_id', draftFilters.campus_id)
    if (draftFilters.max_distance_km) nextParams.set('max_distance_km', draftFilters.max_distance_km)
    if (draftFilters.property_type) nextParams.set('property_type', draftFilters.property_type)
    if (draftFilters.gender && draftFilters.gender !== 'ANY') nextParams.set('gender', draftFilters.gender)
    if (draftFilters.min_rent) nextParams.set('min_rent', draftFilters.min_rent)
    if (draftFilters.max_rent) nextParams.set('max_rent', draftFilters.max_rent)
    if (draftFilters.search?.trim()) nextParams.set('search', draftFilters.search.trim())
    if (draftFilters.sort && draftFilters.sort !== 'newest') nextParams.set('sort', draftFilters.sort)
    if (draftFilters.amenities?.length > 0) nextParams.set('amenities', draftFilters.amenities.join(','))
    nextParams.set('page', '1')
    setSearchParams(nextParams)
    setShowMobileFilters(false)
  }

  const handleResetFilters = () => {
    setDraftFilters({
      city: '',
      campus_id: '',
      max_distance_km: '',
      property_type: '',
      gender: '',
      min_rent: '',
      max_rent: '',
      search: '',
      sort: 'newest',
      amenities: [],
    })
    setSearchParams(new URLSearchParams())
    setShowMobileFilters(false)
  }

  const toggleDraftAmenity = (id) => {
    setDraftFilters((prev) => {
      const exists = prev.amenities.includes(id)
      return {
        ...prev,
        amenities: exists
          ? prev.amenities.filter((item) => item !== id)
          : [...prev.amenities, id],
      }
    })
  }

  const handleSortChange = (newSort) => {
    setDraftFilters((prev) => ({ ...prev, sort: newSort }))
    const nextParams = new URLSearchParams(searchParams)
    if (newSort && newSort !== 'newest') {
      nextParams.set('sort', newSort)
    } else {
      nextParams.delete('sort')
    }
    nextParams.set('page', '1')
    setSearchParams(nextParams)
  }

  // Count active draft filters
  const activeDraftFilterCount = [
    draftFilters.city && draftFilters.city !== 'All Cities',
    draftFilters.campus_id,
    draftFilters.max_distance_km,
    draftFilters.property_type,
    draftFilters.gender,
    draftFilters.min_rent,
    draftFilters.max_rent,
    draftFilters.amenities?.length > 0,
  ].filter(Boolean).length

  return (
    <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Top Search Bar & Mobile Filter Trigger */}
      <div className="flex flex-col md:flex-row gap-4 items-center justify-between mb-8 pb-6 border-b border-neutral-200">
        <form
          onSubmit={(e) => {
            e.preventDefault()
            handleApplyFilters()
          }}
          className="w-full md:w-auto flex-1 max-w-xl flex gap-2"
        >
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
            <input
              type="text"
              placeholder="Search by college, area, or listing title..."
              value={draftFilters.search}
              onChange={(e) => setDraftFilters((prev) => ({ ...prev, search: e.target.value }))}
              className="w-full pl-10 pr-4 py-2.5 bg-white border border-neutral-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2.5 bg-primary hover:bg-primary-dark text-white rounded-xl text-sm font-semibold transition-colors shadow-sm shrink-0"
          >
            Search
          </button>
        </form>

        <div className="w-full md:w-auto flex items-center justify-between md:justify-end gap-3">
          <button
            onClick={() => setShowMobileFilters(!showMobileFilters)}
            className="md:hidden flex items-center gap-2 px-4 py-2 bg-neutral-100 hover:bg-neutral-200 text-neutral-800 rounded-xl text-sm font-medium transition-colors"
          >
            <SlidersHorizontal size={16} />
            Filters {activeDraftFilterCount > 0 ? `(${activeDraftFilterCount})` : ''}
          </button>

          {/* Sort By Dropdown */}
          <div className="flex items-center gap-2 text-sm text-neutral-600">
            <span className="hidden sm:inline">Sort by:</span>
            <select
              value={draftFilters.sort}
              onChange={(e) => handleSortChange(e.target.value)}
              className="bg-white border border-neutral-300 rounded-xl px-3 py-2 text-sm text-neutral-800 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
            >
              <option value="newest">Newest First</option>
              <option value="distance_asc">Nearest to Campus</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="views">Most Popular</option>
            </select>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        {/* Sidebar Filters */}
        <aside
          className={`${
            showMobileFilters ? 'block' : 'hidden'
          } md:block md:col-span-1 bg-white p-5 rounded-2xl border border-neutral-200 shadow-sm space-y-6 h-fit sticky top-24`}
        >
          <div className="flex items-center justify-between pb-3 border-b border-neutral-100">
            <h2 className="font-heading font-semibold text-neutral-900 text-base flex items-center gap-2">
              <SlidersHorizontal size={18} className="text-primary" />
              Filter Listings
            </h2>
            <button
              onClick={handleResetFilters}
              className="text-xs text-neutral-500 hover:text-primary flex items-center gap-1 transition-colors"
            >
              <RotateCcw size={12} />
              Reset All
            </button>
          </div>

          {/* Primary Apply Filters Button (Top) */}
          <button
            onClick={handleApplyFilters}
            className="w-full py-2.5 px-4 bg-primary hover:bg-primary-dark text-white font-semibold text-sm rounded-xl shadow-sm transition-all flex items-center justify-center gap-2 active:scale-[0.99]"
          >
            <SlidersHorizontal size={16} />
            Apply Filters {activeDraftFilterCount > 0 ? `(${activeDraftFilterCount})` : ''}
          </button>

          {/* City Filter */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-2">
              City
            </label>
            <select
              value={draftFilters.city}
              onChange={(e) =>
                setDraftFilters((prev) => ({
                  ...prev,
                  city: e.target.value === 'All Cities' ? '' : e.target.value,
                  campus_id: '', // reset campus if city changes
                }))
              }
              className="w-full bg-neutral-50 border border-neutral-200 rounded-xl p-2.5 text-sm text-neutral-800 focus:outline-none focus:ring-2 focus:ring-primary/20"
            >
              {CITIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          {/* Campus Proximity Filter (PostGIS Spatial) */}
          <div className="bg-primary/5 p-3.5 rounded-xl border border-primary/15 space-y-3">
            <label className="block text-xs font-semibold uppercase tracking-wider text-primary flex items-center gap-1.5">
              <GraduationCap size={15} />
              College / University
            </label>
            <select
              value={draftFilters.campus_id}
              onChange={(e) => {
                const nextCampus = e.target.value
                setDraftFilters((prev) => ({
                  ...prev,
                  campus_id: nextCampus,
                  // Auto set sort to distance if selecting a campus
                  sort: nextCampus ? 'distance_asc' : prev.sort,
                  max_distance_km: nextCampus && !prev.max_distance_km ? '5' : prev.max_distance_km,
                }))
              }}
              className="w-full bg-white border border-primary/20 rounded-lg p-2 text-xs text-neutral-800 focus:outline-none focus:ring-2 focus:ring-primary/30"
            >
              <option value="">Select Campus / College</option>
              {campusesList.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.short_name || c.name} ({c.locality || c.city})
                </option>
              ))}
            </select>

            {draftFilters.campus_id && (
              <div className="pt-2 border-t border-primary/10">
                <div className="flex items-center justify-between text-[11px] font-medium text-neutral-600 mb-1.5">
                  <span>Max Radius:</span>
                  <span className="font-bold text-primary">
                    {draftFilters.max_distance_km ? `< ${draftFilters.max_distance_km} km` : 'Any'}
                  </span>
                </div>
                <div className="grid grid-cols-4 gap-1">
                  {['2', '5', '10', ''].map((dist) => (
                    <button
                      key={dist}
                      type="button"
                      onClick={() => setDraftFilters((prev) => ({ ...prev, max_distance_km: dist }))}
                      className={`py-1 text-[11px] rounded font-medium transition-colors ${
                        draftFilters.max_distance_km === dist
                          ? 'bg-primary text-white'
                          : 'bg-white text-neutral-600 border border-neutral-200 hover:bg-neutral-50'
                      }`}
                    >
                      {dist ? `${dist}km` : 'All'}
                    </button>
                  ))}
                </div>
                <p className="text-[10px] text-neutral-500 mt-2">
                  📍 PostGIS real-time spatial calculation
                </p>
              </div>
            )}
          </div>

          {/* Property Type Filter */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-2">
              Property Type
            </label>
            <div className="space-y-1.5">
              {PROPERTY_TYPES.map((pt) => (
                <button
                  key={pt.value}
                  type="button"
                  onClick={() => setDraftFilters((prev) => ({ ...prev, property_type: pt.value }))}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                    draftFilters.property_type === pt.value
                      ? 'bg-primary text-white font-medium shadow-sm'
                      : 'text-neutral-700 hover:bg-neutral-100'
                  }`}
                >
                  {pt.label}
                </button>
              ))}
            </div>
          </div>

          {/* Budget Range Filter */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-2">
              Monthly Budget (₹)
            </label>
            <div className="grid grid-cols-2 gap-2">
              <input
                type="number"
                placeholder="Min ₹"
                value={draftFilters.min_rent}
                onChange={(e) => setDraftFilters((prev) => ({ ...prev, min_rent: e.target.value }))}
                className="w-full bg-neutral-50 border border-neutral-200 rounded-lg p-2 text-sm"
              />
              <input
                type="number"
                placeholder="Max ₹"
                value={draftFilters.max_rent}
                onChange={(e) => setDraftFilters((prev) => ({ ...prev, max_rent: e.target.value }))}
                className="w-full bg-neutral-50 border border-neutral-200 rounded-lg p-2 text-sm"
              />
            </div>
          </div>

          {/* Gender Preference */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-2">
              Gender Allowed
            </label>
            <div className="grid grid-cols-3 gap-1.5 bg-neutral-100 p-1 rounded-xl text-xs">
              {[
                { label: 'All', value: '' },
                { label: 'Boys', value: 'MALE' },
                { label: 'Girls', value: 'FEMALE' },
              ].map((g) => (
                <button
                  key={g.value}
                  type="button"
                  onClick={() => setDraftFilters((prev) => ({ ...prev, gender: g.value }))}
                  className={`py-1.5 rounded-lg font-medium transition-all ${
                    draftFilters.gender === g.value
                      ? 'bg-white text-neutral-900 shadow-sm'
                      : 'text-neutral-600 hover:text-neutral-900'
                  }`}
                >
                  {g.label}
                </button>
              ))}
            </div>
          </div>

          {/* Amenities Multi-Select */}
          {amenitiesList.length > 0 && (
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-2">
                Amenities
              </label>
              <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                {amenitiesList.map((amenity) => (
                  <label
                    key={amenity.id}
                    className="flex items-center gap-2 text-sm text-neutral-700 cursor-pointer hover:text-neutral-900"
                  >
                    <input
                      type="checkbox"
                      checked={draftFilters.amenities?.includes(amenity.id)}
                      onChange={() => toggleDraftAmenity(amenity.id)}
                      className="rounded border-neutral-300 text-primary focus:ring-primary h-4 w-4"
                    />
                    <span className="truncate">{amenity.label}</span>
                  </label>
                ))}
              </div>
            </div>
          )}

          {/* Bottom Apply / Reset Action Group */}
          <div className="pt-2 border-t border-neutral-100 space-y-2">
            <button
              onClick={handleApplyFilters}
              className="w-full py-2.5 px-4 bg-primary hover:bg-primary-dark text-white font-semibold text-sm rounded-xl shadow-sm transition-all flex items-center justify-center gap-2"
            >
              <SlidersHorizontal size={16} />
              Apply Filters
            </button>
            <button
              onClick={handleResetFilters}
              className="w-full py-2 px-4 bg-neutral-100 hover:bg-neutral-200 text-neutral-700 font-medium text-xs rounded-xl transition-colors"
            >
              Clear All Filters
            </button>
          </div>
        </aside>

        {/* Results Main Area */}
        <main className="md:col-span-3">
          {/* Header Summary */}
          <div className="mb-4 flex items-center justify-between">
            <p className="text-sm text-neutral-600">
              Showing <span className="font-semibold text-neutral-900">{totalCount}</span> verified places
              {activeCity ? ` in ${activeCity}` : ''}
            </p>
          </div>

          {/* Listings Grid */}
          {isLoading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <div key={n} className="bg-white rounded-2xl border border-neutral-200 overflow-hidden animate-pulse">
                  <div className="aspect-[4/3] bg-neutral-200 w-full" />
                  <div className="p-4 space-y-3">
                    <div className="h-4 bg-neutral-200 rounded w-1/3" />
                    <div className="h-5 bg-neutral-200 rounded w-4/5" />
                    <div className="h-4 bg-neutral-200 rounded w-1/2" />
                  </div>
                </div>
              ))}
            </div>
          ) : listings.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {listings.map((listing) => (
                <ListingCard key={listing.id} listing={listing} />
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-neutral-200 p-12 text-center my-8">
              <Building2 className="mx-auto text-neutral-400 mb-3" size={48} />
              <h3 className="font-heading font-semibold text-lg text-neutral-900 mb-1">
                No matching accommodations found
              </h3>
              <p className="text-sm text-neutral-500 max-w-sm mx-auto mb-6">
                Try loosening your filters, broadening your budget range, or selecting a nearby locality.
              </p>
              <button
                onClick={handleResetFilters}
                className="px-5 py-2.5 bg-primary hover:bg-primary-dark text-white rounded-xl text-sm font-medium transition-colors shadow-sm"
              >
                Clear All Filters
              </button>
            </div>
          )}

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="mt-10 flex items-center justify-center gap-2">
              <button
                disabled={activePage <= 1}
                onClick={() => {
                  const nextParams = new URLSearchParams(searchParams)
                  nextParams.set('page', (activePage - 1).toString())
                  setSearchParams(nextParams)
                  window.scrollTo({ top: 0, behavior: 'smooth' })
                }}
                className="px-4 py-2 border border-neutral-300 rounded-xl text-sm font-medium disabled:opacity-40 disabled:cursor-not-allowed hover:bg-neutral-50 transition-colors"
              >
                Previous
              </button>
              <span className="text-sm text-neutral-600 px-3">
                Page {activePage} of {totalPages}
              </span>
              <button
                disabled={activePage >= totalPages}
                onClick={() => {
                  const nextParams = new URLSearchParams(searchParams)
                  nextParams.set('page', (activePage + 1).toString())
                  setSearchParams(nextParams)
                  window.scrollTo({ top: 0, behavior: 'smooth' })
                }}
                className="px-4 py-2 border border-neutral-300 rounded-xl text-sm font-medium disabled:opacity-40 disabled:cursor-not-allowed hover:bg-neutral-50 transition-colors"
              >
                Next
              </button>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
