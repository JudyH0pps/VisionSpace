<template>
  <div class="container">
    <!-- <div>Layout Phase</div> -->
    <v-col class="col-12">
      <v-btn
        v-if="!sessionId"
        no-gutters
        class="mr-2"
        type="button"
        ref="start"
        id="start"
        color="secondary"
        elevation="2"
        @click="startbuttonHandler"
        >영상 참여
      </v-btn>
    </v-col>
    <v-container>
      <v-row class="videoscreen" ref="videolocal" id="videolocal">
        <v-col class="col-12" v-if="sessionId">
          <video
            :id="'video-' + username"
            style="width: inherit"
            autoplay
            muted="muted"
          />
          <v-col class="col-12 div__username" v-if="username">
            {{ username }}
          </v-col>
        </v-col>
        <v-col class="col-12 control" v-if="sessionId">
          <v-btn
            type="button"
            class="control__buttons"
            id="toggle-mute-audio"
            @click="toggleMuteAudio"
          >
            <div class="control__buttons">
              <i class="fas fa-microphone"></i>
            </div>
          </v-btn>
          <v-btn
            type="button"
            id="toggle-mute-video"
            class="control__buttons"
            @click="toggleMuteVideo"
          >
            <div class="control__buttons">
              <i class="fas fa-video"></i>
            </div>
          </v-btn>
          <v-btn
            type="button"
            ref="stop"
            id="stop"
            color="white"
            elevation="2"
            @click="stopbuttonHandler"
          >
            <i class="xi-log-out xi-x"></i>
          </v-btn>
        </v-col>
      </v-row>
      <div class="border" />
      <v-row>
        <v-col class="col-12" v-for="(value, key) in subscriberList" :key="key">
          <div class="videoscreen" :id="value.remoteId">
            <video style="width: inherit" :id="value.videoTagId" autoplay />
            <p class="div__username">{{ value.remoteUserName }}</p>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import SERVER from "@/api/drf";
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";

export default {
  name: "WebRTC",
  components: {},
  data() {
    return {
      roomId: null,
      username: null,
      isCamera: null,
      isMic: null,
    };
  },
  async created() {
    this.roomId = await this.$route.params.code;
    this.username = await this.$store.state.uid.username;
  },
  mounted() {
    // this.startbuttonHandler(); // Uncomment Here when Ready
  },
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
        onVolumeMeterUpdate: this.onVolumeMeterUpdate,
        debug: false,
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
            publishers: 24,
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
            console.log(err);
          });
      } else {
        console.log(err);
      }
    },
    onWarning(msg) {
      console.log(msg);
    },
    async onLocalJoin() {
      // 내 로컬의 미디어스트림이 송출 될 때 호출된다.
      const target = document.getElementById("video-" + this.username);
      this.videoroom.attachStream(target, 0);
      await this.toggleMuteVideo();
      await this.toggleMuteAudio();
    },
    async onRemoteJoin(index, remoteUsername, feedId) {
      console.log("onRemoteJoin:", feedId);
      await this.SET_SUBSCRIBER_INSERT({
        remoteId: "videoremote" + index,
        videoTagId: "video-" + remoteUsername,
        remoteUserName: remoteUsername,
        feedIndex: index,
      });

      const target = document.getElementById("video-" + remoteUsername);
      this.videoroom.attachStream(target, index);
    },
    onRemoteUnjoin(index) {
      // 놀랍게도 RemoteUnjoin 시에는 index만 주어진다.
      this.SET_SUBSCRIBER_OUT({
        remoteId: "videoremote" + index,
      });
    },
    onVolumeMeterUpdate(streamIndex, volume) {
      let target_remotevideo = null;

      if (streamIndex == 0) {
        target_remotevideo = "video-" + this.username;
      } else {
        target_remotevideo = this.subscriberList["videoremote" + streamIndex]
          .videoTagId;
      }

      let el = document.getElementById(target_remotevideo);
      if (el) {
        if (volume > 3) {
          el.classList.add("sound-feed");
        } else {
          el.classList.remove("sound-feed");
        }
      }
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
  /* overflow-y: scroll; */
  height: 100%;
}
.btn-primary {
  margin-left: 5px;
}
.scroll {
  overflow: scroll;
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
.control__buttons {
  width: 70px;
}
.sound-feed {
  border: 2px solid rgb(60, 255, 0);
}
</style>
