<template>
<div>
</div>
</template>

<script>
export default {
  data () {
    return {
      device_type: ''
    }
  },
  mounted: function () {
    window.setInterval(() => {
      this.getDeviceType()
    }, 2000)
    window.setInterval(() => {
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
    RouteToDevice () {
      console.log('Evaluate received Device Type')
      if (this.device_type !== '') {
        console.log('Routing to ' + this.device_type)
        this.$router.push({ name: this.device_type }, () => {})
      } else {
        console.log('No Device Type received')
      }
    }
  }
}
</script>

<style>
#logo {
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
