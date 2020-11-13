<template>
  <div class="container">
    <p>Restore Debug Phase</p>
    <div class="btns">
      <v-btn class="mr-2" @click="getPaginatedList('prev')">Prev</v-btn>
      <v-btn @click="getPaginatedList('next')">Next</v-btn>
    </div>
    <div class="row">
      {{ restore_list }}
    </div>
  </div>
</template>

<script>
export default {
  name: "Restore",
  data() {
    return {};
  },
  props: {
    restore_list: Array,
    restore_prev: String,
    restore_next: String,
  },
  created() {
    console.log("Hello FROM Restore");
    this.$emit("get-list");
  },
  destroyed() {
    console.log("BYE FROM Restore");
  },
  methods: {
    getPaginatedList(target) {
      console.log(target);
      if (target === "prev" && this.restore_prev) {
        this.$emit("page-list", this.restore_prev);
      } else if (target === "next" && this.restore_next) {
        this.$emit("page-list", this.restore_next);
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