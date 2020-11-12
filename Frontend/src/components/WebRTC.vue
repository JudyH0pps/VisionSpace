<template>
  <div class="container">
    <div>Layout Phase</div>

    <v-container>
      <v-row class="videoscreen" ref="videolocal" id="videolocal">
        <v-col class="col-12" v-if="sessionId">
          <video id="myvideo" style="width: inherit" autoplay muted="muted" />
        </v-col>
        <v-col class="col-12" v-if="username">
          {{ username }}
        </v-col>
        <v-col class="col-12">
          <v-btn
            no-gutters
            class="mr-2"
            type="button"
            ref="start"
            id="start"
            color="secondary"
            elevation="2"
            @click="startbuttonHandler"
          >
            Start
          </v-btn>
          <v-btn
            type="button"
            ref="stop"
            id="stop"
            color="secondary"
            elevation="2"
            @click="stopbuttonHandler"
          >
            Stop
          </v-btn>
        </v-col>
        <v-col class="col-12" v-if="sessionId">
          <v-btn type="button" id="toggle-mute-audio" @click="toggleMuteAudio"
            >Mute</v-btn
          >
          <v-btn type="button" id="toggle-mute-video" @click="toggleMuteVideo"
            >Pause webcam</v-btn
          >
          <!-- <v-btn
            type="button"
            ref="sharescreen"
            id="sharescreen"
            color="accent"
            elevation="2"
            @click="sharescreenButtonHandler"
          >
            Start Share Screen
          </v-btn>
          <v-btn
            type="button"
            ref="stopshare"
            id="stopshare"
            color="accent"
            elevation="2"
            @click="stopsharescreenButtonHandler"
          >
            Stop Share Screen -->
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="col-12" v-for="(value, key) in subscriberList" :key="key">
          <div class="videoscreen" :id="value.remoteId">
            <video style="width: inherit" :id="value.videoTagId" autoplay />
            <p>{{ value.remoteUserName }}</p>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import SERVER from "@/api/drf";
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";

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
  },
  mounted() {},
  destroyed() {
    this.leaveRoomHandler();
  },
  computed: {
    ...mapState("videoroom", [
      "sessionId",
      "videoroom",
      "options",
      "subscriberList",
      "publisherInfo",
    ]),
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
      "joinRoomHandler",
      "leaveRoomHandler",
    ]),
    ...mapMutations("videoroom", [
      "SET_SESSION_ID",
      "SET_VIDEO_ROOM",
      "SET_OPTION",
      "SET_SUBSCRIBER_INIT",
      "SET_SUBSCRIBER_INSERT",
      "SET_SUBSCRIBER_OUT",
      "SET_SUBSCRIBER_CLEAN",
    ]),

    infoInitializer() {
      // onVolumeMeterUpdate: this.onVolumeMeterUpdate, seems unstable. Disable it right now
      this.SET_SESSION_ID({
        sessionId: this.roomId,
      });
      this.SET_OPTION({
        server: SERVER.URL + "/rtc",
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
      });
    },
    onError(err) {
      // 에러의 원인: 생각보다 클린하게 종료되지 않는다. janus-room의 stop 기능을 활용해야 콜백 핸들링도 종료될 수 있다.
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
      // 내 로컬의 미디어스트림이 송출 될 때 호출된다.
      const target = document.getElementById("myvideo");
      this.videoroom.attachStream(target, 0);
    },
    async onRemoteJoin(index, remoteUsername, feedId) {
      console.log("onRemoteJoin:", index, remoteUsername, feedId);
      await this.SET_SUBSCRIBER_INSERT({
        remoteId: "videoremote" + index,
        videoTagId: "remotevideo" + index,
        remoteUserName: remoteUsername,
        feedIndex: index,
      });

      const target = document.getElementById("remotevideo" + index);
      this.videoroom.attachStream(target, index);
    },
    onRemoteUnjoin(index) {
      // 놀랍게도 RemoteUnjoin 시에는 index만 주어진다.
      this.SET_SUBSCRIBER_OUT({
        remoteId: "videoremote" + index,
      });

      document.getElementById("videoremote" + index).innerHTML =
        "<div>videoremote" + index + "</div>";
    },
    onVolumeMeterUpdate(streamIndex, volume) {
      const el = document.getElementById("volume-meter-0");
      el.style.width = volume + "%";
    },
    startbuttonHandler() {
      this.infoInitializer();
      this.SET_VIDEO_ROOM();
      this.SET_SUBSCRIBER_INIT();
      this.initializeJanusRoom(this.username);
    },
    stopbuttonHandler() {
      this.leaveRoomHandler();
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
