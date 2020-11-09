<template>
  <v-app>
    <div class="container">
      <div class="row">
        <div class="col-1 col-md-12">
          <p>{{ roomId }}</p>
        </div>
      </div>
    </div>
  </v-app>
</template>

<script>
// import Vue from "vue";
// import { WebRTC } from "plugin";
//   import { find, head } from 'lodash';
// Vue.component(WebRTC, WebRTC);

export default {
  name: "WebRTC",
  components: {},
  data() {
    return {
      img: null,
      roomId: "",
    };
  },
  computed: {},
  watch: {},
  methods: {
    onJoin() {
      // this.$refs.webrtc.join();
    },
    onLeave() {
      // this.$refs.webrtc.leave();
    },
    onCapture() {
      // this.img = this.$refs.webrtc.capture();
    },
    onError(error, stream) {
      console.log("On Error Event", error, stream);
    },
    logEvent(event) {
      console.log("Event : ", event);
    },
  },
  created() {
    this.roomId = this.$route.params.code;
  },
  mounted() {
    // this.onJoin();
  },
  destroyed() {
    // this.onLeave();
  },
};
</script>
<style scoped>
.btn-primary {
  margin-left: 5px;
}
</style>
