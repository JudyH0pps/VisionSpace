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

      <!-- <v-btn
        target="_blank"
        text
      >
        <v-icon color="black">mdi-login</v-icon>
      </v-btn> -->
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',

  components: {
  },

  data: () => ({
    //
  }),
};
</script>
