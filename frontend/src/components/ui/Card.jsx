import React from 'react'
import { cn } from '../../lib/utils'

export const Card = ({ children, className, hover = false, ...props }) => {
  return (
    <div
      className={cn(
        'bg-white rounded-xl border border-neutral-200 shadow-card overflow-hidden',
        hover && 'hover:shadow-card-hover transition-shadow duration-200',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

export const CardHeader = ({ children, className, ...props }) => {
  return (
    <div className={cn('p-6 border-b border-neutral-100', className)} {...props}>
      {children}
    </div>
  )
}

export const CardTitle = ({ children, className, ...props }) => {
  return (
    <h3 className={cn('text-h3 font-heading text-neutral-900', className)} {...props}>
      {children}
    </h3>
  )
}

export const CardDescription = ({ children, className, ...props }) => {
  return (
    <p className={cn('text-sm text-neutral-600 mt-1', className)} {...props}>
      {children}
    </p>
  )
}

export const CardContent = ({ children, className, ...props }) => {
  return (
    <div className={cn('p-6', className)} {...props}>
      {children}
    </div>
  )
}

export const CardFooter = ({ children, className, ...props }) => {
  return (
    <div className={cn('p-4 border-t border-neutral-100 bg-neutral-50/50', className)} {...props}>
      {children}
    </div>
  )
}
