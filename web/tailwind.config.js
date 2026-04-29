/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ivory:    { DEFAULT: '#F5F0E7', light: '#FFFCF5' },
        forest:   { DEFAULT: '#156B49', light: '#3A8C62', dark: '#0E4F36' },
        graphite: { DEFAULT: '#1C2B24', muted: '#4A6359', subtle: '#8BA898' },
        amber:    '#BD6E1B',
        danger:   '#BD3A33',
        ink:      '#17201A',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
