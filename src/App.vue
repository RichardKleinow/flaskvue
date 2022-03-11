<template>
<div id="app">
    <div id="head" class="flex justify-center">
        <router-link to="/">
            <img src="./assets/logo.svg" alt="./assets/logo.png" id="logo">
        </router-link>
    </div>
    <router-view />
</div>
</template>

<script>
export default {
  name: 'App',
  watch: {
    $route: {
      handler (to, from) {
        if (from !== undefined) {
          if (from.name === 'Home') {
            this.$router.go(0)
          }
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
