module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  safelist: [
    'bg-blue-500', 'bg-blue-600', 'bg-blue-700', 'bg-blue-50', 'bg-blue-100',
    'text-blue-700', 'text-blue-800', 'text-blue-600',
    'border-blue-500', 'border-blue-300', 'border-blue-200',
    'bg-gradient-to-r', 'from-blue-500', 'to-cyan-500',
    'hover:bg-blue-600', 'hover:bg-blue-700', 'hover:bg-cyan-200',
    'bg-cyan-50', 'bg-cyan-100', 'text-cyan-700', 'border-cyan-300',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb', // blue-600
          light: '#3b82f6',   // blue-500
          dark: '#1e40af',    // blue-800
        },
        accent: {
          DEFAULT: '#06b6d4', // cyan-500
          light: '#67e8f9',   // cyan-300
        },
      },
    },
  },
  plugins: [],
}; 