<template>
  <v-app>
    <v-app-bar
      app
      dense
      color="rgba(0,0,0,0)"
      height="60"
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
export default {
  name: 'App',

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