<template>
  <div>
    <p>DEBUG for TimeMachine</p>
  </div>
</template>

<script>
export default {
  name: "TimeMachine",
  destroyed() {
    console.log("BYE FROM TimeMachine");
  },
};
</script>

<style>
</style>