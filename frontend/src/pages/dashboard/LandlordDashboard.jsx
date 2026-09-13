import React from 'react'
import { Link } from 'react-router-dom'
import { PlusCircle, Building2, MessageSquare, Eye } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../constants/routes'
import { Button } from '../../components/ui/Button'
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'

export const LandlordDashboard = () => {
  const { user } = useAuthStore()

  return (
    <div className="max-w-content mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Header Profile Summary */}
      <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-primary-light text-primary font-bold text-xl flex items-center justify-center">
            {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'L'}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-heading font-semibold text-neutral-900">{user?.full_name}</h1>
              <Badge variant="type">Landlord</Badge>
              {user?.is_verified && <Badge variant="verified" showIcon>Verified</Badge>}
            </div>
            <p className="text-sm text-neutral-600 mt-0.5">{user?.email}</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Link to={ROUTES.HOME}>
            <Button variant="primary" size="md">
              <PlusCircle className="w-4 h-4 mr-1.5" />
              Post new listing
            </Button>
          </Link>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-base font-medium text-neutral-600">Active Listings</CardTitle>
            <Building2 className="w-5 h-5 text-neutral-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-neutral-900">0</div>
            <p className="text-xs text-neutral-500 mt-1">Live properties on NestMatch</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-base font-medium text-neutral-600">Student Inquiries</CardTitle>
            <MessageSquare className="w-5 h-5 text-neutral-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-neutral-900">0</div>
            <p className="text-xs text-neutral-500 mt-1">Messages from interested students</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-base font-medium text-neutral-600">Total Views</CardTitle>
            <Eye className="w-5 h-5 text-neutral-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-neutral-900">0</div>
            <p className="text-xs text-neutral-500 mt-1">Listing impressions this month</p>
          </CardContent>
        </Card>
      </div>

      {/* Listings Section Placeholder */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>My Listings</CardTitle>
          <span className="text-xs text-neutral-400">Sprint 1 Feature</span>
        </CardHeader>
        <CardContent className="text-center py-12 space-y-3">
          <div className="w-12 h-12 rounded-full bg-neutral-100 mx-auto flex items-center justify-center text-neutral-400">
            <Building2 className="w-6 h-6" />
          </div>
          <h3 className="text-base font-heading font-semibold text-neutral-800">No listings posted yet</h3>
          <p className="text-sm text-neutral-500 max-w-sm mx-auto">
            You can publish your rental rooms and apartments once the Listing Wizard is activated in Sprint 1.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
