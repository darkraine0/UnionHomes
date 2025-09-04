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
    'bg-red-500', 'border-red-600',
    'bg-green-500', 'border-green-600',
    'bg-orange-500', 'border-orange-600',
    'bg-purple-500', 'border-purple-600',
    'bg-amber-500', 'border-amber-600',
    'bg-emerald-500', 'border-emerald-600',
    'bg-pink-500', 'bg-pink-600', 'border-pink-500', 'border-pink-600',
    'bg-pink-50', 'text-pink-700', 'hover:bg-pink-100',
    'bg-purple-500', 'bg-purple-600', 'border-purple-500', 'border-purple-600',
    'bg-gray-500', 'bg-gray-600', 'border-gray-500', 'border-gray-600',
    'bg-lime-500', 'bg-lime-600', 'border-lime-500', 'border-lime-600',
    'bg-lime-50', 'text-lime-700', 'hover:bg-lime-100',
    'bg-cyan-500', 'bg-cyan-600', 'border-cyan-500', 'border-cyan-600',
    'bg-teal-500', 'bg-teal-600', 'border-teal-500', 'border-teal-600',
    'bg-teal-50', 'text-teal-700', 'hover:bg-teal-100',
    'bg-slate-500', 'bg-slate-600', 'border-slate-500', 'border-slate-600',
    'bg-slate-50', 'text-slate-700', 'hover:bg-slate-100',
    'bg-fuchsia-500', 'bg-fuchsia-600', 'border-fuchsia-500', 'border-fuchsia-600',
    'bg-fuchsia-50', 'text-fuchsia-700', 'hover:bg-fuchsia-100',
    'bg-rose-500', 'bg-rose-600', 'border-rose-500', 'border-rose-600',
    'bg-rose-50', 'text-rose-700', 'hover:bg-rose-100',
    'bg-sky-500', 'bg-sky-600', 'border-sky-500', 'border-sky-600',
    'bg-sky-50', 'text-sky-700', 'hover:bg-sky-100',
    'bg-yellow-500', 'bg-yellow-600', 'border-yellow-500', 'border-yellow-600',
    'bg-yellow-50', 'text-yellow-700', 'hover:bg-yellow-100',
    'bg-stone-500', 'bg-stone-600', 'border-stone-500', 'border-stone-600',
    'bg-stone-50', 'text-stone-700', 'hover:bg-stone-100',
    'bg-violet-500', 'bg-violet-600', 'border-violet-500', 'border-violet-600',
    'bg-violet-50', 'text-violet-700', 'hover:bg-violet-100',
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