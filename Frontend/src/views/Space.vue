<template>
  <div class="corkback">
    <Board/>
  </div>
</template>

<script>
// import Chat from "../components/Chat.vue";
import Board from '@/components/Board.vue';

export default {
  data: () => {
    return {
      cards: [
        { title: 'Pre-fab homes', src: '../assets/', flex: 6 },
        { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
        { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
        { title: 'Best airlinsses', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
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
          content: '<video id="videoInput" width="200px"></video>',
        },

      ]
    }
  },
  components: {
    Board
  },
  methods: {
    onResize: (x, y, width, height) => {
      this.x = x
      this.y = y
      this.width = width
      this.height = height
    },
    onDrag: (x, y) => {
      this.x = x
      this.y = y
    }
  },
  mounted() {
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

        var constraints = { 
          audio: false, 
          video: true, 
          };

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
}
</script>

<style scoped>
.corkback {
  /* background-image: url('../assets/cork_board.jpg'); */
  height: 100%;
  width: 100%;
  /* background-size: 20%; */
  
}
.line{
    /* width: 100%; */
    /* height: 35px; */
    position: absolute;
    fill: rgb(255, 0, 0); 
    transform: rotate(10deg) translateX(-50%) translateY(-15px);
    cursor: pointer;
    margin-left: auto;
    left: 50%;
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
  border: none;
}
.vdr {
  box-shadow: 0px 34px 36px -26px rgba(0,0,0,.5);
  background: linear-gradient(-55deg, transparent 1.5em, #ffea4b 0) no-repeat;
  border: none;
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