<template>
<!-- Header -->
<div class="SingleMotorFrame ml-4 mr-4">
    <div class="header">
        <h1 class="text-xl font-extrabold"> Landing Page of Device {{DeviceName}}</h1>
        <div class="flex justify-center">
            <p class="border border-black  border-r-0">Devicestate: </p>
            <p :class="DeviceState ? 'border border-black  border-l-0 text-green-500' : 'border border-black  border-l-0 text-red-500' ">
                {{ DeviceState  ?  'running'  :  'stopped'  }} </p>
        </div>
    </div>

    <!-- Motor Selection Segment -->
    <desy-select @change="MotorNumChanged" placeholder='Motor ' :value=this.MotorNum :disabled=this.ChangePending :options="[
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
            <p class="self-center">actual position:</p>
            <input class="border-0 " type="number" readonly=true v-model="actpos">
        </div>
        <div class="flex justify-center">
            <desy-button variant="success">Start</desy-button>
        </div>
        <div class="border border-black border-t-0 grid grid-cols-2 space-x-1">
            <p class="self-center">target position:</p>
            <input class="border-0 " type="number" readonly=true v-model="targetpos">
        </div>
        <div class="flex justify-center">
            <desy-button variant="error">Stop</desy-button>
        </div>
    </div>

    <!-- Increment Selection -->
    <div>
        <p class="flex justify-center text-xs">target position (in steps):</p>
    </div>
    <div class="grid grid-cols-3 justify-between grid-4">
        <div class="col-span-2 mr-4">
        <div class="flex flex-col space-y-2 p-2">
            <input type="range" class="w-full" min="1" max="6" step="1" v-model="range"/>
            <ul class="flex text-xs md:text-base justify-between w-full px-[10px]">
                <li class="font-bold flex justify-center relative"><span class="absolute">1</span></li>
                <li class="font-bold flex justify-center relative"><span class="absolute">10</span></li>
                <li class="font-bold flex justify-center relative"><span class="absolute">100</span></li>
                <li class="font-bold flex justify-center relative"><span class="absolute">1000</span></li>
                <li class="font-bold flex justify-center relative"><span class="absolute">10000</span></li>
                <li class="font-bold flex justify-center relative"><span class="absolute">100000</span></li>
            </ul>
        </div>
        </div>
        <div class="flex justify-evenly">
            <desy-button @click="SetValue('targetpos', targetpos + true_range)" variant="bigger">+</desy-button>
            <desy-button @click="SetValue('targetpos', targetpos - true_range)" variant="bigger">-</desy-button>
        </div>
    </div>

   <!-- Virtual Limits -->
   <div class="grid grid-cols-2 gap-4 justify-between mt-4 text-xs md:grid-cols-4 md:text-base">
      <desy-table
      :headers="['virtual limits','']"
      :data="[
      ['virtual limit +', virtposlimit],
      ['virtual limit -', virtneglimit]
      ]"
      ><template slot="row" slot-scope="props">
        <tr :class="[props.trClass, props.rowIndex % 2 === 0 ? 'bg-gray-50' : '']">
        <td :class="props.tdClass">{{ props.row[0] }}</td>
        <td :class="props.tdClass"> <t-input type="number" min="0" class='text-xs md:text-base' v-bind:value=props.row[1] /> </td>
        </tr>
      </template>
       <template slot="thead" slot-scope="props">
          <thead :class="props.theadClass">
            <tr :class="props.trClass">
            <th colspan="2" :class="[props.tdClass, 'text-left']">
              {{ props.data[0].text }}
            </th>
            </tr>
          </thead>
       </template>
      </desy-table>
      <!-- Command Values -->
      <desy-table
      :headers="['command values','']"
      :data="[
      ['command', command],
      ['sec. command', seccommand]
      ]"
      ><template slot="row" slot-scope="props">
        <tr :class="[props.trClass, props.rowIndex % 2 === 0 ? 'bg-gray-50' : '']">
        <td :class="props.tdClass">{{ props.row[0] }}</td>
        <td :class="props.tdClass">{{ props.row[1] }} </td>
        </tr>
      </template>
       <template slot="thead" slot-scope="props">
          <thead :class="props.theadClass">
            <tr :class="props.trClass">
            <th colspan="2" :class="[props.tdClass, 'text-left']">
              {{ props.data[0].text }}
            </th>
            </tr>
          </thead>
       </template>
      </desy-table>
      <!-- Current Values -->
      <desy-table
      :headers="['current values A','']"
      :data="[
      ['A1', currA1],
      ['A2', currA2]
      ]"
      ><template slot="row" slot-scope="props">
        <tr :class="[props.trClass, props.rowIndex % 2 === 0 ? 'bg-gray-50' : '']">
        <td :class="props.tdClass">{{ props.row[0] }}</td>
        <td :class="props.tdClass">{{ props.row[1] }} </td>
        </tr>
      </template>
       <template slot="thead" slot-scope="props">
          <thead :class="props.theadClass">
            <tr :class="props.trClass">
            <th colspan="2" :class="[props.tdClass, 'text-left']">
              {{ props.data[0].text }}
            </th>
            </tr>
          </thead>
       </template>
      </desy-table>
      <desy-table
      :headers="['current values B','']"
      :data="[
      ['B1', currB1],
      ['B2', currB2]
      ]"
      ><template slot="row" slot-scope="props">
        <tr :class="[props.trClass, props.rowIndex % 2 === 0 ? 'bg-gray-50' : '']">
        <td :class="props.tdClass">{{ props.row[0] }}</td>
        <td :class="props.tdClass">{{ props.row[1] }} </td>
        </tr>
      </template>
       <template slot="thead" slot-scope="props">
          <thead :class="props.theadClass">
            <tr :class="props.trClass">
            <th colspan="2" :class="[props.tdClass, 'text-left']">
              {{ props.data[0].text }}
            </th>
            </tr>
          </thead>
       </template>
      </desy-table>
   </div>
  <!-- Expert Segment -->
  <div class="flex justify-start text-xs mt-4">
    <p>Expert Content:</p>
  </div>
    <div class="flex justify-start text-xs mt-4">
    <desy-toggle @click="show_expert = !show_expert" />
  </div>
  <div v-show="show_expert" class="grid grid-cols-2 gap-4 justify-between mt-4 text-xs md:grid-cols-3 md:text-base">
    <!-- State Segment -->
     <desy-table
      :headers="['state','']"
      :data="[
      ['motor moving/holding current', bit_test(state,0)],
      ['motor enabled', bit_test(state,1)],
      ['motor not busy ', bit_test(state,2)],
      ['no error  [Error Value: ' + error +']', bit_test(state,3)],
      ['pos. limit switch triggered', bit_test(state,4)],
      ['neg. limit switch triggered', bit_test(state,5)],
      ['virtual limit reached', bit_test(state,6)],
      ['', bit_test(state,7)],
      ['', bit_test(state,8)],
      ['', bit_test(state,9)],
      ['', bit_test(state,10)],
      ['', bit_test(state,11)],
      ['', bit_test(state,12)],
      ['', bit_test(state,13)],
      ['', bit_test(state,14)],
      ['', bit_test(state,15)]
      ]"
      ><template slot="row" slot-scope="props">
        <tr :class="[props.trClass, props.rowIndex % 2 === 0 ? 'bg-gray-50' : '']">
        <td :class="props.tdClass">{{ props.row[0] }}</td>
        <td :class="props.tdClass"><svg height="20" width="20">
        <circle cx=10 cy=10 r="8" stroke="black" stroke-width="1" :fill="colorAttr(props.row[1])" />
        </svg>  </td>
        </tr>
      </template>
       <template slot="thead" slot-scope="props">
          <thead :class="props.theadClass">
            <tr :class="props.trClass">
            <th colspan="2" :class="[props.tdClass, 'text-left']">
              {{ props.data[0].text }}
            </th>
            </tr>
          </thead>
       </template>
      </desy-table>
      <!-- Config Segment -->
     <desy-table
      :headers="['Configuration','']"
      :data="[
      ['limit switch inactive', bit_test(config,0)],
      ['limit switch neg. direction is normally open', bit_test(config,1)],
      ['limit switch pos. direction is normally open ', bit_test(config,2)],
      ['motor is rotary table', bit_test(config,3)],
      ['act. pos. = 0 if limit + reached', bit_test(config,4)],
      ['act. pos. = 0 if limit - reached', bit_test(config,5)],
      ['software limits active', bit_test(config,6)],
      ['', bit_test(config,7)],
      ['autostart on', bit_test(config,8)],
      ['holding current on', bit_test(config,9)],
      ['', bit_test(config,10)],
      ['', bit_test(config,11)],
      ['', bit_test(config,12)],
      ['', bit_test(config,13)],
      ['', bit_test(config,14)],
      ['', bit_test(config,15)]
      ]"
      ><template slot="row" slot-scope="props">
        <tr :class="[props.trClass, props.rowIndex % 2 === 0 ? 'bg-gray-50' : '']">
        <td :class="props.tdClass">{{ props.row[0] }}</td>
        <td :class="props.tdClass"><svg height="20" width="20" @click="config = bit_toggle(config,props.rowIndex)">
        <circle cx=10 cy=10 r="8" stroke="black" stroke-width="1" :fill="colorAttr(props.row[1])"/>
        </svg>
        </td>
        </tr>
      </template>
       <template slot="thead" slot-scope="props">
          <thead :class="props.theadClass">
            <tr :class="props.trClass">
            <th colspan="2" :class="[props.tdClass, 'text-left']">
              {{ props.data[0].text }}
            </th>
            </tr>
          </thead>
       </template>
      </desy-table>
    <!-- Register -->
      <desy-table class="col-span-2"
      :headers="['register','']"
      :data="[
      ['feature Register [R32]', R32],
      ['full steps per rotation [R33]', R33],
      ['encoder increments [R34]', R34],
      ['curr. coil A in % [R35]', R35],
      ['curr. coil B in % [R36]', R36],
      ['number of latch values [R37]', R37],
      ['vmin steps/s [R38]', R38],
      ['vmax steps/s [R39]', R39],
      ['amax steps/s [R40]', R40],
      ['acc. threshold steps/s [R41]', R41],
      ['curr. a > athreshold [R42]', R42],
      ['curr. a <= athreshold [R43]', R43],
      ['curr. (autom.) v=0 [R44]', R44],
      ['curr. (man.) v=0 [R45]', R45],
      ['micro steps per full step[R46] ', R46]
      ]"
      ><template slot="row" slot-scope="props">
        <tr :class="[props.trClass, props.rowIndex % 2 === 0 ? 'bg-gray-50' : '']">
        <td :class="props.tdClass">{{ props.row[0] }}</td>
        <td :class="props.tdClass"> <t-input type="number" min="0" class='text-xs md:text-base' v-bind:value=props.row[1] /> </td>
        </tr>
      </template>
       <template slot="thead" slot-scope="props">
          <thead :class="props.theadClass">
            <tr :class="props.trClass">
            <th colspan="2" :class="[props.tdClass, 'text-left']">
              {{ props.data[0].text }}
            </th>
            </tr>
          </thead>
       </template>
      </desy-table>
  </div>
  </div>
</template>

<script>
export default {
  methods: {
    MotorNumChanged (e) {
      if (typeof (e) === 'string') {
        this.MotorNum = e
        this.$socket.emit('MotorNum_changed', e)
        this.ChangePending = true
      }
    },
    SetValue (name, value) {
      this.$socket.emit('set_value', name, value)
    },
    colorAttr (attr) {
      var retval = '#ffffff'
      if (attr) {
        retval = '#00ff00'
      } else {
        retval = '#ff0000'
      }
      return retval
    },
    bit_test: function (num, bit) {
      return ((num >> bit) % 2 !== 0)
    },
    bit_set: function (num, bit) {
      return num | 1 << bit
    },
    bit_clear: function (num, bit) {
      return num & ~(1 << bit)
    },
    bit_toggle: function (num, bit) {
      return this.bit_test(num, bit) ? this.bit_clear(num, bit) : this.bit_set(num, bit)
    }
  },
  computed: {
    true_range: function () {
      return Math.pow(10, (this.range - 1))
    }
  },
  sockets: {
    connect: function () {
      console.log('socketio connected')
    },
    disconnect: function () {
      console.log('socket disconnected')
    },
    update_values_quick: function (data) {
      this.DeviceState = data.plc_running
      this.actpos = data.actpos
      this.targetpos = data.targetpos
      this.command = data.command
      this.seccommand = data.seccommand
      this.state = data.state
      this.error = data.error
      this.config = data.config
      this.distmeas = data.distmeas
      if (!this.ChangePending) {
        this.MotorNum = parseInt(data.MotorNum)
      }
      if (this.ChangePending && this.MotorNum === data.MotorNum) {
        this.ChangePending = false
      }
    },
    update_values_slow: function (data) {
      this.currA1 = data.currA1
      this.currA2 = data.currA2
      this.currB1 = data.currB1
      this.currB2 = data.currB2
      this.loadangle = data.loadangle
      this.R32 = data.R32
      this.R33 = data.R33
      this.R34 = data.R34
      this.R35 = data.R35
      this.R36 = data.R36
      this.R37 = data.R37
      this.R38 = data.R38
      this.R39 = data.R39
      this.R40 = data.R40
      this.R41 = data.R41
      this.R42 = data.R42
      this.R43 = data.R43
      this.R44 = data.R44
      this.R45 = data.R45
      this.R46 = data.R46
      this.virtposlimit = data.virtposlimit
      this.virtneglimit = data.virtneglimit
      this.diststate = data.diststate
      this.distlatch = data.distlatch
      this.homespeed = data.homespeed
      this.homeacc = data.homeacc
      this.reserve1 = data.reserve1
      this.reserve2 = data.reserve2
      this.reserve3 = data.resserve3
    }
  },
  data () {
    return {
      DeviceName: 'Motor Controller',
      show_expert: false,
      range: 3,
      MotorNum: 0,
      DeviceState: false,
      ChangePending: false,
      actpos: 0.000,
      targetpos: 0.000,
      state: 0,
      error: 0,
      config: 0,
      distmeas: 0,
      command: 0,
      seccommand: 0,
      currA1: 0,
      currA2: 0,
      currB1: 0,
      currB2: 0,
      loadangle: 0,
      R32: 0,
      R33: 0,
      R34: 0,
      R35: 0,
      R36: 0,
      R37: 0,
      R38: 0,
      R39: 0,
      R40: 0,
      R41: 0,
      R42: 0,
      R43: 0,
      R44: 0,
      R45: 0,
      R46: 0,
      virtposlimit: 0,
      virtneglimit: 0,
      diststate: 0,
      distlatch: 0,
      homespeed: 0,
      homeacc: 0,
      reserve1: 0,
      reserve2: 0,
      reserve3: 0
    }
  }
}
</script>

<style>
  #logo {
    animation: none;
    -webkit-animation: none;
  }
</style>
