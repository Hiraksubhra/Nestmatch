import React, { useEffect } from 'react'
import { X } from 'lucide-react'
import { cn } from '../../lib/utils'

export const Modal = ({
  isOpen,
  onClose,
  title,
  description,
  children,
  className,
}) => {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    if (isOpen) {
      document.body.style.overflow = 'hidden'
      window.addEventListener('keydown', handleKeyDown)
    }

    return () => {
      document.body.style.overflow = 'unset'
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-neutral-900/40 backdrop-blur-sm transition-opacity animate-in fade-in duration-200"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div
        className={cn(
          'relative w-full max-w-md bg-white rounded-xl shadow-modal border border-neutral-200 overflow-hidden',
          className
        )}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              {title && (
                <h3
                  id="modal-title"
                  className="text-lg font-heading font-semibold text-neutral-900"
                >
                  {title}
                </h3>
              )}
              {description && (
                <p className="text-sm text-neutral-600 mt-1">
                  {description}
                </p>
              )}
            </div>
            <button
              type="button"
              onClick={onClose}
              className="p-1 rounded-lg text-neutral-400 hover:text-neutral-600 hover:bg-neutral-100 transition-colors"
              aria-label="Close dialog"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="mt-4">{children}</div>
        </div>
      </div>
    </div>
  )
}
