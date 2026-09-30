import React, { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
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
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

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

  if (!isOpen || !mounted) return null

  const modalContent = (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-neutral-900/50 backdrop-blur-md transition-all animate-in fade-in duration-200"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div
        className={cn(
          'relative w-full max-w-md bg-white rounded-2xl shadow-modal border border-neutral-200 p-6 sm:p-7 overflow-hidden transform transition-all animate-in zoom-in-95 duration-200',
          className
        )}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            {title && (
              <h3
                id="modal-title"
                className="text-xl sm:text-2xl font-heading font-semibold text-neutral-900 tracking-tight leading-snug"
              >
                {title}
              </h3>
            )}
            {description && (
              <p className="text-sm text-neutral-600 mt-2">
                {description}
              </p>
            )}
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 rounded-lg text-neutral-400 hover:text-neutral-700 hover:bg-neutral-100 transition-colors shrink-0"
            aria-label="Close dialog"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="mt-6">{children}</div>
      </div>
    </div>
  )

  return createPortal(modalContent, document.body)
}
