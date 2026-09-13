import React from 'react'
import { Link } from 'react-router-dom'
import { Search, Users, Bookmark, MessageSquare, CheckCircle2 } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../constants/routes'
import { Button } from '../../components/ui/Button'
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'

export const StudentDashboard = () => {
  const { user } = useAuthStore()

  return (
    <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Header Profile Summary */}
      <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-primary-light text-primary font-bold text-xl flex items-center justify-center">
            {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'S'}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-heading font-semibold text-neutral-900">{user?.full_name}</h1>
              <Badge variant="default">Student</Badge>
              {user?.is_verified && <Badge variant="verified" showIcon>Verified</Badge>}
            </div>
            <p className="text-sm text-neutral-600 mt-0.5">{user?.email}</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Link to={ROUTES.HOME}>
            <Button variant="primary" size="md">
              <Search className="w-4 h-4 mr-1.5" />
              Find rooms
            </Button>
          </Link>
          <Link to={ROUTES.FLATMATES}>
            <Button variant="secondary" size="md">
              <Users className="w-4 h-4 mr-1.5" />
              Match flatmates
            </Button>
          </Link>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-base font-medium text-neutral-600">Active Inquiries</CardTitle>
            <MessageSquare className="w-5 h-5 text-neutral-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-neutral-900">0</div>
            <p className="text-xs text-neutral-500 mt-1">Inquiries sent to landlords</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-base font-medium text-neutral-600">Saved Listings</CardTitle>
            <Bookmark className="w-5 h-5 text-neutral-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-neutral-900">0</div>
            <p className="text-xs text-neutral-500 mt-1">Bookmarked accommodations</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-base font-medium text-neutral-600">Flatmate Profile</CardTitle>
            <Users className="w-5 h-5 text-neutral-400" />
          </CardHeader>
          <CardContent>
            <div className="text-sm font-semibold text-warning">Pending creation</div>
            <p className="text-xs text-neutral-500 mt-1">Setup lifestyle & budget tags</p>
          </CardContent>
        </Card>
      </div>

      {/* Next Steps Checklist */}
      <Card>
        <CardHeader>
          <CardTitle>Getting started with your search</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-start gap-3 p-3 bg-neutral-50 rounded-lg">
            <CheckCircle2 className="w-5 h-5 text-success shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-semibold text-neutral-900">Account created</h4>
              <p className="text-xs text-neutral-600">Your student account has been registered with NestMatch.</p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 bg-neutral-50 rounded-lg">
            <div className="w-5 h-5 rounded-full border-2 border-neutral-300 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-semibold text-neutral-900">Complete flatmate profile</h4>
              <p className="text-xs text-neutral-600">Set your university, monthly budget, and lifestyle habits.</p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 bg-neutral-50 rounded-lg">
            <div className="w-5 h-5 rounded-full border-2 border-neutral-300 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-semibold text-neutral-900">Explore campus listings</h4>
              <p className="text-xs text-neutral-600">Browse verified listings within walking distance of your campus.</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
