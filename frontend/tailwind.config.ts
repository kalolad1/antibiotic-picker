import type { Config } from 'tailwindcss'
const defaultTheme = require('tailwindcss/defaultTheme');

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      colors: {
        'light-blue': '#8ecae6',
        'dark-blue': '#023047',
        'black': '#051d24',
        'light-orange': '#ffb703',
        'dark-orange': '#fb8500'
      },
      fontFamily: {
        'merriweather': ['Merriweather', defaultTheme.fontFamily.serif],
        'karla': ['Karla', defaultTheme.fontFamily.sans]
      },
    },
  },
  plugins: [],
}
export default config
