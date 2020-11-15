<template>
  <div style="height:100%;">
    <!-- <div>Layout Phase</div> -->
    <!-- <v-col cols="12">
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
    </v-col> -->
    <div style="height:30%;" ref="videolocal" id="videolocal">
        <div v-if="isPublished" class="video__self">
          <video
            :id="'video-' + username"
            autoplay
            style="height:150px;"
            muted="muted"
          />
        </div>
        <!-- <v-col class="col-12 div__username" v-if="username">
            {{ username }}
          </v-col> -->
      <v-col cols="12" class="control" v-if="sessionId" style="height:20%;display:flex;align-items:center;">
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
          @click="publishButtonHandler"
        >
          <i class="xi-log-out xi-x"></i>
        </v-btn>
      </v-col>
      <!-- 
        <v-col class="col-12">
          <v-btn
            type="button"
            ref="presenter"
            id="presenter"
            color="red"
            elevation="2"
            @click="presenterButtonHandler"
          >
            Presenter
          </v-btn>
        </v-col> 
      -->
    </div>
    <!-- <div class="border" /> -->
    <div style="height:65%;padding-right:2px;">
      <v-row dense style="width:100%;height:25%;margin:0;">
        <v-col style="height:100%;padding:0;display:flex;flex-direction:column;align-items:center;" v-for="(value, key) in subscriberList" :key="key" cols="6">
          <video style="box-sizing:content-box;width:100%;height: 110px; margin: 5px auto 5px;" :id="value.videoTagId" autoplay />
          <p style="text-align:center;color:white;position:relative;" class="div__username">{{ value.remoteUserName }}</p>
        </v-col>
      </v-row>
    </div>
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
      isPublished: false,
    };
  },
  async created() {
    this.roomId = await this.$route.params.code;
    this.username = await this.$store.state.uid.username;
  },
  async mounted() {
    const device_info = await navigator.mediaDevices.enumerateDevices();
    const camera_permission = await navigator.permissions.query({
      name: "camera",
    });
    const microphone_permission = await navigator.permissions.query({
      name: "microphone",
    });
    await this.SET_IS_CAMERA(
      !!(
        (await !!device_info.find((element) => element.kind === "videoinput")) &
        (camera_permission.state === "granted")
      )
    );
    await this.SET_IS_MICROPHONE(
      !!(
        (await !!device_info.find((element) => element.kind === "audioinput")) &
        (microphone_permission.state === "granted")
      )
    );
    this.startbuttonHandler(); // Uncomment Here when Ready
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
      "isCamera",
      "isMicrophone",
    ]),
    ...mapGetters("videoroom", ["getSessionId", "getVideoRoom", "getOptions"]),
  },
  watch: {},
  methods: {
    ...mapActions("videoroom", [
      "register",
      "publish",
      "unpublish",
      "toggleMuteVideo",
      "toggleMuteAudio",
      "initializeJanusRoom",
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
      "SET_IS_CAMERA",
      "SET_IS_MICROPHONE",
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
        publishOwnFeed: false,
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
    async onError(err) {
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
    async startbuttonHandler() {
      await this.infoInitializer();
      await this.SET_VIDEO_ROOM();
      await this.SET_SUBSCRIBER_INIT();
      await this.initializeJanusRoom(this.username);
      this.isPublished = true;
    },
    stopbuttonHandler() {
      this.leaveRoomHandler();
    },
    publishButtonHandler() {
      if (this.isPublished) {
        this.unpublish();
        this.isPublished = false;
      } else {
        this.publish();
        this.isPublished = true;
      }
    },
    presenterButtonHandler() {
      this.$emit("presenter");
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
  /* border: 2px solid skyblue; */
}
.video__self {
  display: flex !important;
  flex-direction: column !important;
  align-content: center !important;
  justify-content: center !important;
  height: 80%;
}
.users__video {
  overflow-y: scroll !important;
  height: 300px;
}
video {
  box-sizing: content-box;
  margin: 15px auto 15px;
  height: 100%;
}
</style>
