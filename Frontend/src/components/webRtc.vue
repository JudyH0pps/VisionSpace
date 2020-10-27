<template>
  <v-app>
  <div class="container">
    <div class="row">
      <div class="col-md-12 my-3">
        <h2>Room</h2>
        <input v-model="roomId" />
      </div>
    </div>
    <div class="row">
      <div class="col-1 col-md-12">
        <div class="">
          <vue-webrtc ref="webrtc" width="100%"
            :roomId="roomId"
            :enableAudio="false"
            :cameraHeight=78
            :autoplay="false"
            v-on:joined-room="logEvent"
            v-on:left-room="logEvent"
            v-on:opened-room="logEvent"
            @error="onError"
          />
        </div>

        <div class="row">
          <div class="col-md-12 my-3">
            
            <v-btn type="button" class="btn-primary" color="primary" @click="onJoin">
              Join
            </v-btn>
            <v-btn type="button" class="btn-primary" color="primary" @click="onLeave">
              Leave
            </v-btn>
            <v-btn type="button" class="btn-primary" color="primary" @click="onCapture">
              Capture Photo
            </v-btn>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <h2>Captured Image</h2>
        <figure class="figure">
          <img :src="img" class="img-responsive" style="width: 200px; height: 300px" />
        </figure>
      </div>
    </div>
    
  </div>
  </v-app>
</template>

<script>
import Vue from "vue";
import { WebRTC } from "plugin";
//   import { find, head } from 'lodash';


Vue.component(WebRTC, WebRTC);

export default {
  name: "app",
  components: {},
  data() {
    return {
      img: null,
      roomId: "public-room",
    };
  },
  computed: {},
  watch: {},
  methods: {
    onJoin() {
      this.$refs.webrtc.join();
    },
    onLeave() {
      this.$refs.webrtc.leave();
    },
    onCapture() {
      this.img = this.$refs.webrtc.capture();
    },
    onError(error, stream) {
      console.log("On Error Event", error, stream);
    },
    logEvent(event) {
      console.log("Event : ", event);
    },
    
  },
};
</script>
<style scoped>
.btn-primary{
  margin-left:5px;
}

</style>