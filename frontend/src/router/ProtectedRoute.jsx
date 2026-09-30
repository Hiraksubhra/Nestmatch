import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { ROUTES } from '../constants/routes'
import { Loader2 } from 'lucide-react'

export const ProtectedRoute = ({ children, allowedRoles }) => {
  const { isAuthenticated, isLoading, user } = useAuthStore()
  const location = useLocation()

  if (isLoading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
        <p className="text-sm text-neutral-600">Checking authorization...</p>
      </div>
    )
  }

  if (!isAuthenticated || !user) {
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return (
      <div className="max-w-md mx-auto my-16 p-8 bg-white rounded-xl border border-neutral-200 text-center">
        <h2 className="text-xl font-heading font-semibold text-neutral-900 mb-2">Access restricted</h2>
        <p className="text-sm text-neutral-600 mb-6">
          You need an authorized role ({allowedRoles.join(', ')}) to view this section.
        </p>
        <Navigate to={user.role === 'LANDLORD' ? ROUTES.LANDLORD_DASHBOARD : ROUTES.STUDENT_DASHBOARD} replace />
      </div>
    )
  }

  return children
}
