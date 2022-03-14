<template>
<!-- Header -->
<div class="SingleMotorFrame">
    <div class="header">
        <h1 class="text-xl font-extrabold"> Landing Page of Device {{DeviceName}}</h1>
        <div class="flex justify-center">
            <p class="border border-black  border-r-0">Devicestate: </p>
            <p :class="DeviceState ? 'border border-black  border-l-0 text-green-500' : 'border border-black  border-l-0 text-red-500' ">
                {{ DeviceState  ?  'running'  :  'stopped'  }} </p>
        </div>
    </div>
    <!-- Motor Selection Segment -->
    <desy-select
    @change="MotorNumChanged"
    placeholder='Motor X'
    :value=this.MotorNum
    :disabled=this.ChangePending
    :options="[
    { value: 1, text: 'Motor 1' },{ value: 2, text: 'Motor 2' },{ value: 3, text: 'Motor 3' },{ value: 4, text: 'Motor 4' },
    { value: 5, text: 'Motor 5' },{ value: 6, text: 'Motor 6' },{ value: 7, text: 'Motor 7' },{ value: 8, text: 'Motor 8' },
    { value: 9, text: 'Motor 9' },{ value: 10, text: 'Motor 10' },{ value: 11, text: 'Motor 11' },{ value: 12, text: 'Motor 12' },
    { value: 13, text: 'Motor 13' },{ value: 14, text: 'Motor 14' },{ value: 15, text: 'Motor 15' },{ value: 16, text: 'Motor 16' },
    { value: 17, text: 'Motor 17' },{ value: 18, text: 'Motor 18' },{ value: 19, text: 'Motor 19' },{ value: 20, text: 'Motor 20' },
    { value: 21, text: 'Motor 21' },{ value: 22, text: 'Motor 22' },{ value: 23, text: 'Motor 23' },{ value: 24, text: 'Motor 24' },
    { value: 25, text: 'Motor 25' }
    ]">
    </desy-select>
    <!-- Position Segment -->
  <div class="content font-bold grid grid-cols-2 justify-center p-5">
    <div class="border border-black grid grid-cols-2 space-x-1">
      <p>Istposition:</p>
      <p>{{actValue}}</p>
    </div>
    <div class="flex justify-center">
    <desy-button variant="success">Start</desy-button>
    </div>
    <div class="border border-black border-t-0 grid grid-cols-2 space-x-1">
      <p>Sollposition:</p>
      <p>{{targetValue}}</p>
    </div>
    <div class="flex justify-center">
    <desy-button variant="error">Stop</desy-button>
    </div>
  </div>
    <!-- Increment Selection -->
    <div>
        <p class="flex justify-center text-xs">Sollposition Vorgabe (in Steps):</p>
    </div>
    <div class="grid grid-cols-3 justify-around p-5 md:grid-cols-6">
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
    <div class="flex justify-evenly">
        <desy-button variant="bigger">+</desy-button>
        <desy-button variant="bigger">-</desy-button>
    </div>
</div>
</template>

<script>
export default {
  mounted: function () {
    window.setInterval(() => {
    }, 1000)
  },
  methods: {
    MotorNumChanged (e) {
      if (typeof (e) === 'string') {
        this.MotorNum = e
        this.$socket.emit('MotorNum_changed', e)
        this.ChangePending = true
      }
    }
  },
  sockets: {
    connect: function () {
      console.log('socketio connected')
    },
    disconnect: function () {
      console.log('socket disconnected')
    },
    update_values: function (data) {
      this.ChangePending = false
      this.DeviceState = data.plc_running
      this.actValue = data.actpos
      this.targetValue = data.targetpos
    }
  },
  data () {
    return {
      DeviceName: 'Motor Controller',
      MotorNum: 1,
      DeviceState: false,
      ChangePending: false,
      actValue: 0.000,
      targetValue: 0.000
    }
  }
}
</script>
