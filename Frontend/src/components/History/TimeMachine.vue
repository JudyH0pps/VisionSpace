<template>
  <div class="container">
    <p>TimeMachine Debug Phase</p>
    <div class="btns">
      <v-btn class="mr-2" @click="time_machine_type = 1">This Tab</v-btn>
      <v-btn @click="time_machine_type = 2">All</v-btn>
    </div>
    <div class="row">
      {{ time_machine_type }}
    </div>
  </div>
</template>

<script>
export default {
  name: "TimeMachine",
  data() {
    return {
      time_machine_type: 1,
    };
  },
  destroyed() {
    console.log("BYE FROM TimeMachine");
  },
};
</script>

<style>
</style>