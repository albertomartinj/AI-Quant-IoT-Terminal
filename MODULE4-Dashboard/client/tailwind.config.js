/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dark theme background and surfaces
        darkBg: '#0f172a',    // Very dark blue/black
        darkSurface: '#1e293b', // Slightly lighter for cards
        
        // Critical alerts (High Contrast for HCI)
        alertRed: '#ef4444',
        alertText: '#f87171',
        
        // Positive sentiment
        bullishGreen: '#22c55e',
      }
    },
  },
  plugins: [],
}
