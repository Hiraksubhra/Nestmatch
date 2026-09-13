import React from 'react'
import { Link } from 'react-router-dom'
import { ROUTES } from '../../constants/routes'

export const Footer = () => {
  return (
    <footer className="bg-white border-t border-neutral-200 mt-auto">
      <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-md bg-primary flex items-center justify-center text-white">
                <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current">
                  <path d="M12 2C7.58 2 4 5.58 4 10c0 5.25 8 12 8 12s8-6.75 8-12c0-4.42-3.58-8-8-8zm0 11c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3z" />
                </svg>
              </div>
              <span className="font-heading font-bold text-lg text-neutral-900">NestMatch</span>
            </div>
            <p className="text-sm text-neutral-600 leading-relaxed">
              Find your space, find your people. Verified student accommodations and lifestyle-matched flatmates across India.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-neutral-900 mb-3">Discovery</h4>
            <ul className="space-y-2 text-sm text-neutral-600">
              <li><Link to={ROUTES.HOME} className="hover:text-primary transition-colors">Student PGs in Pune</Link></li>
              <li><Link to={ROUTES.HOME} className="hover:text-primary transition-colors">Shared Flats in Bangalore</Link></li>
              <li><Link to={ROUTES.HOME} className="hover:text-primary transition-colors">Hostels in Mumbai</Link></li>
              <li><Link to={ROUTES.HOME} className="hover:text-primary transition-colors">Accommodations in Delhi NCR</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-neutral-900 mb-3">Platform</h4>
            <ul className="space-y-2 text-sm text-neutral-600">
              <li><Link to={ROUTES.FLATMATES} className="hover:text-primary transition-colors">Find Roommates</Link></li>
              <li><Link to={ROUTES.REGISTER} className="hover:text-primary transition-colors">Post as Landlord</Link></li>
              <li><Link to={ROUTES.LOGIN} className="hover:text-primary transition-colors">Verified Landlords</Link></li>
              <li><a href="#safety" className="hover:text-primary transition-colors">Safety Standards</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-neutral-900 mb-3">Trust & Security</h4>
            <ul className="space-y-2 text-sm text-neutral-600">
              <li><a href="#scam-prevention" className="hover:text-primary transition-colors">Scam Prevention</a></li>
              <li><a href="#terms" className="hover:text-primary transition-colors">Terms of Service</a></li>
              <li><a href="#privacy" className="hover:text-primary transition-colors">Privacy Policy</a></li>
              <li><a href="#support" className="hover:text-primary transition-colors">Help Center</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-neutral-200 mt-8 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-neutral-400">
          <p>© {new Date().getFullYear()} NestMatch Technologies. All rights reserved.</p>
          <p>Built for students, by students.</p>
        </div>
      </div>
    </footer>
  )
}
