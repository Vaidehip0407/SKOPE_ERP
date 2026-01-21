/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1D3557',
          light: '#457B9D',
          dark: '#0D1B2A',
        },
        secondary: {
          DEFAULT: '#A8DADC',
          light: '#F1FAEE',
        },
        accent: {
          DEFAULT: '#E63946',
          light: '#F77F88',
        },
        neutral: {
          50: '#F8F9FA',
          100: '#F1FAEE',
          200: '#E9ECEF',
          300: '#DEE2E6',
          400: '#CED4DA',
          500: '#ADB5BD',
          600: '#6C757D',
          700: '#495057',
          800: '#343A40',
          900: '#212529',
        },
      },
      boxShadow: {
        '3xl': '0 35px 60px -15px rgba(0, 0, 0, 0.3)',
      },
    },
  },
  plugins: [],
}

