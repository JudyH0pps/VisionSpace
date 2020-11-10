<template>
    <div class="container">
        <div v-show="false" class="col-1 col-md-12">
          <p>{{ roomId }}</p>
        </div>
   
          <v-btn type="button" ref="stop" id="stop" @click="stopbuttonHandler">
            Stop </v-btn
          ><br />
          <v-btn
            type="button"
            ref="sharescreen"
            id="sharescreen"
            @click="sharescreenButtonHandler"
          >
            Start Share Screen </v-btn
          ><br />
          <v-btn
            type="button"
            ref="stopshare"
            id="stopshare"
            @click="stopsharescreenButtonHandler"
          >
            Stop Share Screen </v-btn
          ><br />
          <div style="width: 500px">
            <div
              ref="volume-meter-0"
              id="volume-meter-0"
              style="height: 5px; width: 50%; background-color: green"
            ></div>
          </div>
          <div class="videoscreen" ref="videolocal" id="videolocal">
            videolocal
          </div>
          <div class="videoscreen" ref="videoremote1" id="videoremote1">
            videoremote1
          </div>
          <div class="videoscreen" ref="videoremote2" id="videoremote2">
            videoremote2
          </div>
          <div class="videoscreen" ref="videoremote3" id="videoremote3">
            videoremote3
          </div>
          <div class="videoscreen" ref="videoremote4" id="videoremote4">
            videoremote4
          </div>
          <div class="videoscreen" ref="videoremote5" id="videoremote5">
            videoremote5
          </div>
      </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import SERVER from "@/api/drf";
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
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
    this.username = this.$store.state.uid.username;
    this.infoInitializer();
    this.SET_VIDEO_ROOM();
  },
  mounted() {
    this.initializeJanusRoom(this.username);
  },
  destroyed() {
    this.leaveRoomHandler();
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
      "initializeJanusRoom",
      "leaveRoomHandler",
    ]),
    ...mapMutations("videoroom", [
      "SET_SESSION_ID",
      "SET_VIDEO_ROOM",
      "SET_OPTION",
    ]),

    infoInitializer() {
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
        onError: this.onError,
        onWarning: this.onWarning,
        onLocalJoin: this.onLocalJoin,
        onRemoteJoin: this.onRemoteJoin,
        onRemoteUnjoin: this.onRemoteUnjoin,
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
                room: self.roomId,
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
      console.log("onRemoteJoin:", index, remoteUsername, feedId);
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
    stopbuttonHandler() {
      this.unpublish();
    },
    sharescreenButtonHandler() {
      this.startShareScreen();
    },
    stopsharescreenButtonHandler() {
      this.stopShareScreen();
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
  overflow: scroll;
}
</style>
