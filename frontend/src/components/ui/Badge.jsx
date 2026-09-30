import React from 'react'
import { BadgeCheck } from 'lucide-react'
import { cn } from '../../lib/utils'

export const Badge = ({
  children,
  variant = 'default',
  className,
  showIcon = false,
  ...props
}) => {
  const variants = {
    default: 'bg-neutral-100 text-neutral-600',
    verified: 'bg-accent-light text-amber-700',
    active: 'bg-green-50 text-success',
    pending: 'bg-yellow-50 text-warning',
    inactive: 'bg-neutral-100 text-neutral-400',
    type: 'bg-primary-light text-primary',
  }

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full font-medium',
        variants[variant] || variants.default,
        className
      )}
      {...props}
    >
      {variant === 'verified' && showIcon && <BadgeCheck className="w-3.5 h-3.5 text-amber-600" />}
      {children}
    </span>
  )
}
