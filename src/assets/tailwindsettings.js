// CSS Options and Import
import {
  TButton,
  TInput,
  TTag,
  TRadio,
  TSelect,
  TToggle,
  TTable
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
        bigger: 'block md:px-10 md:py-6 text-white bg-desy-blue border border-transparent border border-black shadow-sm rounded hover:bg-blue-600 focus:ring-red-500 font-bold'
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
      fixedClasses: 'pl-3 pr-10 py-2 transition duration-100 ease-in-out border rounded shadow-sm hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-opacity-50 disabled:bg-grey-500 disabled:opacity-50 disabled:cursor-not-allowed',
      classes: 'text-white placeholder-gray-400 bg-desy-blue border-gray-300 focus:border-blue-500'
    }
  },
  'desy-toggle': {
    component: TToggle,
    props: {
      classes: {
        wrapper: 'ring-2 ring-blue-500  bg-gray-100 rounded-full border-2 border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-opacity-50',
        wrapperChecked: 'bg-blue-500 rounded-full focus:ring-2 focus:ring-blue-500',
        wrapperDisabled: 'bg-gray-100 rounded-full border-2 border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-opacity-50',
        wrapperCheckedDisabled: 'bg-blue-500',
        button: 'h-5 w-5 rounded-full bg-white shadow flex items-center justify-center text-gray-400 text-xs',
        buttonChecked: 'h-5 w-5 rounded-full bg-white shadow flex items-center justify-center text-blue-500 text-xs',
        checkedPlaceholder: 'rounded-full w-5 h-5 flex items-center justify-center text-gray-400 text-xs',
        uncheckedPlaceholder: 'rounded-full w-5 h-5 flex items-center justify-center text-gray-400 text-xs'
      }
    }
  },
  'desy-table': {
    component: TTable,
    props: {
      classes: {
        table: 'min-w-full divide-y divide-gray-100 shadow-sm border-gray-200 border',
        thead: '',
        theadTr: '',
        theadTh: 'px-3 py-2 font-semibold text-left bg-gray-100 border-b',
        tbody: 'bg-white divide-y divide-gray-100',
        tr: '',
        td: 'px-3 py-2 whitespace-no-wrap',
        tfoot: '',
        tfootTr: '',
        tfootTd: ''
      }
    }
  }
}

export default settings
