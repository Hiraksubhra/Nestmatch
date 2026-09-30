import React, { useId } from 'react'
import { cn } from '../../lib/utils'

export const Input = React.forwardRef(
  (
    {
      label,
      error,
      id,
      className,
      type = 'text',
      helperText,
      ...props
    },
    ref
  ) => {
    const generatedId = useId()
    const inputId = id || generatedId

    return (
      <div className="w-full flex flex-col">
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium text-neutral-600 mb-1"
          >
            {label}
          </label>
        )}
        <input
          id={inputId}
          ref={ref}
          type={type}
          className={cn(
            'h-10 px-3 rounded-lg border border-neutral-200 bg-white text-neutral-800 placeholder:text-neutral-400 transition-all text-base focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary disabled:bg-neutral-100 disabled:cursor-not-allowed',
            error && 'border-danger focus:ring-danger/30 focus:border-danger',
            className
          )}
          {...props}
        />
        {error ? (
          <p className="text-danger text-sm mt-1">{error}</p>
        ) : helperText ? (
          <p className="text-neutral-400 text-xs mt-1">{helperText}</p>
        ) : null}
      </div>
    )
  }
)

Input.displayName = 'Input'
