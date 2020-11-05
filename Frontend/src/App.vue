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
import { mapActions, mapGetters } from 'vuex'

import * as io from 'socket.io-client'
window.io = io



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
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@300;900&display=swap");

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

video {
  display: flex;
  width: 200px;
  height: 150px;
  transform:rotate(0deg);

   -moz-transform: scaleX(-1); 

     -o-transform: scaleX(-1); 

-webkit-transform: scaleX(-1); 

        transform: scaleX(-1);  
}

</style>