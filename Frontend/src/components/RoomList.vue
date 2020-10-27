<template>
  <div>
    <!-- <v-card class="mx-auto" max-width="370" v-for="n in 5" v-bind:key="n">
      <v-img
        class="black--text align-end"
        height="300px"
        src="@/assets/note.jpg"
      >
        <v-card-title>{{ n }}번째 보드</v-card-title>
      </v-img>
    </v-card> -->
    <v-container class="lighten-5">
      <!-- Stack the columns on mobile by making one full-width and the other half-width -->

      <!-- Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop -->
      <v-row>
        <v-col v-for="n in 5" :key="n" cols="6" md="4">
          <!-- <v-card
          class="pa-2"
          outlined
          tile
        > -->
          <router-link to="space"><v-img class="white--text" src="@/assets/board.png">
            <p class="text mt-10">{{ n }}번째 보드</p>
          </v-img></router-link>
          <!-- </v-card> -->
        </v-col>
        <v-col cols="6" md="4">
          <v-img class="plus" src="@/assets/plus.jpg"></v-img>
        </v-col>
      </v-row>

      <!-- Columns are always 50% wide, on mobile and desktop -->
    </v-container>
  </div>
</template>

<script>
export default {
  data: () => ({
    
  }),
};
</script>

<style>
.plus {
  width: 80%;
  padding: auto auto;
  margin: 50px;
  margin-left: auto;
  margin-right: auto;
}
.text {
  text-align: center;
  /* background-color: yellow; */
  position: absolute;
  top: 40%;
	left: 40%;
  /* transform: translate( -50%, -50% ); */
}
</style>