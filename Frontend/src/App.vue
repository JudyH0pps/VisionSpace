<template>
  <v-app>
    <v-app-bar
      app
      color="rgba(0,0,0,0)"
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="./assets/logo-black .png"
          transition="scale-transition"
          width="180"
        />
      </div>

      <v-spacer></v-spacer>

      <div>
        <vue-webrtc ref="webrtc" width="100%" roomId="sample-room"/>
      </div>

      <router-link to="/" class="router-link"><v-btn text>Home</v-btn></router-link>
      <router-link to="login" class="router-link"><v-btn text>Login</v-btn></router-link>
      <router-link to="logout" class="router-link"><v-btn text>Logout</v-btn></router-link>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Vue from 'vue'
import WebRTC from 'vue-webrtc'

import * as io from 'socket.io-client'
window.io = io

Vue.use(WebRTC)


export default {
  name: 'App',

  mounted: function () {
    this.$refs.webrtc.join()
  },
  components: {
  },

  data: () => ({
    //
  }),
};
</script>

<style>
.router-link {
  text-decoration: none;
}
</style>