<template>
  <div class="container">
    <p>TimeMachine Debug Phase</p>
    <div class="btns">
      <v-btn class="mr-2" @click="getPaginatedList('prev')">Prev</v-btn>
      <v-btn @click="getPaginatedList('next')">Next</v-btn>
    </div>
    <v-container>
      <v-row>
        <v-col v-for="(value, idx) in time_machine_list" :key="idx">
          {{ value }}
          <v-btn @click="requestTimeSlip(value.tm_index)">Time Slip</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "TimeMachine",
  data() {
    return {};
  },
  props: {
    time_machine_list: Array,
    time_machine_prev: String,
    time_machine_next: String,
  },
  created() {
    console.log("Hello FROM TimeMachine");
    this.$emit("get-list");
  },
  destroyed() {
    console.log("BYE FROM TimeMachine");
  },
  methods: {
    requestTimeSlip(target) {
      this.$emit("time-slip-request", target);
    },
    getPaginatedList(target) {
      console.log(target);
      if (target === "prev" && this.time_machine_prev) {
        this.$emit("page-list", this.time_machine_prev);
      } else if (target === "next" && this.time_machine_next) {
        this.$emit("page-list", this.time_machine_next);
      }
    },
    getList() {
      this.$emit("get-list");
    },
  },
};
</script>

<style>
</style>