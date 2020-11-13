<template>
  <div class="container">
    <p>Restore Debug Phase</p>
    <div class="btns">
      <v-btn class="mr-2" @click="restore_type = 1">This Tab</v-btn>
      <v-btn @click="restore_type = 2">All</v-btn>
    </div>
    <div class="row">
      {{ restore_type }}
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
  destroyed() {
    console.log("BYE FROM Restore");
  },
};
</script>

<style>
</style>