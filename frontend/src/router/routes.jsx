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
import { SearchResults } from '../pages/listings/SearchResults'
import { ListingDetail } from '../pages/listings/ListingDetail'
import { CreateListing } from '../pages/landlord/CreateListing'
import { MyListings } from '../pages/landlord/MyListings'
import { Chat } from '../pages/messages/Chat'
import { StudentBookings } from '../pages/bookings/StudentBookings'
import { LandlordBookings } from '../pages/landlord/LandlordBookings'
import { BrowseFlatmates } from '../pages/flatmates/BrowseFlatmates'
import { MyFlatmateProfile } from '../pages/flatmates/MyFlatmateProfile'
import { SavedListings } from '../pages/saved/SavedListings'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path={ROUTES.LOGIN} element={<Login />} />
        <Route path={ROUTES.REGISTER} element={<Register />} />
        <Route path={ROUTES.SEARCH} element={<SearchResults />} />
        <Route path={ROUTES.LISTING_DETAIL} element={<ListingDetail />} />
        <Route path={ROUTES.FLATMATES} element={<BrowseFlatmates />} />


        {/* Protected Messaging Routes */}
        <Route
          path={ROUTES.MESSAGES}
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />
        <Route
          path={`${ROUTES.MESSAGES}/:conversationId`}
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.INBOX}
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />

        {/* Protected Student Routes */}
        <Route
          path={ROUTES.STUDENT_DASHBOARD}
          element={
            <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
              <StudentDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.STUDENT_BOOKINGS}
          element={
            <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
              <StudentBookings />
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.SAVED_LISTINGS}
          element={
            <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
              <SavedListings />
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.MY_FLATMATE_PROFILE}
          element={
            <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
              <MyFlatmateProfile />
            </ProtectedRoute>
          }
        />


        {/* Protected Landlord Routes */}
        <Route
          path={ROUTES.LANDLORD_DASHBOARD}
          element={
            <ProtectedRoute allowedRoles={['LANDLORD', 'ADMIN']}>
              <LandlordDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.CREATE_LISTING}
          element={
            <ProtectedRoute allowedRoles={['LANDLORD', 'ADMIN']}>
              <CreateListing />
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.MY_LISTINGS}
          element={
            <ProtectedRoute allowedRoles={['LANDLORD', 'ADMIN']}>
              <MyListings />
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.LANDLORD_BOOKINGS}
          element={
            <ProtectedRoute allowedRoles={['LANDLORD', 'ADMIN']}>
              <LandlordBookings />
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
