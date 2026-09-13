import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Menu, X, User as UserIcon, LogOut, Home, Search, Users, PlusCircle } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../constants/routes'
import { Button } from '../ui/Button'
import { Badge } from '../ui/Badge'

export const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuthStore()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = async () => {
    await logout()
    navigate(ROUTES.HOME)
  }

  const dashboardRoute = user?.role === 'LANDLORD' ? ROUTES.LANDLORD_DASHBOARD : ROUTES.STUDENT_DASHBOARD

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-neutral-200">
      <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to={ROUTES.HOME} className="flex items-center gap-2.5 focus:outline-none">
          <div className="w-9 h-9 rounded-lg bg-primary flex items-center justify-center text-white shadow-sm">
            <svg viewBox="0 0 24 24" className="w-5 h-5 fill-current" aria-hidden="true">
              <path d="M12 2C7.58 2 4 5.58 4 10c0 5.25 8 12 8 12s8-6.75 8-12c0-4.42-3.58-8-8-8zm0 11c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3z" />
            </svg>
          </div>
          <span className="text-xl font-heading font-bold tracking-tight text-neutral-900">
            Nest<span className="text-primary">Match</span>
          </span>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-6">
          <Link
            to={ROUTES.HOME}
            className="text-neutral-600 hover:text-primary transition-colors text-sm font-medium"
          >
            Find homes
          </Link>
          <Link
            to={ROUTES.FLATMATES}
            className="text-neutral-600 hover:text-primary transition-colors text-sm font-medium"
          >
            Roommates
          </Link>
          {user?.role === 'LANDLORD' ? (
            <Link
              to={ROUTES.CREATE_LISTING}
              className="text-neutral-600 hover:text-primary transition-colors text-sm font-medium"
            >
              Post listing
            </Link>
          ) : (
            <Link
              to={ROUTES.REGISTER}
              className="text-neutral-600 hover:text-primary transition-colors text-sm font-medium"
            >
              List a property
            </Link>
          )}
        </nav>

        {/* Desktop Auth State */}
        <div className="hidden md:flex items-center gap-3">
          {isAuthenticated && user ? (
            <div className="flex items-center gap-3">
              <Link to={dashboardRoute} className="flex items-center gap-2 hover:opacity-80 transition">
                <div className="w-8 h-8 rounded-full bg-primary-light text-primary font-medium flex items-center justify-center text-xs">
                  {user.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
                </div>
                <div className="flex flex-col text-left">
                  <span className="text-sm font-medium text-neutral-800 leading-tight">
                    {user.full_name.split(' ')[0]}
                  </span>
                  <Badge variant={user.role === 'LANDLORD' ? 'type' : 'default'} className="text-[10px] py-0 px-1.5 w-fit">
                    {user.role}
                  </Badge>
                </div>
              </Link>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                aria-label="Log out"
                className="text-neutral-600 hover:text-danger"
              >
                <LogOut className="w-4 h-4" />
              </Button>
            </div>
          ) : (
            <>
              <Link to={ROUTES.LOGIN}>
                <Button variant="ghost" size="sm">
                  Sign in
                </Button>
              </Link>
              <Link to={ROUTES.REGISTER}>
                <Button variant="primary" size="sm">
                  Register
                </Button>
              </Link>
            </>
          )}
        </div>

        {/* Mobile Menu Toggle */}
        <div className="flex md:hidden items-center">
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100"
            aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-neutral-200 bg-white px-4 py-4 space-y-3">
          <Link
            to={ROUTES.HOME}
            onClick={() => setMobileMenuOpen(false)}
            className="flex items-center gap-2 py-2 text-neutral-800 font-medium"
          >
            <Search className="w-4 h-4 text-neutral-400" />
            Find homes
          </Link>
          <Link
            to={ROUTES.FLATMATES}
            onClick={() => setMobileMenuOpen(false)}
            className="flex items-center gap-2 py-2 text-neutral-800 font-medium"
          >
            <Users className="w-4 h-4 text-neutral-400" />
            Roommates
          </Link>
          <div className="pt-3 border-t border-neutral-100 space-y-2">
            {isAuthenticated && user ? (
              <>
                <Link
                  to={dashboardRoute}
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center justify-between py-2 text-neutral-800 font-medium"
                >
                  <span>Dashboard ({user.role})</span>
                  <span className="text-xs text-neutral-500">{user.email}</span>
                </Link>
                <Button
                  variant="secondary"
                  size="md"
                  fullWidth
                  onClick={() => {
                    setMobileMenuOpen(false)
                    handleLogout()
                  }}
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Log out
                </Button>
              </>
            ) : (
              <div className="flex flex-col gap-2">
                <Link to={ROUTES.LOGIN} onClick={() => setMobileMenuOpen(false)}>
                  <Button variant="secondary" size="md" fullWidth>
                    Sign in
                  </Button>
                </Link>
                <Link to={ROUTES.REGISTER} onClick={() => setMobileMenuOpen(false)}>
                  <Button variant="primary" size="md" fullWidth>
                    Register
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  )
}
