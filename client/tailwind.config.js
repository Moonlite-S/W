/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "W": "url('https://gamepress.gg/arknights/sites/arknights/files/2020-12/Ak_avg_ac9_3.png')",
      }
    },
  },
  plugins: [],
}

