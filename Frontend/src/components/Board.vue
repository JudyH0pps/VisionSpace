<template>
  <div class="cork" style="height:100%; width: 100%;position: relative;">
    <BoardDrawer @add_note="add" />
    <vue-draggable-resizable v-for="note in notes" :key="note.no" :w="220" :h="220" :x="note.x" :y="note.y" @dragging="onDrag" :resizable="false" :parent="true" :drag-handle="'.line'">
      <svg class="line" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="40" height="40" viewBox="0 0 24 24"><path d="M16,12V4H17V2H7V4H8V12L6,14V16H11.2V22H12.8V16H18V14L16,12Z" /></svg>
      <div class="content" v-html="note.content">
      </div>
    </vue-draggable-resizable>
  </div>
</template>

<script>
import BoardDrawer from "@/components/BoardDrawer.vue"

export default {
    name: 'Board',
    data: () => {
    return {
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
          content: "<p>왜안돼</p>",
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
  methods: {
    addVideoStream(video, stream) {
      video.srcObject = stream
      video.addEventListener('loadedmetadata', () =>{
        video.play()
      })
  
    },
    onResize(x, y, width, height) {
      this.x = x
      this.y = y
      this.width = width
      this.height = height
    },
    onDrag(x, y) {
      this.x = x
      this.y = y
    },
    add(text) {
        let new_note = {};
        new_note.no = 400;
        new_note.width = 0;
        new_note.height = 0;
        new_note.x = 0;
        new_note.y = 0;
        new_note.content = '<p>' + text + '</p>'
        this.notes.push(new_note)
    }
  },
  components: {
    // Chat
    BoardDrawer,
  },
}
</script>

<style scoped>
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
  /* display:flex;
  flex-direction: column;
  justify-content: center;
  align-items: center; */
  /* font-size: 2em; */
}
</style>