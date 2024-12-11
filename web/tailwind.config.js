/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{vue,jsx}"],
  theme: {
    extend: {
      colors: {
        azul: "#133E78",
        laranja: "#F59E0B",
        verde: "#008940",
        cinza1: "#F3F4F6",
        cinza2: "#D9D9D9",
        cinza3: "#8899a8",
      },
      fontFamily: {
        inter: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
