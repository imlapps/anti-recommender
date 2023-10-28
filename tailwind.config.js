/** @type {import('tailwindcss').Config} */

module.exports = {
  theme: {
    extend: {
      colors: {
        "custom-gray": "#222222",
        "custom-black-1": "#1B1B1D",
        "custom-black-2": "#121212",
        "custom-pink": "#FF6CC9",
      },
      backgroundImage: {
        "radial-gradient":
          "radial-gradient(circle at 10% 20%, rgb(10, 10, 10) 0%, rgb(34,34,34) 90.2%)",
      },
      height: {
        112: "28rem",
        120: "30rem",
        128: "32rem",
        144: "36rem",
        160: "40rem",
      },
    },
  },
  variants: [],
  plugins: [],
};
