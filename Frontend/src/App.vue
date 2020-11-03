<template>
  <v-app>
    <v-app-bar
      app
      dense
      hide-on-scroll
      color="white"
      height="35"
      style="z-index: 2147483647;"
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

      <div>
        <vue-webrtc ref="webrtc" width="100%" roomId="sample-room"/>
      </div>

      <!-- <router-link to="/" class="router-link"><v-btn text>Home</v-btn></router-link> -->
      <span span v-if="isLoggedIn">
        <router-link to="/ex" class="router-link"><v-btn text>ex</v-btn></router-link>
      </span>
      <span span v-if="isLoggedIn">
        <router-link to="/BoardList" class="router-link"><v-btn text>My Boards</v-btn></router-link>
      </span>
      <span v-if="!isLoggedIn">
        <router-link to="/login" class="router-link"><v-btn text>Login</v-btn></router-link>
      </span>
      <span v-if="isLoggedIn">
        <v-btn @click="logout" text>Logout</v-btn>
      </span>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapGetters } from 'vuex'
import WebRTC from 'vue-webrtc'

import * as io from 'socket.io-client'
window.io = io

Vue.use(WebRTC)


export default {
  name: 'App',


  data: () => ({
    //
  }),
  computed: {
    ...mapGetters(['isLoggedIn']),
    
  },
  methods: {
    ...mapActions(['logout'])
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap');

.router-link {
  text-decoration: none;
}
body::-webkit-scrollbar{
    width: 0.25rem;
}

body::-webkit-scrollbar-track{
    background: #ffffff;
}

body::-webkit-scrollbar-thumb{
    background: #77b2d4;
}

</style>