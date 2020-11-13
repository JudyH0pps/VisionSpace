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
        v-on:get-list="getRestoreList(null)"
      ></Restore>
    </div>
    <div v-if="history_type == 2">
      <TimeMachine
        :time_machine_list="time_machine_list"
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
      time_machine_list: null,
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
    getPaginatedRestoreList() {},
    getRestoreList(params) {
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

      console.log(base_url, config, params);

      axios
        .get(base_url, config)
        .then((res) => {
          this.restore_list = res.data.results;
        })
        .catch((err) => console.log(err.response.data));
    },
    getPaginatedTimeMachineList() {},
    getTimeMachineList(params) {
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

      console.log(base_url, config, params);

      axios
        .get(base_url, config)
        .then((res) => {
          this.time_machine_list = res.data.results;
        })
        .catch((err) => console.log(err.response.data));
    },
  },
};
</script>

<style>
</style>