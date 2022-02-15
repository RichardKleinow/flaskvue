// Home.vue

<template>
<div>
    <p>Home Page</p>
    <p>Random Number from Backend: {{ randomNumber }}</p>
    <button @click="getRandom">Random Number Generator</button>
</div>
</template>

<script>
export default {
    data() {
        return {
            randomNumber: 0
        }
    },
    mounted () {
      this.$socket.on("user-connected", (data) => {
        debugger
        console.log(data)
        this.$socket.emit("users")
      })
    },
    methods: {
        getRandom() {
            this.randomNumber = this.GetFromBackend()
        },
        GetFromBackend() {
            const Arr_basepath = window.location.href.split(':')
            const basepath = Arr_basepath[0] + ":" + Arr_basepath[1]
            const path = basepath + `:5000/api/random`
            console.log(path)
            const axios = require('axios')
            axios.get(path)
                .then((response) => {
                    this.randomNumber = response.data.randomNumber
                    console.log(response.data.randomNumber)
                })
                .catch((error) => {
                    console.log(error)
                    this.randomNumber = error
                })
        }
    }
}
</script>
