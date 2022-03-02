module.exports = {
  purge: {
    enabled: process.env.PURGE_CSS === 'production' ? true : false,
    content: [
    './public/**/*.html',
    './src/**/*.vue',
    './assets/tailwindsettings.js',
    'node_modules/vue-tailwind/dist/*.js'
    ],
  },
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
  plugins: [
    require('@tailwindcss/forms')
  ],
}
