import React from 'react'
import { Loader2 } from 'lucide-react'
import { cn } from '../../lib/utils'

export const Button = React.forwardRef(
  (
    {
      children,
      className,
      variant = 'primary',
      size = 'md',
      isLoading = false,
      disabled = false,
      fullWidth = false,
      type = 'button',
      ...props
    },
    ref
  ) => {
    const variants = {
      primary: 'bg-primary text-white hover:bg-primary-dark active:bg-primary-dark',
      secondary: 'bg-white border border-neutral-200 text-neutral-800 hover:bg-neutral-50 active:bg-neutral-100',
      ghost: 'bg-transparent text-neutral-800 hover:bg-neutral-100 active:bg-neutral-200',
      danger: 'bg-danger text-white hover:bg-red-700 active:bg-red-800',
    }

    const sizes = {
      sm: 'h-8 px-3 text-sm rounded-lg',
      md: 'h-10 px-4 text-base rounded-lg',
      lg: 'h-12 px-6 text-base rounded-xl font-medium',
    }

    return (
      <button
        ref={ref}
        type={type}
        disabled={disabled || isLoading}
        className={cn(
          'inline-flex items-center justify-center gap-2 font-medium transition-colors focus-visible:outline-none disabled:opacity-50 disabled:cursor-not-allowed',
          variants[variant] || variants.primary,
          sizes[size] || sizes.md,
          fullWidth && 'w-full',
          className
        )}
        {...props}
      >
        {isLoading && <Loader2 className="w-4 h-4 animate-spin shrink-0 text-currentColor" />}
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
