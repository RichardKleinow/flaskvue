<template>
<div class="SingleMotorFrame">
  <div class="header">
    <h1 class="text-xl font-extrabold"> Landing Page of Device {{DeviceName}} </h1>
  </div>
  <div class="content grid justify-center p-5">
    <desy-button>Desy colored button</desy-button>
  </div>
</div>
</template>

<script>
export default {
  data () {
    return {
      DeviceName: 'Testmotor'
    }
  }
}
</script>
