<template>
<div>
    <head v-show="seen" class="flex justify-center" id="header">
        <router-link to="/">
            <img src="./assets/logo.svg" alt="./assets/logo.png" id="logo">
        </router-link>
    </head>
<div id="app">
    <router-view />
</div>
</div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      seen: false
    }
  },
  watch: {
    $route: {
      handler (to, from) {
        if ((from === undefined) || (to.name === 'Home')) {
          this.seen = false
        } else {
          this.seen = true
        }
      }
    },
    immediate: true
  }
}
</script>

<style>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}

#logo {
    height: 200px;
    width: auto;
}
</style>
