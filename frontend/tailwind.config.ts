// tailwind.config.ts
import type { Config } from 'tailwindcss';
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import aspectRatio from '@tailwindcss/aspect-ratio';
import lineClamp from '@tailwindcss/line-clamp';

const config: Config = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx,css}'], // Included 'css' to cover global styles
  theme: {
    extend: {
      // 1. Simplified Custom Colors
      colors: {
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
          950: '#1e1b4b',
        },
        accent: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        techblue: {
          500: '#3b82f6', // Define if not already present
        },
      },

      // 2. Updated Box Shadows Aligned with 'accent'
      boxShadow: {
        'accent-light': '0 2px 4px rgba(20, 184, 166, 0.1)',
        'accent-dark': '0 4px 6px rgba(20, 184, 166, 0.2)',
        'accent-glow': '0 0 10px rgba(20, 184, 166, 0.3)',
      },
      // 3. Custom Animations
      animation: {
        'gradient-x': 'gradient-x 5s ease infinite',
        'fade-in': 'fade-in 1s ease-out forwards',
        'fade-out': 'fade-out 1s ease-in forwards',
        'slide-down': 'slide-down 0.5s ease-out forwards',
        'slide-up': 'slide-up 0.5s ease-in forwards',
      },

      // 4. Custom Keyframes
      keyframes: {
        'gradient-x': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(-10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-out': {
          '0%': { opacity: '1', transform: 'translateY(0)' },
          '100%': { opacity: '0', transform: 'translateY(-10px)' },
        },
        'slide-down': {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(0)' },
        },
        'slide-up': {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(-100%)' },
        },
      },

      // 5. Custom Font Families
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        serif: ['Merriweather', 'serif'],
        mono: ['Fira Code', 'monospace'],
      },

      // 6. Custom Spacing
      spacing: {
        '128': '32rem',
        '144': '36rem',
        '1/7': '14.2857143%',
        '2/7': '28.5714286%',
        '3/7': '42.8571429%',
        '4/7': '57.1428571%',
        '5/7': '71.4285714%',
        '6/7': '85.7142857%',
      },

      // 7. Custom Sizes
      maxWidth: {
        '8xl': '90rem',
      },
      minHeight: {
        'screen-75': '75vh',
      },

      // 8. Custom Border Radius
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },

      // 9. Custom Transition Timing Functions
      transitionTimingFunction: {
        'in-expo': 'cubic-bezier(0.95, 0.05, 0.795, 0.035)',
        'out-expo': 'cubic-bezier(0.19, 1, 0.22, 1)',
      },

      // 10. Background Gradients for Text Animation
      backgroundImage: {
        'gradient-rainbow': 'linear-gradient(270deg, #14b8a6, #6366f1, #14b8a6)',
      },
    },
  },
  plugins: [
    forms,
    typography,
    aspectRatio,
    lineClamp,
  ],
};

export default config;
