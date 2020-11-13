<template>
 <div style="height:100%;width:100%;">
    <v-dialog
      v-model="dialog"
      max-width="800"
      max-height="800"
      style="z-index:20000000000000000;"
    >
      <template v-slot:activator="{ on, attrs }">
          <img class="noteImg" v-bind="attrs" v-on="on" :src="src">
      </template>
      <!-- <v-card style="display:flex;justify-content:center;align-items:center;width:60%;height:auto;"> -->
        <img class="modalImg" :src="src">
        <!-- <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Disagree
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Agree
          </v-btn>
        </v-card-actions> -->
      <!-- </v-card> -->
    </v-dialog>
  </div>
</template>

<script>
export default {
    name: 'NoteImage',
    data() {
        return {
            dialog: false,
        }
    },
    props: {
        src: String,
    }
}
</script>

<style scoped>
img.noteImg {
    display: block;
    margin: 0 auto 0;
    object-fit: cover;
    max-height: 100%;
    width: 100%;
    border: 2px solid rgba(0,0,0,0);
}
.noteImg:hover {
    border: 2px solid rgb(63, 192, 243);
    
}
img.modalImg {
    max-height: 100%;
    max-width: 100%;
}

</style>