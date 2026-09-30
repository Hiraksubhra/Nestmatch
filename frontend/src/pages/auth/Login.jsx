import React, { useState } from 'react'
import { Link, useNavigate, useLocation, useSearchParams } from 'react-router-dom'
import { GraduationCap, Building2, ShieldCheck, Users, Home, MessageSquare, Sparkles } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../constants/routes'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/Card'
import { cn } from '../../lib/utils'

export const Login = () => {
  const location = useLocation()
  const [searchParams] = useSearchParams()

  const initialRole =
    location.state?.role ||
    (searchParams.get('role')?.toUpperCase() === 'LANDLORD' ? 'LANDLORD' : 'STUDENT')

  const [role, setRole] = useState(initialRole)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [formError, setFormError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const { login } = useAuthStore()
  const navigate = useNavigate()

  const from = location.state?.from?.pathname || null

  const handleFillDemo = () => {
    if (role === 'LANDLORD') {
      setEmail('landlord@nestmatch.in')
      setPassword('Landlord123!')
    } else {
      setEmail('student@nestmatch.in')
      setPassword('Student123!')
    }
    setFormError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError('')

    if (!email || !password) {
      setFormError('Please enter both email and password.')
      return
    }

    setIsSubmitting(true)
    try {
      const user = await login({ email, password })
      if (from) {
        navigate(from, { replace: true })
      } else if (user.role === 'LANDLORD') {
        navigate(ROUTES.MY_LISTINGS, { replace: true })
      } else {
        navigate(ROUTES.SEARCH, { replace: true })
      }
    } catch (err) {
      setFormError(err.message || 'Invalid email or password.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="max-w-lg mx-auto px-4 py-10 sm:py-14">
      <Card className="border border-neutral-200/80 shadow-card">
        {/* Role Toggle Switcher */}
        <div className="p-4 pb-0">
          <div className="grid grid-cols-2 gap-2 p-1 bg-neutral-100/80 rounded-xl">
            <button
              type="button"
              onClick={() => {
                setRole('STUDENT')
                setFormError('')
              }}
              className={cn(
                'flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-sm font-semibold transition-all',
                role === 'STUDENT'
                  ? 'bg-white text-primary shadow-sm'
                  : 'text-neutral-600 hover:text-neutral-900'
              )}
            >
              <GraduationCap size={18} />
              <span>Student Sign In</span>
            </button>
            <button
              type="button"
              onClick={() => {
                setRole('LANDLORD')
                setFormError('')
              }}
              className={cn(
                'flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-sm font-semibold transition-all',
                role === 'LANDLORD'
                  ? 'bg-white text-primary shadow-sm'
                  : 'text-neutral-600 hover:text-neutral-900'
              )}
            >
              <Building2 size={18} />
              <span>Landlord Portal</span>
            </button>
          </div>
        </div>

        <CardHeader className="text-center pt-4 pb-2 space-y-1.5">
          <CardTitle className="text-2xl font-bold font-heading">
            {role === 'LANDLORD' ? 'Landlord & Property Owner Portal' : 'Student Accommodation Sign In'}
          </CardTitle>
          <CardDescription className="text-xs sm:text-sm text-neutral-500 max-w-sm mx-auto">
            {role === 'LANDLORD'
              ? 'Manage your student housing listings, review inquiries, and verify accommodations.'
              : 'Browse verified campus rentals, connect with roommates, and send inquiries.'}
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4 pt-2">
          {/* Role-Specific Feature Highlight Pills */}
          <div className="p-3 rounded-xl bg-neutral-50 border border-neutral-100 space-y-2">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-neutral-400 block">
              {role === 'LANDLORD' ? 'Landlord Features' : 'Student Features'}
            </span>
            {role === 'LANDLORD' ? (
              <div className="grid grid-cols-2 gap-2 text-xs text-neutral-700">
                <div className="flex items-center gap-1.5">
                  <Home size={14} className="text-primary shrink-0" />
                  <span>List & Manage Rentals</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <MessageSquare size={14} className="text-primary shrink-0" />
                  <span>Direct Student Inquiries</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <ShieldCheck size={14} className="text-emerald-600 shrink-0" />
                  <span>Campus Ops Verified</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Sparkles size={14} className="text-amber-500 shrink-0" />
                  <span>High Student Visibility</span>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-2 text-xs text-neutral-700">
                <div className="flex items-center gap-1.5">
                  <ShieldCheck size={14} className="text-primary shrink-0" />
                  <span>Campus-Verified PGs & Flats</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Users size={14} className="text-primary shrink-0" />
                  <span>Roommate Match Finder</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <MessageSquare size={14} className="text-primary shrink-0" />
                  <span>Contact Landlords Free</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Sparkles size={14} className="text-emerald-600 shrink-0" />
                  <span>Zero Brokerage Fees</span>
                </div>
              </div>
            )}
          </div>

          {/* Quick Demo Autofill Button */}
          <button
            type="button"
            onClick={handleFillDemo}
            className="w-full py-2 px-3 bg-primary/5 hover:bg-primary/10 border border-primary/20 text-primary rounded-xl text-xs font-semibold transition-colors flex items-center justify-center gap-1.5"
          >
            <Sparkles size={14} />
            Quick Demo Fill: {role === 'LANDLORD' ? 'landlord@nestmatch.in' : 'student@nestmatch.in'}
          </button>

          {formError && (
            <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-danger text-sm">
              {formError}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Email address"
              type="email"
              placeholder={role === 'LANDLORD' ? 'landlord@nestmatch.in' : 'student@nestmatch.in'}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <Button
              type="submit"
              variant="primary"
              size="md"
              fullWidth
              isLoading={isSubmitting}
            >
              Sign in as {role === 'LANDLORD' ? 'Landlord' : 'Student'}
            </Button>
          </form>

          <div className="text-center text-sm text-neutral-600 pt-2 border-t border-neutral-100">
            {role === 'LANDLORD' ? (
              <span>
                New property owner?{' '}
                <Link
                  to="/register?role=landlord"
                  className="text-primary font-medium hover:underline"
                >
                  Register as Landlord
                </Link>
              </span>
            ) : (
              <span>
                Don't have a student account?{' '}
                <Link
                  to="/register?role=student"
                  className="text-primary font-medium hover:underline"
                >
                  Create Student Account
                </Link>
              </span>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
