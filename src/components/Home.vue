// Home.vue

<template>
  <div id="content" class="flex flex-col justify-center pt-5">
    <h1>Home Page</h1>
    <p>Random Number from Backend: {{ randomNumber }}</p>
    <button @click="getRandom">Random Number Generator</button>
  </div>
</template>

<script>
export default {
  connected: false,
  sockets: {
    connect: function () {
      this.connected = true
      console.log('socketio connected')
    },
    disconnect: function () {
      this.connected = false
      console.log('socket disconnected')
    }
  },
  data () {
    return {
      randomNumber: 0
    }
  },
  methods: {
    getRandom () {
      this.$socket.emit('req_random', (rand) => {
        this.randomNumber = rand
      })
      console.log('Request emmited!')
    }
  }
}
</script>
