<template>
  <div class="cork" style="height:100%; width: 100%;position: relative;">
    <v-btn
      class="mx-2"
      fab
      dark
      small
      color="white"
      @click.stop="drawer = !drawer"
      :class="{ open:drawer }"
    >
      <v-icon color="black">
        mdi-arrow-left
      </v-icon>
    </v-btn>
    <v-navigation-drawer
        right
        absolute
        v-model="drawer"
    >
      <template v-slot:prepend>
      <v-container fluid>
      <v-row dense>
        <v-col
          v-for="card in cards"
          :key="card.title"
          :cols="card.flex"
        >
          <v-card>
            <v-img
              src="../assets/person-icon.png"
              class="white--text align-end"
              height="100px"
            >
              <!-- <v-card-title v-text="card.title"></v-card-title> -->
            </v-img>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    </template>
    <v-divider></v-divider>
    <v-container fluid>
      <v-row dense>
        <p style="width:100%;text-align:center;">Add new note</p>
        <!-- <Chat /> -->
        <textarea class="note" type="text-area"></textarea>

        <!-- <div class="note" style="height:220px;width:220px;"> -->
        <!-- </div> -->
      </v-row>
    </v-container>
    </v-navigation-drawer>
    <vue-draggable-resizable v-for="note in notes" :key="note.no" :w="220" :h="220" :x="note.x" :y="note.y" @dragging="onDrag" :resizable="false" :parent="true" :drag-handle="'.line'">
      <svg class="line" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="40" height="40" viewBox="0 0 24 24"><path d="M16,12V4H17V2H7V4H8V12L6,14V16H11.2V22H12.8V16H18V14L16,12Z" /></svg>
      <div class="content" v-html="note.content">
      </div>
    </vue-draggable-resizable>
  </div>
</template>

<script>
// import Chat from "../components/Chat.vue";

export default {
  data: function () {
    return {
      cards: [
        { title: 'Pre-fab homes', src: '../assets/', flex: 6 },
        { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
        { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
      ],
      drawer: false,
      notes: [
        {
          no: 0,
          width: 0,
          height: 0,
          x: 400,
          y: 300,
          content: '<lottie-player src="https://assets6.lottiefiles.com/packages/lf20_R7CRMj.json"  background="transparent"  speed="1"  loop  autoplay></lottie-player>'
        },
        {
          no: 1,
          width: 0,
          height: 0,
          x: 150,
          y: 200,
          content: "<p>Good</p>",
        },
        {
          no: 2,
          width: 0,
          height: 0,
          x: 750,
          y: 200,
          content: '<video id="videoInput" width="200"></video>',
        },
      ]
    }
  },
  methods: {
    onResize: function (x, y, width, height) {
      this.x = x
      this.y = y
      this.width = width
      this.height = height
    },
    onDrag: function (x, y) {
      this.x = x
      this.y = y
    }
  },
  mounted() {
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

        var constraints = { audio: false, video: true };

        var video = document.getElementById("videoInput");

        function successCallback(stream) {
            video.srcObject = stream;
            video.play();
        }

        function errorCallback(error) {
            console.log(error);
        }
        navigator.getUserMedia(constraints, successCallback, errorCallback);
  },
  components: {
    // Chat
  },
}
</script>

<style scoped>
.cork {
  background-image: url('../assets/cork_board.jpg');
  background-size: 100%;
}
.line{
    /* width: 100%; */
    /* height: 35px; */
    position: absolute;
    fill: rgb(255, 0, 0); 
    transform: rotate(10deg) translateY(-15px);
    cursor: pointer;
}
.line:hover{
  fill: rgb(252, 76, 76); 
}
.note {
  box-shadow: 0px 34px 36px -26px hsla(0, 0%, 0%, 0.5);
  background: linear-gradient(transparent 0em, #ffea4b 0) no-repeat;
  margin-left: auto;
  margin-right: auto;
  height:220px;
  width:220px;
  outline: none;
  resize: none;
  padding: 25px 10px 25px;
}
.vdr {
  box-shadow: 0px 34px 36px -26px rgba(0,0,0,.5);
  background: linear-gradient(-55deg, transparent 1.5em, #ffea4b 0) no-repeat;
}
.vdr::after{
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  display: inline-block;
  /* background: linear-gradient(-135deg, transparent 1.5em, rgb(239, 248, 106) 0) no-repeat; */
  border-bottom-left-radius: 5px;
  background-repeat: no-repeat;
  height: 3em;
  width: 1.35em;
  transform: translate(-3px, 175px) rotate(59.5deg);
  background: linear-gradient(to left bottom, transparent 50%, #cec365 0, #e9faab 27px, #d1b562);
  box-shadow: 0 6px 4px -4px #112429;
}
.content {
  padding: 25px 10px 25px;
  height: 100%;
  width: 100%;
  display:flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 2em;
}
.v-btn {
  position: absolute;
  top: 50%;
  right: 0px;
  translate: linear;
}
.open {
  transform: translateX(-255px) rotate(180deg);
}
</style>