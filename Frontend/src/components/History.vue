<template>
  <div class="container">
    <div class="rows">
      <div v-if="this.host == this.$store.state.uid.username" class="btns mb-3">
        <v-btn style="margin-right:5px;" @click="history_type = 1">노트 삭제 기록</v-btn>
        <v-btn @click="history_type = 2">화면 히스토리</v-btn>
      </div>
      <div class="btns mb-3" v-if="history_type == 2">
        <p
          style="
            color: white;
            text-align: center;
            font-family: 'HangeulNuri-Bold';
            font-size: 15px;
            margin: 0 auto 10px;
          "
        >
          현재 화면에 보이는 노트 상태를 저장하고 <br>
          원하는 시점에 불러올 수 있습니다.
        </p>
        <v-btn block class="md-2" @click="timemachineSave()">SAVE</v-btn>
        <p
          style="
            color: white;
            text-align: center;
            font-family: 'HangeulNuri-Bold';
            font-size: 15px;
            margin: 10px auto 10px;
          "
        >
          마우스를 올리면 미리 볼 수 있습니다.<br>
          불러오려면 클릭하세요
        </p>
      </div>
    </div>
    <div v-if="history_type == 1">
      <Restore
        :restore_list="restore_list"
        :restore_prev="restore_prev"
        :restore_next="restore_next"
        v-on:restore-request="restoreNote"
        v-on:get-list="getRestoreList()"
      ></Restore>

        <!-- v-on:page-list="getPaginatedRestoreList" -->
    </div>
    <div v-if="history_type == 2">
      <TimeMachine
        :time_machine_list="time_machine_list"
        :time_machine_prev="time_machine_prev"
        :time_machine_next="time_machine_next"
        v-on:time-slip-request="timeslipTab"
        v-on:get-list="getTimeMachineList()"
        @tmpTimeSlip="tmpTimeSlip"
        @tmpTimeSlipend="tmpTimeSlipend"
      ></TimeMachine>
        <!-- v-on:page-list="getPaginatedTimeMachineList" -->
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
  created() {
    this.getRestoreList();
  },
  components: {
    Restore,
    TimeMachine,
  },
  props: {
    activatedTab: Number,
    host: String,
    restore_list_t: Array,
    restore_prev_t: Array,
    restore_next_t: Array,
  },
  watch: {
    restore_list_t() {
      this.getRestoreList();
    },
    history_type() {
      this.getRestoreList();
    },
    activatedTab: function () {
      this.history_type = 1;
      this.getRestoreList();
    },
  },
  methods: {
    tmpTimeSlip(note_list){
      this.$emit("tmpTimeSlip", note_list);
    },
    tmpTimeSlipend() {
      this.$emit("tmpTimeSlipend");
    },
    timeslipTab(time_machine_index) {
      let base_url =
        SERVER.URL +
        "/api/v1/board/" +
        this.$route.params.code +
        "/tab/" +
        this.activatedTab +
        "/time-machine/" +
        time_machine_index +
        "/";

      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };

      // console.log(base_url, config);
      axios.post(base_url, null, config).then(() => {
        // TO-DO: 이 요청이 지나간 직후 곧 바로 fetchNoteList를 호출하도록 해야 한다. 다른 코드를 건드려야 하는 상황이므로 이 부분에 대해서는 작업하지 않겠음
        this.getTimeMachineList();
        this.$emit("refresh");
      });
    },
    restoreNote(target_note_index) {
      // console.log("Restore This!", target_note_index);
      let base_url =
        SERVER.URL +
        "/api/v1/board/" +
        this.$route.params.code +
        "/tab/" +
        this.activatedTab +
        "/history/" +
        target_note_index +
        "/detail/";

      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };

      axios.post(base_url, null, config).then(() => {
        // TO-DO: 이 요청이 지나간 직후 곧 바로 fetchNoteList를 호출하도록 해야 한다. 다른 코드를 건드려야 하는 상황이므로 이 부분에 대해서는 작업하지 않겠음
        this.getRestoreList();
        this.$emit("refresh");
      });
    },
    getPaginatedRestoreList(target_url) {
      const split_url = target_url.split("/");
      const target_param = split_url[split_url.length - 1];
      let base_url =
        SERVER.URL +
        "/api/v1/board/" +
        this.$route.params.code +
        "/tab/" +
        this.activatedTab +
        "/history/" +
        target_param;

      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };

      axios
        .get(base_url, config)
        .then((res) => {
          this.restore_prev = res.data.previous;
          this.restore_next = res.data.next;
          this.restore_list = res.data.results;
        })
        .catch((err) => console.log(err.response.data));
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

      axios
        .get(base_url, config)
        .then((res) => {
          this.restore_prev = res.data.previous;
          this.restore_next = res.data.next;
          this.restore_list = res.data.results;
        })
        .catch((err) => console.log(err.response.data));
    },
    timemachineSave() {
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

      axios.post(base_url, null, config).then(() => {
        this.getTimeMachineList();
      });
    },
    // getPaginatedTimeMachineList(target_url) {
    //   const split_url = target_url.split("/");
    //   const target_param = split_url[split_url.length - 1];
    //   let base_url =
    //     SERVER.URL +
    //     "/api/v1/board/" +
    //     this.$route.params.code +
    //     "/tab/" +
    //     this.activatedTab +
    //     "/time-machine/" +
    //     target_param;

    //   let config = {
    //     headers: {
    //       Authorization: "Bearer " + cookies.get("auth-token"),
    //     },
    //   };

    //   axios
    //     .get(base_url, config)
    //     .then((res) => {
    //       console.log(res);
    //       this.time_machine_prev = res.data.previous;
    //       this.time_machine_next = res.data.next;
    //       this.time_machine_list = res.data.results;
    //     })
    //     .catch((err) => console.log(err.response.data));
    // },
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

<style scoped>
.container {
  overflow-y: scroll;
  height: 100%;
}
.btn-primary {
  margin-left: 5px;
}
.scroll {
  /* overflow: scroll; */
}
.div__username {
  margin: 0;
  padding: 0;
  font-size: 1.2em;
}
.control {
  display: flex;
  justify-content: space-evenly;
  padding: 0;
}
.button {
  padding: 0px;
}
.border {
  margin-top: 2em;
  border-bottom: dashed #453c2b 0.2em;
}
</style>