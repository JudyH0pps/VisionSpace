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
// eslint-disable-next-line no-unused-vars
import SERVER from "@/api/drf";
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
// import Room from "janus-room";
import adapter from "webrtc-adapter";

export default {
  name: "WebRTC",
  components: {},
  data() {
    return {
      roomId: null,
      username: null,
    };
  },
  created() {
    this.roomId = this.$route.params.code;
    this.username = $store.state.uid.username;
    this.videoRoomInitializer();
  },
  mounted() {
    // this.onJoin();
    this.register();
    this.unpublish();
    this.toggleMuteVideo();
    this.toggleMuteAudio();
    this.startShareScreen();
    this.stopShareScreen();
    console.log(this.getSessionId.sessionId);
    console.log(this.getOptions);
  },
  destroyed() {
    console.log("I am 'DED'");
  },
  computed: {
    ...mapState("videoroom", ["sessionId", "videoroom", "options"]),
    ...mapGetters("videoroom", ["getSessionId", "getVideoRoom", "getOptions"]),
  },
  watch: {},
  methods: {
    ...mapActions("videoroom", [
      "register",
      "unpublish",
      "toggleMuteVideo",
      "toggleMuteAudio",
      "startShareScreen",
      "stopShareScreen",
    ]),
    ...mapMutations("videoroom", [
      "SET_SESSION_ID",
      "SET_VIDEO_ROOM",
      "SET_OPTION",
    ]),

    videoRoomInitializer() {
      this.SET_SESSION_ID({
        sessionId: this.roomId,
      });
      this.SET_OPTION({
        server: SERVER.URL + "/rtc",
        adapter: adapter,
        room: this.roomId,
        token: "a1b2c3d4",
        extensionId: "bkkjmbohcfkfemepmepailpamnppmjkk",
        publishOwnFeed: true,
        iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
        useRecordPlugin: false,
        volumeMeterSkip: 10,
        onLocalJoin: this.onLocalJoin,
        onRemoteJoin: this.onRemoteJoin,
        onRemoteUnjoin: this.onRemoteUnjoin,
        onError: this.onError,
        onWarning: this.onWarning,
        onVolumeMeterUpdate: this.onVolumeMeterUpdate,
      });
    },
    onError(err) {
      let self = this;
      if (err.indexOf("The room is unavailable") > -1) {
        console.log(
          "Room " + this.roomId + " is unavailable. Let's create one."
        );
        this.videoroom
          .createRoom({
            room: this.roomId,
            publishers: 12,
          })
          .then(() => {
            setTimeout(function () {
              self.videoroom.register({
                username: self.username,
                room: self.room_id,
              });
            }, 1000);
          })
          .catch((err) => {
            alert(err);
          });
      } else {
        alert(err);
      }
    },
    onWarning(msg) {
      alert(msg);
    },
    onLocalJoin() {
      let htmlStr = "<div>" + this.username + "</div>";
      htmlStr += '<button id="toggle-mute-audio">Mute</button>';
      htmlStr += '<button id="toggle-mute-video">Pause webcam</button>';
      htmlStr +=
        '<video id="myvideo" style="width:inherit;" autoplay muted="muted"/>';
      document.getElementById("videolocal").innerHTML = htmlStr;
      const target = document.getElementById("myvideo");
      this.videoroom.attachStream(target, 0);
      const muteAudioButton = document.getElementById("toggle-mute-audio");
      const muteVideoButton = document.getElementById("toggle-mute-video");
      muteVideoButton.onclick = this.toggleMuteVideo;
      muteAudioButton.onclick = this.toggleMuteAudio;
    },
    onRemoteJoin(index, remoteUsername, feedId) {
      document.getElementById("videoremote" + index).innerHTML =
        "<div>" +
        remoteUsername +
        ":" +
        feedId +
        '</div><video style="width:inherit;" id="remotevideo' +
        index +
        '" autoplay/>';
      const target = document.getElementById("remotevideo" + index);
      this.videoroom.attachStream(target, index);
    },
    onRemoteUnjoin(index) {
      document.getElementById("videoremote" + index).innerHTML =
        "<div>videoremote" + index + "</div>";
    },
    onVolumeMeterUpdate(streamIndex, volume) {
      const el = document.getElementById("volume-meter-0");
      el.style.width = volume + "%";
    },
  },
};
</script>
<style scoped>
.btn-primary {
  margin-left: 5px;
}
</style>
