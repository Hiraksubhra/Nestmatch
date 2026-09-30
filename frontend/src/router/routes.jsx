import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { ROUTES } from '../constants/routes'
import { Layout } from '../components/layout/Layout'
import { ProtectedRoute } from './ProtectedRoute'
import { Home } from '../pages/Home'
import { Login } from '../pages/auth/Login'
import { Register } from '../pages/auth/Register'
import { StudentDashboard } from '../pages/dashboard/StudentDashboard'
import { LandlordDashboard } from '../pages/dashboard/LandlordDashboard'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path={ROUTES.LOGIN} element={<Login />} />
        <Route path={ROUTES.REGISTER} element={<Register />} />

        {/* Protected Student Dashboard */}
        <Route
          path={ROUTES.STUDENT_DASHBOARD}
          element={
            <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
              <StudentDashboard />
            </ProtectedRoute>
          }
        />

        {/* Protected Landlord Dashboard */}
        <Route
          path={ROUTES.LANDLORD_DASHBOARD}
          element={
            <ProtectedRoute allowedRoles={['LANDLORD', 'ADMIN']}>
              <LandlordDashboard />
            </ProtectedRoute>
          }
        />

        {/* 404 Catch-all */}
        <Route
          path="*"
          element={
            <div className="max-w-md mx-auto my-20 p-8 bg-white rounded-xl border border-neutral-200 text-center">
              <h1 className="text-3xl font-heading font-bold text-neutral-900 mb-2">404</h1>
              <p className="text-neutral-600 mb-6">We couldn't find the page you were looking for.</p>
              <a href={ROUTES.HOME} className="text-primary font-medium hover:underline">
                Return home
              </a>
            </div>
          }
        />
      </Route>
    </Routes>
  )
}
