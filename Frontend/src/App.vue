<template>
  <v-app>
    <v-app-bar
      app
      dense
      
      color="white"
      height="35"
      style="z-index: 2147483647"
    >
      <div class="d-flex align-center">
        <router-link to="/">
          <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            src="./assets/logo-black .png"
            transition="scale-transition"
            width="110"
        /></router-link>
      </div>
      <v-spacer></v-spacer>

      <!-- <router-link to="/" class="router-link"><v-btn text>Home</v-btn></router-link> -->
      <span span v-if="isLoggedIn">
        <router-link to="/BoardList" class="router-link"
          ><v-btn text>My Boards</v-btn></router-link
        >
      </span>
      <span v-if="!isLoggedIn">
        <router-link to="/login" class="router-link"
          ><v-btn text>Login</v-btn></router-link
        >
      </span>
      <span v-if="isLoggedIn">
        <v-btn @click="emitLogout" text>Logout</v-btn>
      </span>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Vue from "vue";
import { mapActions, mapGetters } from "vuex";
// import WebRTC from 'vue-webrtc'
// Vue.use(WebRTC);

import * as io from "socket.io-client";
window.io = io;

export default {
  name: "App",

  data: () => ({
    //
  }),
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },
  methods: {
    ...mapActions(["logout"]),
    emitLogout() {
      this.$socket.emit("logout");
      this.logout();
    },
  },
  created() {
    this.$socket.on("logout", () => {
      // alert('asdf');
      this.logout();
    });
    Vue.loadScript(
      "https://cdnjs.cloudflare.com/ajax/libs/webrtc-adapter/6.0.3/adapter.min.js"
    );
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@300;900&display=swap");
@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&display=swap');
@font-face {
    font-family: 'HangeulNuri-Bold';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
@font-face {
    font-family: 'NEXON Lv1 Gothic OTF';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/NEXON Lv1 Gothic OTF.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.router-link {
  text-decoration: none;
}
body::-webkit-scrollbar {
  width: 0;
}
*::-webkit-scrollbar {
  width: 5px; 
}

*::-webkit-scrollbar-track {
  background: #ffffff;
}

*::-webkit-scrollbar-thumb {
  background: #77b2d4;
}
*::-webkit-scrollbar-track {
  background: #ffffff;
}

*::-webkit-scrollbar-thumb {
  background: #77b2d4;
}

video {
  display: flex;
  width: 200px;
  height: 150px;
  transform: rotate(0deg);

  -moz-transform: scaleX(-1);

  -o-transform: scaleX(-1);

  -webkit-transform: scaleX(-1);

  transform: scaleX(-1);
}
.unMute{
  color:  #CC3B33;
}
.stopVideo{
  color:  #CC3B33;
}
.control__buttons{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0px !important;
  width: 80px;
  cursor: pointer;
}

.v-color-picker__controls {
  display: none !important;
}
.v-dialog {
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 !important;
  z-index: 20000000000000000 !important;
}
.v-overlay__scrim,
.v-tooltip {
  z-index: 20000000000000000 !important;
}

</style>