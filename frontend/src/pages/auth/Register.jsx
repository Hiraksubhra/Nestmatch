import { Link, useNavigate, useLocation, useSearchParams } from 'react-router-dom'
import { GraduationCap, Building2 } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../constants/routes'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../components/ui/Card'
import { cn } from '../../lib/utils'

export const Register = () => {
  const location = useLocation()
  const [searchParams] = useSearchParams()

  const initialRole =
    location.state?.role ||
    (searchParams.get('role')?.toUpperCase() === 'LANDLORD' ? 'LANDLORD' : 'STUDENT')

  const [role, setRole] = useState(initialRole)
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [phone, setPhone] = useState('')
  const [formError, setFormError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const { register } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError('')

    if (!fullName.trim() || !email.trim() || !password) {
      setFormError('Please fill in all required fields.')
      return
    }

    if (password.length < 6) {
      setFormError('Password must be at least 6 characters long.')
      return
    }

    setIsSubmitting(true)
    try {
      const user = await register({
        full_name: fullName.trim(),
        email: email.trim(),
        password,
        role,
        phone: phone.trim() || null,
      })

      if (user.role === 'LANDLORD') {
        navigate(ROUTES.LANDLORD_DASHBOARD, { replace: true })
      } else {
        navigate(ROUTES.STUDENT_DASHBOARD, { replace: true })
      }
    } catch (err) {
      setFormError(err.message || 'Registration failed. Please check your details.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="max-w-lg mx-auto px-4 py-12 sm:py-16">
      <Card>
        <CardHeader className="text-center space-y-1">
          <CardTitle>Create your NestMatch account</CardTitle>
          <CardDescription>
            Join students and landlords across universities in India.
          </CardDescription>
        </CardHeader>

        <CardContent>
          {formError && (
            <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-danger text-sm">
              {formError}
            </div>
          )}

          <div className="mb-6">
            <label className="text-sm font-medium text-neutral-600 block mb-2">
              I want to join as:
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setRole('STUDENT')}
                className={cn(
                  'flex items-center gap-3 p-3 rounded-xl border text-left transition-all',
                  role === 'STUDENT'
                    ? 'border-primary bg-primary-light/40 ring-1 ring-primary'
                    : 'border-neutral-200 hover:bg-neutral-50'
                )}
              >
                <div className={cn(
                  'w-8 h-8 rounded-lg flex items-center justify-center shrink-0',
                  role === 'STUDENT' ? 'bg-primary text-white' : 'bg-neutral-100 text-neutral-600'
                )}>
                  <GraduationCap className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-sm font-semibold text-neutral-900">Student</div>
                  <div className="text-xs text-neutral-500">Find room or flatmate</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setRole('LANDLORD')}
                className={cn(
                  'flex items-center gap-3 p-3 rounded-xl border text-left transition-all',
                  role === 'LANDLORD'
                    ? 'border-primary bg-primary-light/40 ring-1 ring-primary'
                    : 'border-neutral-200 hover:bg-neutral-50'
                )}
              >
                <div className={cn(
                  'w-8 h-8 rounded-lg flex items-center justify-center shrink-0',
                  role === 'LANDLORD' ? 'bg-primary text-white' : 'bg-neutral-100 text-neutral-600'
                )}>
                  <Building2 className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-sm font-semibold text-neutral-900">Landlord</div>
                  <div className="text-xs text-neutral-500">List accommodation</div>
                </div>
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Full name"
              type="text"
              placeholder="e.g. Aanya Sharma"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />

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
              placeholder="At least 6 characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <Input
              label="Mobile phone number (optional)"
              type="tel"
              placeholder="+91 98765 43210"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />

            <Button
              type="submit"
              variant="primary"
              size="md"
              fullWidth
              isLoading={isSubmitting}
            >
              Create account
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-neutral-600">
            Already have an account?{' '}
            <Link to={ROUTES.LOGIN} className="text-primary font-medium hover:underline">
              Sign in
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
