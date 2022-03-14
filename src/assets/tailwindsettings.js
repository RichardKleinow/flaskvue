// CSS Options and Import
import {
  TButton,
  TInput,
  TTag,
  TRadio,
  TSelect
} from 'vue-tailwind/dist/components'

const settings = {
  'desy-button': {
    component: TButton,
    props: {
      fixedClasses: 'block px-4 py-2 transition duration-100 ease-in-out focus:border-blue-500 focus:ring-2 focus:ring-desy-blue focus:outline-none focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed',
      classes: 'text-white bg-desy-blue border border-transparent shadow-sm rounded hover:bg-blue-600 focus:ring-red-500',
      variants: {
        secondary: 'text-gray-800 bg-white border border-gray-300 shadow-sm hover:text-gray-600',
        error: 'text-white bg-red-500 border border-transparent rounded shadow-sm hover:bg-red-600',
        success: 'text-white bg-green-500 border border-transparent rounded shadow-sm hover:bg-green-600',
        link: 'text-blue-500 underline hover:text-blue-600',
        bigger: 'block px-10 py-6 text-white bg-desy-blue border border-transparent shadow-sm rounded hover:bg-blue-600 focus:ring-red-500 font-bold'
      }
    }
  },
  't-input': {
    component: TInput
  },
  't-tag': {
    component: TTag,
    props: {
      fixedClasses: '',
      classes: '',
      variants: {
        radiolabel: 'grid grid-cols-2 place-items-center border border-black bg-gray-100 rounded'
      }
    }
  },
  't-radio': {
    component: TRadio,
    props: {
      classes: 'focus:border-desy-blue focus:border-width-0'
    }
  },
  'desy-select': {
    component: TSelect,
    props: {
      fixedClasses: 'pl-3 pr-10 py-2 transition duration-100 ease-in-out border rounded shadow-sm hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-opacity-50  disabled:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed',
      classes: 'text-white placeholder-gray-400 bg-desy-blue border-gray-300 focus:border-blue-500'
    }
  }
}

export default settings
