<template>
  <div class="container">
    <p>TimeMachine Debug Phase</p>
    <div class="btns">
      <v-btn class="mr-2" @click="getTabList()">This Tab</v-btn>
      <v-btn @click="getBoardList()">This Board</v-btn>
    </div>
    <div class="row">
      {{ time_machine_type }}
      {{ time_machine_list }}
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
  props: {
    time_machine_list: Array,
  },
  created() {
    console.log("Hello FROM TimeMachine");
    this.$emit("get-list");
  },
  destroyed() {
    console.log("BYE FROM TimeMachine");
  },
  methods: {
    getTabList() {
      this.time_machine_type = 1;
      this.$emit("get-list");
    },
    getBoardList() {
      this.time_machine_type = 2;
      this.$emit("get-list");
    },
  },
};
</script>

<style>
</style>