import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

export const getBackendBaseUrl = () => {
  const apiUrl =
    import.meta.env.VITE_API_BASE_URL ||
    (import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}/api/v1` : 'http://localhost:8000/api/v1')
  return apiUrl.replace(/\/api\/v1\/?$/, '')
}

export const getImageUrl = (url, fallback = '') => {
  if (!url) return fallback
  if (url.startsWith('http://') || url.startsWith('https://')) return url
  const backendBase = getBackendBaseUrl()
  const cleanPath = url.startsWith('/') ? url : `/${url}`
  return `${backendBase}${cleanPath}`
}
