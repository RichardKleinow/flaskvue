import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', name: 'Home', component: 'Home' },
  { path: '/Motorcontrol', name: 'BC9000', component: 'BC9000' },
  { path: '/about', component: 'About' },
  { path: '*', component: 'NotFound' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`),
    props: {default: true, Home: false}
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})
