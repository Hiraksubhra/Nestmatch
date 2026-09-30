import React from 'react'
import {
  Wifi,
  Wind,
  Utensils,
  Shirt,
  Zap,
  Droplets,
  ShieldCheck,
  Flame,
  Sparkles,
  Car,
  Refrigerator,
  BookOpen,
  Bath,
  Dumbbell,
  CheckCircle2,
} from 'lucide-react'

const ICON_MAP = {
  wifi: Wifi,
  ac: Wind,
  food_included: Utensils,
  mess: Utensils,
  laundry: Shirt,
  power_backup: Zap,
  ro_water: Droplets,
  security: ShieldCheck,
  geyser: Flame,
  housekeeping: Sparkles,
  parking: Car,
  refrigerator: Refrigerator,
  study_desk: BookOpen,
  attached_washroom: Bath,
  gym: Dumbbell,
}

export const AmenityIcon = ({ name, icon, label, size = 16, className = '' }) => {
  const IconComponent = ICON_MAP[name] || ICON_MAP[icon] || CheckCircle2

  return (
    <div className={`inline-flex items-center gap-1.5 text-xs text-neutral-600 bg-neutral-100 px-2.5 py-1 rounded-md ${className}`}>
      <IconComponent size={size} className="text-primary-600 shrink-0" />
      <span>{label || name}</span>
    </div>
  )
}
