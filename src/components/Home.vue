<template>
<div>
   <head class="flex justify-center">
             <router-link to="/">
            <img src=".././assets/logo.svg" alt=".././assets/logo.png" id="logo_wait">
        </router-link>
    </head>
  <p class="justify-center mt-4">Scanning for Devices... {{ this.ScanningState }}</p>
</div>
</template>

<script>
export default {
  data () {
    return {
      device_type: '',
      ScanningState: ''
    }
  },
  mounted: function () {
    this.intdevtype = window.setInterval(() => {
      this.getDeviceType()
      this.getScanProgress()
    }, 2000)
    this.intdevroute = window.setInterval(() => {
      this.RouteToDevice()
    }, 3000)
  },
  methods: {
    getDeviceType () {
      console.log('Querying for Device Type')
      this.$socket.emit('req_DeviceType', (type) => {
        this.device_type = type
        console.log('returned type ' + type)
      })
    },
    getScanProgress () {
      this.$socket.emit('req_ScanProgress', (progress) => {
        this.ScanningState = progress
      })
    },
    RouteToDevice () {
      console.log('Evaluate received Device Type')
      if (this.device_type !== '') {
        console.log('Routing to ' + this.device_type)
        window.clearInterval(this.intdevtype)
        window.clearInterval(this.intdevroute)
        this.$router.push({ name: this.device_type }, () => {})
      } else {
        console.log('No Device Type received')
      }
    }
  }
}
</script>

<style scoped>

#logo_wait {
    height: 200px;
    width: auto;
    -webkit-animation: v-squareDelay 3s 0s infinite;
    animation: v-squareDelay 3s 0s infinite;
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
    perspective: 100px;
    display: inline-block;
}

@-webkit-keyframes v-squareDelay {
    25% {
        -webkit-transform: rotateX(180deg) rotateY(0);
        transform: rotateX(180deg) rotateY(0);
    }

    50% {
        -webkit-transform: rotateX(180deg) rotateY(180deg);
        transform: rotateX(180deg) rotateY(180deg);
    }

    75% {
        -webkit-transform: rotateX(0) rotateY(180deg);
        transform: rotateX(0) rotateY(180deg);
    }

    100% {
        -webkit-transform: rotateX(0) rotateY(0);
        transform: rotateX(0) rotateY(0);
    }
}

@keyframes v-squareDelay {
    25% {
        -webkit-transform: rotateX(180deg) rotateY(0);
        transform: rotateX(180deg) rotateY(0);
    }

    50% {
        -webkit-transform: rotateX(180deg) rotateY(180deg);
        transform: rotateX(180deg) rotateY(180deg);
    }

    75% {
        -webkit-transform: rotateX(0) rotateY(180deg);
        transform: rotateX(0) rotateY(180deg);
    }

    100% {
        -webkit-transform: rotateX(0) rotateY(0);
        transform: rotateX(0) rotateY(0);
    }
}
</style>
