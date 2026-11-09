/** @type {import('tailwindcss').Config} */
// Colours are declared only as CSS variables in src/index.css. Tailwind maps
// semantic names onto them here, so `bg-card` / `text-muted-foreground` work
// identically in light and dark mode and no component holds a raw hex.
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
      },
      colors: {
        primary: {
          DEFAULT: 'var(--color-primary)',
          hover: 'var(--color-primary-hover)',
        },
        'on-primary': 'var(--color-on-primary)',
        secondary: 'var(--color-secondary)',
        accent: {
          DEFAULT: 'var(--color-accent)',
          hover: 'var(--color-accent-hover)',
        },
        'on-accent': 'var(--color-on-accent)',
        background: 'var(--color-background)',
        foreground: 'var(--color-foreground)',
        card: {
          DEFAULT: 'var(--color-card)',
          foreground: 'var(--color-card-foreground)',
        },
        muted: {
          DEFAULT: 'var(--color-muted)',
          foreground: 'var(--color-muted-foreground)',
        },
        border: 'var(--color-border)',
        success: 'var(--color-success)',
        warning: 'var(--color-warning)',
        destructive: {
          DEFAULT: 'var(--color-destructive)',
          foreground: 'var(--color-on-destructive)',
        },
        ring: 'var(--color-ring)',
      },
      borderRadius: {
        xl: '0.875rem',
        '2xl': '1.25rem',
      },
      spacing: {
        // Density 6/10 — standard 16-64px rhythm.
        section: '4rem',
      },
      keyframes: {
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
      },
      animation: {
        // 300-450ms band from the motion tier; no single global duration.
        'fade-in-up': 'fade-in-up 400ms cubic-bezier(0.22, 1, 0.36, 1) both',
        'fade-in': 'fade-in 250ms ease-out both',
        shimmer: 'shimmer 1.6s infinite',
      },
      transitionDuration: {
        200: '200ms',
      },
    },
  },
  plugins: [],
};
