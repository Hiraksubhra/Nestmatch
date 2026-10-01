/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50:      '#EFF6FF',
          100:     '#DBEAFE',
          200:     '#BFDBFE',
          300:     '#93C5FD',
          400:     '#60A5FA',
          500:     '#3B82F6',
          600:     '#2563EB',
          700:     '#1D4ED8',
          800:     '#1E40AF',
          900:     '#1E3A8A',
          DEFAULT: '#2563EB',
          dark:    '#1D4ED8',
          light:   '#DBEAFE',
        },
        accent: {
          DEFAULT: '#F59E0B',
          light:   '#FEF3C7',
          dark:    '#B45309',
        },
        success: '#16A34A',
        danger:  '#DC2626',
        warning: '#D97706',
        neutral: {
          50:  '#F9FAFB',
          100: '#F3F4F6',
          200: '#E5E7EB',
          400: '#9CA3AF',
          600: '#4B5563',
          800: '#1F2937',
          900: '#111827',
        },
      },
      fontFamily: {
        sans:    ['"Inter"', 'system-ui', 'sans-serif'],
        heading: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', 'monospace'],
      },
      fontSize: {
        'display': ['3.5rem',  { lineHeight: '1.1', fontWeight: '700' }],
        'h1':      ['2.25rem', { lineHeight: '1.2', fontWeight: '600' }],
        'h2':      ['1.75rem', { lineHeight: '1.3', fontWeight: '600' }],
        'h3':      ['1.375rem',{ lineHeight: '1.35',fontWeight: '600' }],
        'h4':      ['1.125rem',{ lineHeight: '1.4', fontWeight: '600' }],
      },
      borderRadius: {
        'xl':  '12px',
        '2xl': '16px',
        '3xl': '24px',
      },
      boxShadow: {
        'card':       '0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06)',
        'card-hover': '0 4px 12px rgba(0,0,0,0.12), 0 2px 4px rgba(0,0,0,0.08)',
        'modal':      '0 20px 60px rgba(0,0,0,0.15)',
      },
      maxWidth: {
        'content': '1280px',
      },
    },
  },
  plugins: [],
}
