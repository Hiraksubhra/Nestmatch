import { create } from 'zustand'
import { authService } from '../services/auth'

export const useAuthStore = create((set, get) => ({
  user: null,
  accessToken: localStorage.getItem('access_token') || null,
  refreshToken: localStorage.getItem('refresh_token') || null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  isLoading: true,
  error: null,

  setTokens: (accessToken, refreshToken) => {
    if (accessToken) localStorage.setItem('access_token', accessToken)
    else localStorage.removeItem('access_token')

    if (refreshToken) localStorage.setItem('refresh_token', refreshToken)
    else localStorage.removeItem('refresh_token')

    set({
      accessToken,
      refreshToken,
      isAuthenticated: !!accessToken,
    })
  },

  setUser: (user) => set({ user }),

  login: async (credentials) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.login(credentials)
      const { access_token, refresh_token, user } = response.data
      get().setTokens(access_token, refresh_token)
      set({ user, isLoading: false, isAuthenticated: true })
      return user
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  register: async (userData) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.register(userData)
      const { access_token, refresh_token, user } = response.data
      get().setTokens(access_token, refresh_token)
      set({ user, isLoading: false, isAuthenticated: true })
      return user
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  logout: async () => {
    try {
      await authService.logout()
    } catch {
      // Ignore API failure on logout
    } finally {
      get().setTokens(null, null)
      set({ user: null, isAuthenticated: false, isLoading: false, error: null })
    }
  },

  initAuth: async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      set({ isLoading: false, isAuthenticated: false, user: null })
      return
    }

    try {
      const response = await authService.getMe()
      set({ user: response.data, isAuthenticated: true, isLoading: false })
    } catch {
      // If fetching user profile fails, clear tokens
      get().setTokens(null, null)
      set({ user: null, isAuthenticated: false, isLoading: false })
    }
  },
}))
