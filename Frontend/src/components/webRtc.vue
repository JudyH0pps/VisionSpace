<template>
  <div>
    <div class="main__right">
      <div class="main__header">
        <h2>Room</h2>
      </div>
      <div id="video-grid" class="web__video"></div>
      <div class="web__members">팀원 목록</div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import VuePeerJS from "vue-peerjs";
import Peer from "peerjs";

Vue.use(VuePeerJS, new Peer({}));

export default {
  name: "app",
  components: {},
  data() {
    return {
      img: null,
      roomId: "public-room",
      myVideoStream: "",
      videoGrid: null,
      peer: new Peer({
        path: "/peerjs",
        host: "/",
        port: "8081",
      }),
      peers: {},
    };
  },
  computed: {},
  watch: {},
  methods: {
    addVideoStream(video, stream) {
      // console.log("스트리밍 테스트!!!!!! :",stream)
      video.srcObject = stream;
      // console.log("비디오 테스트!!!!!! :",video.srcObject)
      video.addEventListener("loadedmetadata", () => {
        video.play();
      });
      this.videoGrid.append(video);

      // console.log("videoGrid :", this.videoGrid)
    },
    connectToNewUser(userId, stream) {
      const call = this.peer.call(userId, stream);
      const video = document.createElement("video");
      call.on("stream", (userVideoStream) => {
        this.addVideoStream(video, userVideoStream);
      });
      call.on("close", () => {
        console.log("나가요!!!");
        video.remove();
      });

      this.peers[userId] = call;
      console.log(this.peers)
    },
  },

  created() {
    this.peer.on("open", (id) => {
      // open 은 socket. connection과 비슷한듯
      console.log("peer id : ", id); // id는 자신의 id
      this.$socket.emit("join-room", this.roomId, id);
    });
  },
  mounted() {
    this.myVideo = document.createElement("video");
    this.videoGrid = document.getElementById("video-grid");
    this.myVideo.muted = true;
    // this.$nextTick(() => {
    //   // console.log(`lskdnv${this.videoGrid}`);
    // })
    navigator.mediaDevices
      .getUserMedia({
        video: true,
        audio: false,
      })
      .then((stream) => {
        this.myVideoStream = stream;
        this.addVideoStream(this.myVideo, stream);
        // console.log("Stream 완료오오오오");
        setTimeout(() => {}, 2000);
        this.peer.on("call", (call) => {
          call.answer(stream);
          const video = document.createElement("video");
          call.on("stream", (userVideoStream) => {
            this.addVideoStream(video, userVideoStream);
          });
        });
        this.$socket.on("user-connected", (userId) => {
          setTimeout(() => {
            this.connectToNewUser(userId, stream);
          }, 2000);
          // this.connectToNewUser(userId);
          // setTimeout(function () {
          //       this.connectToNewUser(userId);
          //   }, 2000)
        });
      })
      .catch((err) => {
        console.log("에러났다!!!!!!!!!!!!!!!!!!", err);
      });

    //     peer.on('call', call => {
    //     call.answer(stream);
    //     const video = document.createElement('video')
    //     call.on('stream', userVideoStream => {
    //         addVideoStream(video, userVideoStream)
    //     })
    // })
    this.$socket.on("user-disconnected", (userId) => {
      console.log("잘 받고 있나 모르겠네", userId);
      if (this.peers[userId]) this.peers[userId].close();
    });
  },
};
</script>
<style scoped>
div {
  padding: 0;
  margin: 0;
}
.btn-primary {
  margin-left: 5px;
}
.main__right {
  display: flex;
  flex-direction: column;
  background-color: #242323;
  border-left: 1px solid;
  height: 100vh;
}
.video-grid {
  display: flex;
  justify-content: center;
  flex-grow: 1;
  overflow-y: scroll;
}
.main__header {
  color: #f5f5f5;
  text-align: center;
}
.web__members {
  padding: 22px 12px;
  display: flex;
  border: none;
  color: #f5f5f5;
}
</style>