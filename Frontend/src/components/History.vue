<template>
  <div class="container">
    <p>DEBUG for History</p>
    <div class="btns">
      <v-btn @click="history_type = 1">MODE 1</v-btn>
      <v-btn @click="history_type = 2">MODE 2</v-btn>
    </div>
    <div v-if="history_type == 1">
      <Restore></Restore>
    </div>
    <div v-if="history_type == 2">
      <TimeMachine></TimeMachine>
    </div>
  </div>
</template>

<script>
import Restore from "./History/Restore.vue";
import TimeMachine from "./History/TimeMachine.vue";

export default {
  name: "History",
  data() {
    return {
      history_type: 1,
    };
  },
  components: {
    Restore,
    TimeMachine,
  },
};
</script>

<style>
</style>