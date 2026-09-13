import React, { useEffect } from 'react'
import { BrowserRouter } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import { AppRoutes } from './router/routes'

function App() {
  const initAuth = useAuthStore((state) => state.initAuth)

  useEffect(() => {
    initAuth()
  }, [initAuth])

  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  )
}

export default App
