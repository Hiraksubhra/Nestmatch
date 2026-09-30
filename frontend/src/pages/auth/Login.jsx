import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../constants/routes'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/Card'

export const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [formError, setFormError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const { login } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()

  const from = location.state?.from?.pathname || null

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
        navigate(ROUTES.LANDLORD_DASHBOARD, { replace: true })
      } else {
        navigate(ROUTES.STUDENT_DASHBOARD, { replace: true })
      }
    } catch (err) {
      setFormError(err.message || 'Invalid email or password.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-12 sm:py-16">
      <Card>
        <CardHeader className="text-center space-y-1">
          <CardTitle>Sign in to NestMatch</CardTitle>
          <CardDescription>
            Enter your credentials to access your inquiries, listings, and profile.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {formError && (
            <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-danger text-sm">
              {formError}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Email address"
              type="email"
              placeholder="e.g. aanya@college.edu"
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
              Sign in
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-neutral-600">
            Don't have an account?{' '}
            <Link to={ROUTES.REGISTER} className="text-primary font-medium hover:underline">
              Create an account
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
