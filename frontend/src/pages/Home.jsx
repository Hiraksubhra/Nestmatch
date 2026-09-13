import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Search, MapPin, ShieldCheck, Users, MessageSquare, ArrowRight } from 'lucide-react'
import { ROUTES } from '../constants/routes'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'

export const Home = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`${ROUTES.SEARCH}?city=${encodeURIComponent(searchQuery.trim())}`)
    }
  }

  const popularCities = ['Pune', 'Bangalore', 'Mumbai', 'Delhi NCR']

  return (
    <div className="space-y-16 sm:space-y-24">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-neutral-50 border-b border-neutral-200/60 pt-12 pb-20 lg:py-24">
        {/* Subtle right-side blue tint backdrop (20% opacity) as per brandRules */}
        <div className="absolute top-0 right-0 w-1/2 h-full bg-primary-light/20 -skew-x-12 transform origin-top pointer-events-none hidden lg:block" />

        <div className="relative max-w-content mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Content (Left-aligned as per brandRules) */}
            <div className="lg:col-span-7 space-y-6">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-neutral-200 text-neutral-600 text-xs font-medium">
                <span className="w-2 h-2 rounded-full bg-success" />
                Verified accommodations for Indian universities
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-display font-heading font-bold text-neutral-900 tracking-tight leading-[1.1]">
                Find your space, <br className="hidden sm:inline" />
                <span className="text-primary">find your people.</span>
              </h1>

              <p className="text-base sm:text-lg text-neutral-600 max-w-xl leading-relaxed">
                Discover verified campus-proximate housing, eliminate scams with in-platform communication, and match with compatible roommates by lifestyle.
              </p>

              {/* Search Bar */}
              <form
                onSubmit={handleSearch}
                className="bg-white p-2 sm:p-3 rounded-xl border border-neutral-200 shadow-card flex flex-col sm:flex-row items-stretch sm:items-center gap-3 max-w-2xl"
              >
                <div className="flex-1 flex items-center gap-3 px-3">
                  <MapPin className="w-5 h-5 text-neutral-400 shrink-0" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Enter city, university, or locality..."
                    className="w-full text-base bg-transparent text-neutral-800 placeholder:text-neutral-400 focus:outline-none"
                  />
                </div>
                <Button type="submit" variant="primary" size="md" className="shrink-0">
                  <Search className="w-4 h-4 mr-1" />
                  Search homes
                </Button>
              </form>

              {/* Popular quick links */}
              <div className="flex items-center flex-wrap gap-2 text-sm text-neutral-500 pt-1">
                <span>Popular:</span>
                {popularCities.map((city) => (
                  <button
                    key={city}
                    type="button"
                    onClick={() => {
                      setSearchQuery(city)
                      navigate(`${ROUTES.SEARCH}?city=${encodeURIComponent(city)}`)
                    }}
                    className="px-2.5 py-1 rounded-lg bg-neutral-100 hover:bg-neutral-200 text-neutral-700 text-xs transition-colors font-medium"
                  >
                    {city}
                  </button>
                ))}
              </div>
            </div>

            {/* Right Graphic/Illustration */}
            <div className="lg:col-span-5 hidden lg:flex justify-center">
              <div className="relative w-full max-w-md bg-white p-6 rounded-2xl border border-neutral-200 shadow-card space-y-4">
                <div className="flex items-center justify-between border-b border-neutral-100 pb-3">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-primary-light text-primary flex items-center justify-center font-bold text-sm">
                      NM
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-neutral-900">Student Housing Guarantee</h4>
                      <p className="text-xs text-neutral-400">Pune University Campus Area</p>
                    </div>
                  </div>
                  <Badge variant="verified" showIcon>Verified</Badge>
                </div>

                <div className="space-y-3 pt-1">
                  <div className="flex items-center justify-between text-sm py-2 px-3 bg-neutral-50 rounded-lg">
                    <span className="text-neutral-600">Average distance to campus</span>
                    <span className="font-semibold text-neutral-900">0.8 km</span>
                  </div>
                  <div className="flex items-center justify-between text-sm py-2 px-3 bg-neutral-50 rounded-lg">
                    <span className="text-neutral-600">Zero broker commissions</span>
                    <span className="font-semibold text-success">Guaranteed</span>
                  </div>
                  <div className="flex items-center justify-between text-sm py-2 px-3 bg-neutral-50 rounded-lg">
                    <span className="text-neutral-600">In-platform messaging</span>
                    <span className="font-semibold text-primary">Safe & direct</span>
                  </div>
                </div>

                <div className="pt-2 text-center">
                  <Link to={ROUTES.REGISTER}>
                    <Button variant="secondary" size="sm" fullWidth>
                      Get started today
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How it works Section */}
      <section className="max-w-content mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-2xl sm:text-h2 font-heading font-semibold text-neutral-900">
            How NestMatch works
          </h2>
          <p className="text-sm sm:text-base text-neutral-600 mt-2">
            A simple, secure process built to take the anxiety out of student housing.
          </p>
        </div>

        {/* 3 Steps with horizontal connector line on desktop */}
        <div className="relative grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="hidden md:block absolute top-10 left-[18%] right-[18%] h-[2px] border-t-2 border-dashed border-neutral-200 z-0" />

          <div className="relative z-10 bg-white p-6 rounded-xl border border-neutral-200 shadow-card text-center space-y-4">
            <div className="w-14 h-14 mx-auto rounded-full bg-primary-light text-primary flex items-center justify-center">
              <Search className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-heading font-semibold text-neutral-900">1. Discover & Filter</h3>
            <p className="text-sm text-neutral-600 leading-relaxed">
              Search by college, price, gender preference, and amenities like Wi-Fi, power backup, and food.
            </p>
          </div>

          <div className="relative z-10 bg-white p-6 rounded-xl border border-neutral-200 shadow-card text-center space-y-4">
            <div className="w-14 h-14 mx-auto rounded-full bg-accent-light text-accent-dark flex items-center justify-center">
              <MessageSquare className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-heading font-semibold text-neutral-900">2. Inquire Safely</h3>
            <p className="text-sm text-neutral-600 leading-relaxed">
              Connect with verified landlords inside the app without revealing your personal phone number.
            </p>
          </div>

          <div className="relative z-10 bg-white p-6 rounded-xl border border-neutral-200 shadow-card text-center space-y-4">
            <div className="w-14 h-14 mx-auto rounded-full bg-green-50 text-success flex items-center justify-center">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-heading font-semibold text-neutral-900">3. Book with Confidence</h3>
            <p className="text-sm text-neutral-600 leading-relaxed">
              Lock in your room with transparent terms and move into a student-vetted community.
            </p>
          </div>
        </div>
      </section>

      {/* Roommate Matching CTA Band */}
      <section className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="bg-primary-light rounded-2xl p-8 sm:p-12 border border-blue-200 grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
          <div className="md:col-span-8 space-y-3">
            <Badge variant="type">Roommate Matching</Badge>
            <h2 className="text-2xl sm:text-3xl font-heading font-bold text-neutral-900">
              Looking for someone to share an apartment with?
            </h2>
            <p className="text-neutral-700 text-base max-w-xl leading-relaxed">
              Create your flatmate profile with study habits, sleep schedule, and dietary preferences to connect with compatible college peers.
            </p>
          </div>
          <div className="md:col-span-4 flex md:justify-end">
            <Link to={ROUTES.REGISTER}>
              <Button variant="primary" size="lg" className="w-full sm:w-auto">
                Create flatmate profile
                <ArrowRight className="w-4 h-4 ml-1" />
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
