module.exports = {
  purge: [
    './public/**/*.html',
    './src/**/*.vue',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    container: {
      center : true
    },
    extend: {
      colors: {
        'desy-blue': '#00A6EB',
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
