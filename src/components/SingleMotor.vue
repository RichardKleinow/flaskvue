<template>
<!-- Header -->
<div class="SingleMotorFrame">
  <div class="header">
    <h1 class="text-xl font-extrabold"> Landing Page of Device {{DeviceName}}</h1>
    <div class="flex justify-center">
    <p class="border border-black  border-r-0">State: </p>
    <p v-if=DeviceState class="text-green-500 border border-black border-l-0"> online </p>
    <p v-else class="text-red-500 border border-black border-l-0">offline</p>
    </div>
  </div>
  <!-- Position Segment -->
  <div class="content grid grid-cols-2 justify-center p-5">
    <div class="border border-black grid grid-cols-2 space-x-1">
      <p>Istwert:</p>
      <p>{{actValue}}</p>
    </div>
    <div class="flex justify-center">
    <desy-button variant="success">Start</desy-button>
    </div>
    <div class="border border-black border-t-0 grid grid-cols-2 space-x-1">
      <p>Sollwert:</p>
      <p>{{targetValue}}</p>
    </div>
    <div class="flex justify-center">
    <desy-button variant="error">Stop</desy-button>
    </div>
  </div>
  <!-- Increment buttons -->
    <div>
      <p class="flex justify-center text-xs">Sollposition Vorgabe (in Steps):</p>
    </div>
   <div class="flex justify-around p-5">
      <t-tag tag-name="label" variant="radiolabel">
        <t-radio name="increments" value=1 checked />
        <span class="ml-2 text-sm">1</span>
      </t-tag>
      <t-tag tag-name="label" variant="radiolabel">
        <t-radio name="increments" value=10 />
        <span class="ml-2 text-sm">10</span>
      </t-tag>
      <t-tag tag-name="label" variant="radiolabel">
        <t-radio name="increments" value=100 />
        <span class="ml-2 text-sm">100</span>
      </t-tag>
      <t-tag tag-name="label" variant="radiolabel">
        <t-radio name="increments" value=1000 />
        <span class="ml-2 text-sm">1000</span>
      </t-tag>
       <t-tag tag-name="label" variant="radiolabel">
        <t-radio name="increments" value=10000 />
        <span class="ml-2 text-sm">10000</span>
      </t-tag>
       <t-tag tag-name="label" variant="radiolabel">
        <t-radio name="increments" value=100000 />
        <span class="ml-2 text-sm">100000</span>
      </t-tag>
   </div>
</div>
</template>

<script>
export default {
  data () {
    return {
      DeviceName: 'Testmotor',
      DeviceState: false,
      actValue: 0.000,
      targetValue: 0.000
    }
  }
}
</script>
