<template>
  <div class="container">
    <p>DEBUG for History</p>
    <div class="btns">
      <v-btn class="mr-2" @click="history_type = 1">Restore</v-btn>
      <v-btn @click="history_type = 2">Time Machine</v-btn>
    </div>
    <div v-if="history_type == 1">
      <Restore
        :restore_list="restore_list"
        :restore_prev="restore_prev"
        :restore_next="restore_next"
        v-on:page-list="getPaginatedRestoreList(target_url)"
        v-on:get-list="getRestoreList(null)"
      ></Restore>
    </div>
    <div v-if="history_type == 2">
      <TimeMachine
        :time_machine_list="time_machine_list"
        :time_machine_prev="time_machine_prev"
        :time_machine_next="time_machine_next"
        v-on:page-list="getPaginatedTimeMachineList(target_url)"
        v-on:get-list="getTimeMachineList(null)"
      ></TimeMachine>
    </div>
  </div>
</template>

<script>
import Restore from "./History/Restore.vue";
import TimeMachine from "./History/TimeMachine.vue";

// eslint-disable-next-line no-unused-vars
import SERVER from "@/api/drf";

// eslint-disable-next-line no-unused-vars
import axios from "axios";

// eslint-disable-next-line no-unused-vars
import cookies from "vue-cookies";

export default {
  name: "History",
  data() {
    return {
      history_type: 1,
      restore_list: null,
      restore_prev: null,
      restore_next: null,
      time_machine_list: null,
      time_machine_prev: null,
      time_machine_next: null,
    };
  },
  created() {},
  components: {
    Restore,
    TimeMachine,
  },
  props: {
    activatedTab: Number,
  },
  methods: {
    getPaginatedRestoreList(target_url) {
      console.log(target_url);
    },
    getRestoreList() {
      let base_url =
        SERVER.URL +
        "/api/v1/board/" +
        this.$route.params.code +
        "/tab/" +
        this.activatedTab +
        "/history/";

      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };

      console.log(base_url, config);

      axios
        .get(base_url, config)
        .then((res) => {
          this.restore_prev = res.data.previous;
          this.restore_next = res.data.next;
          this.restore_list = res.data.results;
        })
        .catch((err) => console.log(err.response.data));
    },
    getPaginatedTimeMachineList(target_url) {
      console.log(target_url);
    },
    getTimeMachineList() {
      let base_url =
        SERVER.URL +
        "/api/v1/board/" +
        this.$route.params.code +
        "/tab/" +
        this.activatedTab +
        "/time-machine/";

      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };

      console.log(base_url, config);

      axios
        .get(base_url, config)
        .then((res) => {
          this.time_machine_prev = res.data.previous;
          this.time_machine_next = res.data.next;
          this.time_machine_list = res.data.results;
        })
        .catch((err) => console.log(err.response.data));
    },
  },
};
</script>

<style>
</style>