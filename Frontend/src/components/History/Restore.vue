<template>
  <div class="container">
    <p>Restore Debug Phase</p>
    <div class="btns">
      <v-btn class="mr-2" @click="restore_type = 1">This Tab</v-btn>
      <v-btn @click="restore_type = 2">All</v-btn>
    </div>
    <div class="row">
      {{ restore_type }}
      {{ restore_list }}
    </div>
  </div>
</template>

<script>
export default {
  name: "Restore",
  data() {
    return {
      restore_type: 1,
    };
  },
  props: {
    restore_list: Array,
  },
  created() {
    console.log("Hello FROM Restore");
    this.$emit("get-list");
  },
  destroyed() {
    console.log("BYE FROM Restore");
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