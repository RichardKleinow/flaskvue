// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'

// const options = { path: '/api/' }

Vue.use(
  new VueSocketIO({
    debug: true,
    connection: SocketIO('http://localhost:5000') //, options)
  })
)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
