<template>
  <v-container fluid>
    <v-card>
      <v-toolbar dense flat>
        <v-toolbar-title>문서편집기</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon>mdi-eye</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text>
        <v-textarea v-model="text"></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="read">read</v-btn>
        <v-btn @click="write">write</v-btn>
      </v-card-actions>
    </v-card>
    <div class="container">
      <div class="jumbotron">
        <p class="alert alert-info" id="drag-file">Drag your file here.</p>
      </div>
      <textarea
        id="txtarea"
        style="width: 700px; height: 350px"
        class="form-control"
      ></textarea
      ><br />
      <button id="btn" class="btn btn-success">Save</button>
    </div>
  </v-container>
</template>

<script>
// const { dialog } = require('electron').remote
// // const fs = require('fs')
// export default {
//   data () {
//     return {
//       text: ''
//     }
//   },
//   methods: {
//     read () {
//       const r = dialog.showOpenDialogSync()
//       if (!r) return
//       // fs.readFileSync
//       console.log(r)
//     },
//     write () {

//     }
//   }
// }
</script>

<style>
</style>
