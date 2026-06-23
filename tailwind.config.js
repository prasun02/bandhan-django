module.exports = {
  content: ["./templates/**/*.html", "./**/templates/**/*.html", "./**/*.py"],
  theme: {
    extend: {
      colors: {
        burgundy: "#7A1F3D",
        "dark-burgundy": "#5D1730",
        rose: "#B85C76",
        gold: "#C79A45",
        "dark-gold": "#9A702E",
        ivory: "#FFF9F5",
        "soft-cream": "#F8EDE8",
        blush: "#F8EDE8",
        "warm-white": "#FFFCFA",
        charcoal: "#2B2527",
        grey: "#756A6E",
        border: "#E7D8D1",
        success: "#2F7D5A",
        warning: "#B7791F",
        error: "#B42318",
      },
      boxShadow: {
        soft: "0 12px 30px rgba(43, 37, 39, 0.08)",
      },
      fontFamily: {
        serif: ["Georgia", "Times New Roman", "serif"],
        sans: ["ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
